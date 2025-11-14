# Release Note Builder

A simple Python console application that generates user-friendly release notes from GitHub issues using AI.

## Features

- Fetches closed GitHub issues within a specified date range
- Uses AI (Claude) to summarize changes in user-benefit focused language
- Categorizes updates into Features and Bug Fixes sections
- Outputs clean, professional Markdown with links to original issues
- Single-file implementation for simplicity

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
# Generate release notes for React repository
python release_notes.py facebook react 2024-01-01 2024-01-31

# Generate release notes for a smaller repo
python release_notes.py octocat Hello-World 2024-06-01 2024-06-30
```

## Output Format

The tool generates Markdown output with the following structure:

```markdown
# Release Notes: owner/repo

**Period:** 2024-01-01 to 2024-01-31

## Features

- Added dark mode support for better visibility in low-light environments ([#123](https://github.com/...))
- Improved performance when loading large datasets ([#145](https://github.com/...))

## Bug Fixes

- Fixed authentication errors that prevented users from logging in ([#134](https://github.com/...))
- Resolved display issues on mobile devices ([#142](https://github.com/...))
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
