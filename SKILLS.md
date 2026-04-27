# SA Assistant Agent: Skills Overview

## Purpose
Skills are specialized, repeatable workflows that guide the Gemini CLI to perform specific tasks. Unlike Agents, which define a "persona," Skills define a "procedure."

## Registry
- **`process-notes`**: Converts raw meeting notes (from Obsidian or Google Docs) into a structured format with summaries, action items, and technical requirements.
- **`prep-meeting`**: (Planned) Aggregates recent context to prepare a briefing for an upcoming interaction.
- **`analyze-emails`**: Uses the Gmail MCP to analyze recent email threads with a target, extracting active initiatives, SA action items, and stalled/forgotten conversations.
- **`schedule-tasks`**: Bridges Obsidian tasks to Google Calendar focus blocks with automated deep-linking and work-hour enforcement.
- **`redact-confidential`**: (Planned) Automatically anonymizes customer data for external reporting.
- **`rh-docs-downloader`**: Downloads all Red Hat product documentation guides as PDFs when provided with a base documentation URL.

## How to use
To invoke a skill, you can tell the CLI:
`"Run the process-notes skill on [Path/to/file]"` or `"Help me prep for my meeting with [Customer] using the prep-meeting skill."`
