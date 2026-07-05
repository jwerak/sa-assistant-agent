# SA Assistant Agent: Skills Overview

## Purpose
Skills are specialized, repeatable workflows that guide the AI assistant to perform specific tasks. Unlike Agents, which define a "persona," Skills define a "procedure."

## Registry
- **`process-notes`**: Converts raw meeting notes (from Obsidian or Google Docs) into a structured format with summaries, action items, and technical requirements.
- **`prep-meeting`**: (Planned) Aggregates recent context to prepare a briefing for an upcoming interaction.
- **`analyze-emails`**: Uses the Gmail MCP to analyze recent email threads with a target, extracting active initiatives, SA action items, and stalled/forgotten conversations.
- **`schedule-tasks`**: Bridges Obsidian tasks to Google Calendar focus blocks with automated deep-linking and work-hour enforcement.
- **`redact-confidential`**: (Planned) Automatically anonymizes customer data for external reporting.
- **`rh-docs-downloader`**: Downloads all Red Hat product documentation guides as PDFs when provided with a base documentation URL.
- **`rhdh-docs`**: Answers technical questions and drafts architectures for Red Hat Developer Hub 1.10 using locally downloaded official documentation (36 PDFs). Enforces a "read-before-answer" workflow to minimize hallucinations.
- **`generate-vault-index`**: Runs a Python script to regenerate `_vault_index.md` and `_stakeholder_map.md` from vault frontmatter, then reports consistency warnings.
- **`manage-contact`**: Creates or updates a Contact note with dynamic Interactions via an Obsidian Bases embed. Always creates both the `.md` contact file and the corresponding `_Meetings.base` file in `Contacts/_bases/`.
- **`rh-docs-ocp-4.21`**: Answers technical questions and drafts architectures for OpenShift Container Platform 4.21 using locally downloaded official documentation (112 PDFs). Enforces a "read-before-answer" workflow to minimize hallucinations.

## How to use
To invoke a skill, tell your AI CLI assistant:
`"Run the process-notes skill on [Path/to/file]"` or `"Help me prep for my meeting with [Company] using the prep-meeting skill."`
