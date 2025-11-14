#!/usr/bin/env python3
"""
Release Note Builder - Generate user-friendly release notes from GitHub issues

This tool uses the GitHub MCP server and Pydantic AI to fetch closed issues
within a date range and creates a summarized markdown document with features
and bug fixes. It includes an optional editor agent that reviews and refines
the generated output for clarity, consistency, and alignment with best practices.

Usage:
    python release_notes.py <owner> <repo> <start_date> <end_date> [--editor|--no-editor]

    Example:
    python release_notes.py facebook react 2024-01-01 2024-01-31
    python release_notes.py facebook react 2024-01-01 2024-01-31 --no-editor

Options:
    --editor      Enable editor review (default)
    --no-editor   Skip editor review for faster generation

Requirements:
    - GITHUB_TOKEN environment variable (create at https://github.com/settings/tokens)
    - OPENAI_API_KEY environment variable
    - Install dependencies: pip install -r requirements.txt
"""

import asyncio
import os
import sys
from datetime import datetime
from typing import Literal

from dateutil import parser as date_parser
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP


class IssueInfo(BaseModel):
    """Information about a closed issue"""

    title: str
    number: int
    url: str
    issue_type: Literal["feature", "bug"]
    user_benefit: str = Field(
        description="A single sentence describing the benefit to users, starting with a verb"
    )
    detail_summary: str | None = Field(
        default=None,
        description="One short paragraph expanding on the change using the issue description",
    )
    screenshot_urls: list[str] = Field(
        default_factory=list,
        description="Any screenshot URLs referenced in the issue description",
    )


class ThemeGroup(BaseModel):
    """A theme grouping of related issues"""

    name: str
    summary: str = Field(
        description="One sentence summarizing the user impact of this theme",
    )
    issues: list[IssueInfo] = Field(default_factory=list)


class ReleaseNotes(BaseModel):
    """Structured release notes output"""

    theme_groups: list[ThemeGroup] = Field(default_factory=list)
    features: list[IssueInfo] = Field(default_factory=list)
    bug_fixes: list[IssueInfo] = Field(default_factory=list)


class EditorReview(BaseModel):
    """Editor's review and refinement of release notes"""

    edited_markdown: str = Field(
        description="The improved version of the release notes markdown"
    )
    changes_made: list[str] = Field(
        default_factory=list,
        description="List of specific changes made to improve the release notes",
    )
    clarity_issues_fixed: list[str] = Field(
        default_factory=list,
        description="Clarity issues that were identified and fixed",
    )
    consistency_improvements: list[str] = Field(
        default_factory=list,
        description="Improvements made to ensure consistent tone and voice",
    )
    recommendations: list[str] = Field(
        default_factory=list,
        description="Optional recommendations for future improvements",
    )


# System prompt for the agent
SYSTEM_INSTRUCTIONS = """You are a technical writer creating release notes for software.

Your goal is to transform GitHub issues into user-friendly release notes.

Guidelines:
- Focus on USER BENEFITS, not technical implementation details
- Use consistent, professional tone throughout
- Start each bullet with a verb (e.g., "Added", "Fixed", "Improved", "Enabled")
- Keep descriptions concise but clear (1-2 sentences max)
- Group issues into clear THEMES when possible, each with a one-sentence summary
- Categorize issues as either "feature" (new functionality/improvements) or "bug" (fixes) for fallback
- Make the text feel cohesive, as if written by one person
- Avoid jargon unless necessary; explain technical terms simply

Examples:
- Good: "Added dark mode support for better visibility in low-light environments"
- Bad: "Implemented CSS variables for theme switching"
- Good: "Fixed authentication errors that prevented users from logging in"
- Bad: "Resolved OAuth token expiration bug in auth middleware"

When using GitHub tools:
- Use available MCP tools to search for and retrieve issue information
- Filter for closed issues within the specified date range
- Exclude pull requests, focus only on issues
- Read titles, labels, and full descriptions to infer themes, user benefits, and any screenshot URLs
- Extract key information including title, labels, body text, and attachments
"""

EDITOR_INSTRUCTIONS = """You are an experienced technical editor reviewing release notes for quality and consistency.

Your goal is to refine the release notes to ensure they are clear, aligned with best practices, and read as if written by a single, professional voice.

Review the release notes for:

1. CLARITY
   - Are descriptions immediately understandable?
   - Are there any ambiguous phrases that should be clarified?
   - Does each item clearly communicate what changed and the benefit?
   - Are sentences concise but complete?
   - Note: Technical jargon is acceptable for this technical audience

2. GOAL ALIGNMENT
   - Does each item focus on benefits and outcomes?
   - Do items start with action verbs (Added, Fixed, Improved, Enabled, etc.)?
   - Is the tone professional and informative?
   - Are we clearly explaining what changed?

3. CONSISTENCY
   - Does the entire document read like it was written by one person?
   - Is the sentence structure and phrasing style consistent throughout?
   - Are similar types of changes described in similar ways?
   - Is the level of detail consistent across all items?
   - Are theme descriptions and summaries formatted uniformly?

4. VOICE AND TONE
   - Is the tone professional and technical where appropriate?
   - Is the language active rather than passive?
   - Does the writing feel polished and publication-ready?
   - Is the style consistent throughout?

Make improvements to:
- Clarify confusing or ambiguous descriptions
- Strengthen weak benefit statements
- Ensure consistent verb tense and sentence structure
- Fix any grammar, punctuation, or formatting issues
- Improve flow and readability
- Ensure theme summaries accurately reflect their contained issues
- Maintain consistent level of technical detail throughout

Document your changes:
- List specific changes you made and why
- Note clarity issues you fixed
- Highlight consistency improvements
- Provide recommendations for future release notes if applicable

Preserve:
- All issue numbers and links
- Screenshot URLs and references
- The overall structure (themes, features, bug fixes)
- The factual accuracy of what was changed

Output the refined markdown that maintains accuracy while significantly improving clarity, consistency, and professional polish.
"""


async def generate_release_notes(
    owner: str, repo: str, start_date: datetime, end_date: datetime
) -> str:
    """Generate release notes for the given repository and date range using GitHub MCP server."""

    # Check for required environment variables
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError(
            "GITHUB_TOKEN environment variable is required. "
            "Get a token at https://github.com/settings/tokens"
        )

    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError(
            "OPENAI_API_KEY environment variable is required. "
            "Get a key at https://platform.openai.com/account/api-keys"
        )

    # Validate inputs
    if not owner or not repo:
        raise ValueError("Repository owner and name cannot be empty")

    print(f"Connecting to GitHub MCP server...")

    # Configure GitHub MCP server (remote hosted version)
    github_mcp = MCPServerStreamableHTTP(
        url="https://api.githubcopilot.com/mcp/",
        headers={
            "Authorization": f"Bearer {github_token}",
            "X-MCP-Toolsets": "issues,pull_requests",   # Limit what the agent can access
            "X-MCP-Readonly": "true"    # Don't allow any editing changes
        },
    )

    print(f"Fetching closed issues from {owner}/{repo}...")
    print(f"Date range: {start_date.date()} to {end_date.date()}")

    # Create the agent with GitHub MCP server
    agent = Agent(
        model="openai:gpt-5",
        output_type=ReleaseNotes,
        system_prompt=SYSTEM_INSTRUCTIONS,
        toolsets=[github_mcp],
    )

    # Construct the prompt for the agent
    prompt = f"""Using the GitHub MCP server tools, retrieve all closed issues from the repository {owner}/{repo} that were closed between {start_date.date()} and {end_date.date()}.

For each closed issue found:
1. Exclude any pull requests - only include actual issues
2. Read the title, labels, and full description/body text to understand the change, infer the user benefit, and identify any screenshot or image URLs
3. Determine if it's a feature or bug fix (for fallback categorization)
4. Write a user-focused benefit statement that explains what users gain
5. Capture a short detail summary (1 paragraph max) that references context from the description/body
6. Collect any screenshot URLs that illustrate the change

After analyzing all issues, infer broader THEMES that group related issues by user-facing outcomes. For each theme provide:
- A concise name (2-4 words) that users will understand
- A one-sentence summary emphasizing the impact of that theme
- All issues that belong to that theme

If no meaningful themes emerge, leave the theme list empty and ensure issues are still included in the appropriate feature or bug fix lists.

Search criteria:
- Repository: {owner}/{repo}
- State: closed
- Closed date: between {start_date.isoformat()} and {end_date.isoformat()}
- Type: issues only (not pull requests)

Return a ReleaseNotes object containing theme_groups plus feature and bug lists for fallback."""

    print("Generating release notes with AI...")

    try:
        # Run the agent (MCP server connected via toolsets parameter)
        result = await agent.run(prompt)
        release_notes = result.output
    except Exception as e:
        raise ValueError(f"Failed to generate release notes: {e}")

    # Check if we got any results
    if (
        not release_notes.theme_groups
        and not release_notes.features
        and not release_notes.bug_fixes
    ):
        return f"No closed issues found between {start_date.date()} and {end_date.date()}"

    # Format as markdown
    markdown = f"""# Release Notes: {owner}/{repo}

**Period:** {start_date.date()} to {end_date.date()}

"""

    def anchor_from_theme(name: str) -> str:
        """Create a GitHub-friendly anchor from a theme name."""
        anchor = name.strip().lower()
        cleaned = []
        for char in anchor:
            if char.isalnum():
                cleaned.append(char)
            elif char in {" ", "-"}:
                cleaned.append("-")
        anchor = "".join(cleaned)
        while "--" in anchor:
            anchor = anchor.replace("--", "-")
        anchor = anchor.strip("-")
        return anchor or "theme"

    if release_notes.theme_groups:
        markdown += "## Themes\n\n"
        for theme in release_notes.theme_groups:
            anchor = anchor_from_theme(theme.name)
            count = len(theme.issues)
            label = "item" if count == 1 else "items"
            markdown += (
                f"- [{theme.name}](#{anchor}): {theme.summary} ({count} {label})\n"
            )
        markdown += "\n"

        for theme in release_notes.theme_groups:
            anchor = anchor_from_theme(theme.name)
            markdown += f"## {theme.name}\n\n"
            markdown += f"{theme.summary}\n\n"
            for issue in theme.issues:
                markdown += f"- {issue.user_benefit} ([#{issue.number}]({issue.url}))\n"
                if issue.detail_summary:
                    markdown += f"  - {issue.detail_summary}\n"
                if issue.screenshot_urls:
                    for idx, url in enumerate(issue.screenshot_urls, start=1):
                        markdown += f"  - ![Screenshot {idx}]({url})\n"
            markdown += "\n"

        total_issues = sum(len(theme.issues) for theme in release_notes.theme_groups)
    else:
        if release_notes.features:
            markdown += "## Features\n\n"
            for feature in release_notes.features:
                markdown += (
                    f"- {feature.user_benefit} ([#{feature.number}]({feature.url}))\n"
                )
                if feature.detail_summary:
                    markdown += f"  - {feature.detail_summary}\n"
                if feature.screenshot_urls:
                    for idx, url in enumerate(feature.screenshot_urls, start=1):
                        markdown += f"  - ![Screenshot {idx}]({url})\n"
            markdown += "\n"

        if release_notes.bug_fixes:
            markdown += "## Bug Fixes\n\n"
            for bug in release_notes.bug_fixes:
                markdown += f"- {bug.user_benefit} ([#{bug.number}]({bug.url}))\n"
                if bug.detail_summary:
                    markdown += f"  - {bug.detail_summary}\n"
                if bug.screenshot_urls:
                    for idx, url in enumerate(bug.screenshot_urls, start=1):
                        markdown += f"  - ![Screenshot {idx}]({url})\n"
            markdown += "\n"

        total_issues = len(release_notes.features) + len(release_notes.bug_fixes)

    print(f"Successfully processed {total_issues} issues")

    return markdown


async def review_with_editor(markdown: str, owner: str, repo: str) -> EditorReview:
    """Review and refine release notes using an editor agent."""

    print("Running editor review for quality and consistency...")

    # Create the editor agent (no MCP tools needed, just reviewing markdown)
    editor_agent = Agent(
        model="openai:gpt-5",
        output_type=EditorReview,
        system_prompt=EDITOR_INSTRUCTIONS,
    )

    # Construct the prompt for the editor
    prompt = f"""Review and refine the following release notes for {owner}/{repo}.

Apply your editorial expertise to improve clarity, ensure consistency, and align with best practices while preserving all factual content.

Release Notes to Review:
{markdown}

Provide the refined markdown along with detailed documentation of changes made."""

    try:
        result = await editor_agent.run(prompt)
        return result.output
    except Exception as e:
        raise ValueError(f"Failed to complete editor review: {e}")


def parse_date(date_str: str) -> datetime:
    """Parse a date string into a datetime object."""
    try:
        return date_parser.parse(date_str)
    except Exception as e:
        raise ValueError(f"Invalid date format '{date_str}': {e}")


async def main():
    """Main entry point for the CLI."""
    if len(sys.argv) < 5 or len(sys.argv) > 6:
        print("Usage: python release_notes.py <owner> <repo> <start_date> <end_date> [--editor|--no-editor]")
        print("\nExample:")
        print("  python release_notes.py facebook react 2024-01-01 2024-01-31")
        print("  python release_notes.py facebook react 2024-01-01 2024-01-31 --editor")
        print("\nOptions:")
        print("  --editor      Enable editor review (default)")
        print("  --no-editor   Skip editor review")
        print("\nEnvironment variables required:")
        print("  - GITHUB_TOKEN: Your GitHub Personal Access Token")
        print("  - OPENAI_API_KEY: Your OpenAI API key")
        sys.exit(1)

    owner = sys.argv[1]
    repo = sys.argv[2]
    start_date_str = sys.argv[3]
    end_date_str = sys.argv[4]

    # Parse editor flag (default to True)
    use_editor = True
    if len(sys.argv) == 6:
        flag = sys.argv[5].lower()
        if flag == "--no-editor":
            use_editor = False
        elif flag == "--editor":
            use_editor = True
        else:
            print(f"Error: Unknown option '{sys.argv[5]}'. Use --editor or --no-editor")
            sys.exit(1)

    try:
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if start_date > end_date:
        print("Error: Start date must be before end date")
        sys.exit(1)

    try:
        release_notes = await generate_release_notes(owner, repo, start_date, end_date)

        # Run editor review if enabled
        final_markdown = release_notes
        if use_editor:
            editor_review = await review_with_editor(release_notes, owner, repo)

            # Display editor feedback
            print("\n" + "=" * 80)
            print("EDITOR REVIEW COMPLETE")
            print("=" * 80)

            if editor_review.changes_made:
                print("\nChanges Made:")
                for change in editor_review.changes_made:
                    print(f"  - {change}")

            if editor_review.clarity_issues_fixed:
                print("\nClarity Issues Fixed:")
                for issue in editor_review.clarity_issues_fixed:
                    print(f"  - {issue}")

            if editor_review.consistency_improvements:
                print("\nConsistency Improvements:")
                for improvement in editor_review.consistency_improvements:
                    print(f"  - {improvement}")

            if editor_review.recommendations:
                print("\nRecommendations:")
                for rec in editor_review.recommendations:
                    print(f"  - {rec}")

            final_markdown = editor_review.edited_markdown

        # Prompt for output filename
        print("\n" + "=" * 80)
        output_file = input("Output filename (press Enter for stdout): ").strip()

        if output_file:
            # Write to file
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(final_markdown)
            print(f"\nRelease notes saved to: {output_file}")
            print("=" * 80)
        else:
            # Output to stdout
            print("=" * 80)
            print("FINAL RELEASE NOTES")
            print("=" * 80 + "\n")
            print(final_markdown)

    except Exception as e:
        print(f"Error generating release notes: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
