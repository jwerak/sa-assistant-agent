# SA Assistant Agent: Project Overview

## Vision
To build a highly personalized, secure, and context-aware digital assistant tailored for the specific workflow of a Solutions Architect (Pre-sales) operating in the Google Cloud ecosystem. This project bridges the gap between structured meeting notes (Google Docs), local personal knowledge (Obsidian), and real-time communication (Gmail/Calendar).

## Core Principles
1. **Security & Confidentiality First:** All data processing respects the user's Enterprise Gemini privacy standards. Sensitive data stays within the Google/Local boundary.
2. **Contextual Intelligence:** Leverage MCP (Model Context Protocol) to seamlessly access Google Workspace and Obsidian data.
3. **Action-Oriented:** Focus on reducing administrative overhead (meeting prep, note processing) and enhancing strategic planning (account strategy, technical brainstorming).

## Data Strategy & Tooling Philosophy

To maintain a clean and efficient workspace, we adhere to the following role distribution between Obsidian and Google Workspace:

| Feature | **Obsidian** | **Google Drive / Workspace** |
| :--- | :--- | :--- |
| **Role** | **Primary Brain** — knowledge, records, context | **Collaboration Output** — sharing, cooperation |
| **Audience** | Personal (Internal use) | Team + Colleagues + Customers |
| **Organization** | Properties, categories, links, Atlas/Dashboards | Simple folders based on purpose |
| Lifecycle | Long-term, constantly updated SSOT | Per-document snapshots for sharing |

**Scheduling Constraints:**
- **Core Working Hours:** 08:30 - 17:00. Do not schedule focus sessions or tasks outside this window unless explicitly requested.
- **Deep Linking:** Every task-related calendar event MUST include an `obsidian://` deep link in the description.

---

## Agent Architecture
This project utilizes specialized `.agent.md` files to define distinct AI personas:
- **Account Strategist:** Long-term planning, relationship mapping, and opportunity identification.
- **Solution Architect (Technical):** Technical validation, architecture design, and competitive analysis.
- **Meeting Specialist:** Prep and post-processing of customer interactions.

## Skills & Workflows
Custom `.skill.md` files define repeatable procedures:
- `prep-meeting`: Automated briefing generation.
- `process-notes`: Structuring raw input into actionable intelligence.
- `redact-data`: Automated anonymization for external sharing.
