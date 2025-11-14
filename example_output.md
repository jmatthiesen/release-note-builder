# Example Output

This file shows what the generated release notes look like when using the GitHub MCP server integration.

## Sample Command

```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
export ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxx"

python release_notes.py jmatthiesen csharp-ai-buddy-site 2025-05-01 2025-11-01
```

## Expected Console Output

```
Connecting to GitHub MCP server...
Fetching closed issues from jmatthiesen/csharp-ai-buddy-site...
Date range: 2025-05-01 to 2025-11-01
Generating release notes with AI...
Successfully processed 16 issues

================================================================================
```

## Sample Output

```markdown
# Release Notes: jmatthiesen/csharp-ai-buddy-site

**Period:** 2025-05-01 to 2025-11-01

## Theme Summary

- [Chat Experience](#chat-experience): Made chatting more controllable, personalized, and easy to give feedback so you get better answers faster. (5 items)
- [Content Discovery](#content-discovery): Made it easier to find the latest news and relevant samples, starting from an improved home page. (4 items)
- [Look and Feel](#look-and-feel): Improved readability and comfort across devices with dark mode and mobile fixes. (2 items)
- [Secure Access](#secure-access): Protected your data and improved access control with HTTPS and per-user keys. (3 items)
- [Quality & Insights](#quality-insights): Increased reliability and guided future improvements with automated builds and privacy-friendly analytics. (2 items)

## Chat Experience

Made chatting more controllable, personalized, and easy to give feedback so you get better answers faster.

- Added a Stop button to cancel a streaming AI response and regain control instantly. ([#7](https://github.com/jmatthiesen/csharp-ai-buddy-site/issues/7))
  - While a response streams, Send is replaced with a Stop control; clicking it (or pressing Esc) halts the backend stream and restores the Send button, preventing unwanted tokens from continuing to arrive.
- Added chat options to target your preferred .NET version, AI provider, library, and model. ([#11](https://github.com/jmatthiesen/csharp-ai-buddy-site/issues/11))
  - An Options button opens a compact overlay where you choose .NET version, AI model provider, library, and model; these choices are sent as filters to guide retrieval and prompts, and experimental options are clearly flagged in responses.
- Added thumbs up/down on AI responses with an optional comment so you can quickly signal quality. ([#38](https://github.com/jmatthiesen/csharp-ai-buddy-site/issues/38))
  - Hovering a model response reveals rating controls that open a feedback dialog with OK/Cancel; your selection is highlighted and can be updated, and feedback is recorded to improve future answers.
- Improved the chat introduction to clearly state it answers C#/.NET AI development questions. ([#48](https://github.com/jmatthiesen/csharp-ai-buddy-site/issues/48))
  - The chat page description now uses a friendly "buddy" tone and explicitly frames the assistant's focus on AI development with C# and .NET so new users know what to expect.
- Fixed the Chat Options dialog by adding OK/Cancel with Enter/Esc support for faster, predictable changes. ([#51](https://github.com/jmatthiesen/csharp-ai-buddy-site/issues/51))
  - The dialog now applies changes and closes on OK (Enter), ignores changes on Cancel (Esc or Close), and behaves consistently with standard UI conventions.

## Content Discovery

Made it easier to find the latest news and relevant samples, starting from an improved home page.

- Added a searchable samples gallery with tags, filters, pagination, and deep links to help you find code faster. ([#5](https://github.com/jmatthiesen/csharp-ai-buddy-site/issues/5))
  - Browse sample cards showing title, author, MS-authored badge, tags, and a short description; open an overlay for full details and clone steps, search/filter in-browser, and share results via deep links with optional telemetry opt-out.
  - ![Screenshot 1](https://github.com/user-attachments/assets/a5612df9-2203-4da4-abc9-f679900edbce)
- Added a Latest News section with summaries, search, pagination, and RSS so you can stay current. ([#14](https://github.com/jmatthiesen/csharp-ai-buddy-site/issues/14))
  - View concise article cards (title, source, date, 140‑char summary, link) sourced from the site's indexed content, sorted newest to oldest and available as an RSS feed with search and paging.
- Added a welcoming home page with quick paths to Chat, News, and Samples plus feedback and policy links. ([#25](https://github.com/jmatthiesen/csharp-ai-buddy-site/issues/25))
  - The new home page summarizes the site, includes a question box that routes to Chat, and adds visible Feedback plus Terms of Service and Privacy Policy links across the site along with creator attribution.
- Fixed News sorting so articles reliably show newest first. ([#55](https://github.com/jmatthiesen/csharp-ai-buddy-site/issues/55))
  - The news listing now consistently orders content from newest to oldest to match expectations and make recent updates easier to find.

## Look and Feel

Improved readability and comfort across devices with dark mode and mobile fixes.

- Added a light/dark theme toggle that follows your OS setting and remembers your choice. ([#31](https://github.com/jmatthiesen/csharp-ai-buddy-site/issues/31))
  - Use a sun/moon switch with tooltips to change themes; the site mirrors OS theme changes automatically, stores your manual preference, and maintains accessible contrast in both modes.
- Fixed mobile layout issues so pages display cleanly without clipped headers or side scrolling. ([#46](https://github.com/jmatthiesen/csharp-ai-buddy-site/issues/46))
  - A mobile audit addressed a clipped sidebar header and right-side overflow on Samples and News, ensuring proper stacking and eliminating horizontal scrolling across Safari, Chrome, and Edge.

## Secure Access

Protected your data and improved access control with HTTPS and per-user keys.

- Secured browsing and API calls with HTTPS for safer, encrypted connections. ([#23](https://github.com/jmatthiesen/csharp-ai-buddy-site/issues/23))
  - All website and API traffic now enforces HTTPS, reducing the risk of interception and improving trust when using the service.
- Enabled early access via a temporary magic key so testers can try chat before general release. ([#26](https://github.com/jmatthiesen/csharp-ai-buddy-site/issues/26))
  - In production, chat requires a secret key that can be passed via URL and is stored in the browser until it expires (10 days or invalidated); development builds don't require the key.
- Enabled per-user API keys so access can be granted or revoked individually. ([#44](https://github.com/jmatthiesen/csharp-ai-buddy-site/issues/44))
  - The service now supports multiple keys (e.g., one per user) with the ability to disable any key server-side, replacing the prior single-key approach.

## Quality & Insights

Increased reliability and guided future improvements with automated builds and privacy-friendly analytics.

- Improved reliability with automated build checks for every change. ([#17](https://github.com/jmatthiesen/csharp-ai-buddy-site/issues/17))
  - GitHub Actions now builds the src/api and src/dataIngestion projects independently to validate pull requests compile cleanly before merging.
- Added lightweight, privacy-friendly analytics to help prioritize features you value most. ([#24](https://github.com/jmatthiesen/csharp-ai-buddy-site/issues/24))
  - Using GoatCounter, the site measures high-level usage such as chats started, interactions with results, sample/news searches and clicks, and "no results" events to inform UX improvements (LLM tracing handled separately).
```

## Key Features of the Output

1. **Theme-based organization** - Related features are grouped under user-friendly themes with summaries
2. **User-benefit focused** - Each line explains *why* users care about the change
3. **Two-level detail** - High-level bullets with expandable technical details
4. **Linked to source** - Every item links back to the original GitHub issue
5. **Consistent tone** - All text feels like it was written by the same person
6. **Professional formatting** - Clean Markdown that's ready to publish
7. **Visual elements** - Includes screenshots when available to illustrate features

## Customization

To adjust the writing style, tone, or categorization logic, edit the `SYSTEM_INSTRUCTIONS` constant in `release_notes.py` (lines 53-77).

## How It Works

1. **MCP Connection**: The tool connects to GitHub's remote MCP server using your GitHub token
2. **AI Agent Query**: The Pydantic AI agent uses the MCP server's tools to search for closed issues in the date range
3. **AI Analysis**: Claude analyzes each issue and categorizes it as a feature or bug fix
4. **User-Benefit Translation**: The AI rewrites technical issue titles into user-friendly benefits
5. **Markdown Generation**: The structured data is formatted into clean, professional markdown

This demonstrates a modern AI agent architecture where the AI autonomously uses tools (via MCP) to gather data and then processes it according to instructions.
