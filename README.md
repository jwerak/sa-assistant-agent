# SA Assistant Agent

A specialized AI agent configuration designed to assist a Solutions Architect (SA) in managing complex enterprise accounts, specifically within the CZ/SK region. This project integrates personal knowledge management (Obsidian) with communication channels (Gmail/Google Calendar) using the Model Context Protocol (MCP).

## 🎯 Vision
To reduce administrative overhead and enhance strategic planning by bridging the gap between structured meeting notes, real-time emails, and proactive scheduling.

## 🏛️ Architecture & Philosophy

The repository follows a clear **Data Strategy** as defined in `AGENTS.md`:
- **Obsidian:** The "Primary Brain" – stores knowledge, records, and context.
- **Google Workspace:** The "Collaboration Output" – for sharing with colleagues and customers.

### Project Structure
- **`GEMINI.md`**: Core system instructions and foundational mandates.
- **`AGENTS.md`**: Persona definitions (Account Strategist, Tech SA, etc.) and tool-use philosophy.
- **`SKILLS.md`**: A registry of repeatable procedural workflows.
- **`*.skill.md`**: Individual skill definitions (e.g., email analysis, task scheduling).
- **`*.agent.md`**: Detailed persona instructions for specific roles.

## 🚀 Key Skills
- **`analyze-emails`**: Scans Gmail threads to extract active initiatives and stalled conversations.
- **`process-notes`**: Transforms raw meeting notes into structured Obsidian account documents.
- **`schedule-tasks`**: Automatically time-blocks focus sessions on Google Calendar with deep links back to Obsidian notes.

## 🛠️ Usage
This repository is designed to be used with the **Gemini CLI**. To invoke the agent:
1. Ensure your Obsidian vault and Google Workspace MCPs are active.
2. Ask for specific tasks like:
   - *"Analyze my recent emails with SPCSS."*
   - *"Run the process-notes skill on my latest meeting log."*
   - *"Block 90 minutes on Monday for SPCSS preparation."*

## 🛡️ Security & Privacy
This agent adheres to high privacy standards:
- Customer confidential data stays within the user's secure boundaries (Local/Red Hat Google Workspace).
- No sensitive customer data is stored in this repository; only the logic to process it.
