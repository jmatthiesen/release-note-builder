# Release Note Builder

Creating release notes can be tedious. You need to review every closed issue, summarize features and bug fixes, and ensure consistent formatting—especially challenging when multiple team members contribute.

This repository demonstrates how AI can streamline this process by automatically:

* Finding all closed issues for a release (within a date range for now)
* Generating clear, consistent release notes
* Creating an at-a-glance summary of new features and fixes
* Writing a clean, professional Markdown file with links to original issues

The result: professional release notes that help users quickly understand what's new, without the manual effort.

## Requirements

- Python 3.10 or higher
- GitHub Personal Access Token (for MCP server authentication)
- OpenAI API Key (for AI model access)
- Internet connection (for remote MCP server)

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:

Create a `.env` file in the project root directory:

```bash
GITHUB_TOKEN=your_github_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

The application will automatically load these variables from the `.env` file when it runs.

### Getting Your API Keys

- **GitHub Token**: Create at [github.com/settings/tokens](https://github.com/settings/tokens)
  - Select "Generate new token (classic)"
  - Grant `repo` scope (read access to repositories)

- **OpenAI API Key**: Create at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
  - Sign up or log in
  - Click "Create new secret key"
  - Copy the key immediately (it won't be shown again)

## Usage

```bash
python release_notes.py <owner> <repo> <start_date> <end_date>
```

### Parameters

- `owner`: GitHub repository owner (user or organization)
- `repo`: Repository name
- `start_date`: Start of date range (ISO format: YYYY-MM-DD)
- `end_date`: End of date range (ISO format: YYYY-MM-DD)

### Examples

```bash
# Generate release notes for the csharp-ai-buddy-site project
python release_notes.py jmatthiesen csharp-ai-buddy-site 2025-09-01 2025-10-31

# Generate release notes for a smaller repo
python release_notes.py octocat Hello-World 2024-06-01 2024-06-30
```

## Output Format

The tool generates Markdown output with the following structure:

```markdown
**Period:** 2025-05-01 to 2025-11-01

## Theme Summary

- [Chat Experience](#chat-experience): Made chatting more controllable, personalized, and easy to give feedback so you get better answers faster. (5 items)
- [Content Discovery](#content-discovery): Made it easier to find the latest news and relevant samples, starting from an improved home page. (4 items)
...

## Chat Experience

Made chatting more controllable, personalized, and easy to give feedback so you get better answers faster.

- Added a Stop button to cancel a streaming AI response and regain control instantly. ([#7](https://github.com/jmatthiesen/csharp-ai-buddy-site/issues/7))
...
```

## Design Principles

The AI is instructed to:

- **Focus on user benefits** rather than technical implementation
- **Use consistent tone** throughout the release notes
- **Start with action verbs** (Added, Fixed, Improved, Enabled)
- **Keep descriptions concise** (1-2 sentences maximum)
- **Avoid jargon** unless necessary

## Technical Details

### Architecture

- **Framework**: Pydantic AI for agent-based architecture
- **MCP Integration**: GitHub MCP Server (remote hosted) for issue retrieval
- **AI Model**: OpenAI GPT-5 for natural language generation
- **Data Validation**: Pydantic models for structured outputs

### Implementation Notes

This implementation uses the **GitHub MCP (Model Context Protocol) Server** to fetch issues. The MCP server provides a standardized interface for AI agents to interact with GitHub's API.

**Why MCP?**
- Standardized tool interface for AI agents
- Demonstrates modern AI agent architecture patterns
- Leverages remote hosted MCP server (no local setup required)
- Shows integration between Pydantic AI and MCP servers

The agent connects to GitHub's remote MCP server at `https://api.githubcopilot.com/mcp/` using the `MCPServerStreamableHTTP` client with your GitHub token for authentication. The AI agent then uses the MCP server's tools to search for and retrieve closed issues within the specified date range.

For more information about the GitHub MCP Server, see the [GitHub MCP Server documentation](https://github.com/github/github-mcp-server).

### Rate Limiting

The tool uses the GitHub MCP server which respects GitHub API rate limits:
- Authenticated requests: 5,000 requests per hour
- The MCP server handles pagination and API calls internally

## Troubleshooting

### Common Issues

**"GITHUB_TOKEN environment variable is required"**
- Set your GitHub token as an environment variable before running

**"Authentication failed"**
- Check that your GitHub token is valid and hasn't expired
- Ensure the token has appropriate permissions

**"API rate limit exceeded"**
- Wait an hour or use a different token
- Check your rate limit: `curl -H "Authorization: Bearer $GITHUB_TOKEN" https://api.github.com/rate_limit`

**"Repository not found"**
- Verify the owner and repo name are correct
- Ensure the repository is public or your token has access to private repos

**"OPENAI_API_KEY environment variable is required"**
- Set your OpenAI API key as an environment variable
- Verify your API key is active at https://platform.openai.com/api-keys

## License

This project is licensed under the MIT License - feel free to modify and use as needed.

## Future Enhancements

Potential improvements for production use:
- Specify a milestone to use, instead of date range
- Support for multiple repositories in one run
- Custom categorization rules (e.g., by label)
- Template customization (different output formats)
- Integration with release management tools
- Support for other MCP servers (JIRA, Linear, etc.)
- Configurable AI prompts for different writing styles
