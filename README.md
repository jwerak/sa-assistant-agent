# SA Assistant Agent

A specialized AI agent workspace for Solutions Architects managing enterprise accounts. It bridges personal knowledge management (Obsidian) with Google Workspace (Gmail, Calendar, Drive, Docs) using AI CLI tools and the Model Context Protocol (MCP).

Built for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and [Gemini CLI](https://github.com/google-gemini/gemini-cli). Fork it, swap in your own accounts, and adapt the skills to your workflow.

## Table of Contents

- [What It Does](#what-it-does)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [1. Clone and Configure Environment](#1-clone-and-configure-environment)
  - [2. Set Up the Obsidian Vault](#2-set-up-the-obsidian-vault)
  - [3. Install the Google Workspace MCP](#3-install-the-google-workspace-mcp)
  - [4. Install Python Dependencies](#4-install-python-dependencies)
  - [5. Verify Setup](#5-verify-setup)
- [Project Structure](#project-structure)
- [Concepts](#concepts)
  - [Agents vs. Skills](#agents-vs-skills)
  - [Data Strategy: Obsidian vs. Google Workspace](#data-strategy-obsidian-vs-google-workspace)
- [Skills Reference](#skills-reference)
  - [process-notes](#process-notes)
  - [analyze-emails](#analyze-emails)
  - [schedule-tasks](#schedule-tasks)
  - [generate-vault-index](#generate-vault-index)
  - [rh-docs-downloader](#rh-docs-downloader)
- [Vault Schema](#vault-schema)
  - [Folder Layout](#folder-layout)
  - [Meeting Notes](#meeting-notes)
  - [Account Blueprints](#account-blueprints)
  - [Task Notes](#task-notes)
  - [Canonical Company Names](#canonical-company-names)
  - [Tags, Properties, and Categories](#tags-properties-and-categories)
- [Customizing for Your Accounts](#customizing-for-your-accounts)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)
- [Security and Privacy](#security-and-privacy)

---

## What It Does

When you open this project directory in Claude Code (or Gemini CLI), the AI assistant loads the system instructions from `CLAUDE.md` (or `GEMINI.md`) and gains the ability to:

- **Process meeting notes** -- transform raw notes into structured documentation with executive summaries, technical requirements, action items, and stakeholder insights.
- **Analyze email threads** -- scan Gmail for a customer or topic and surface active initiatives, stalled conversations, and forgotten action items.
- **Schedule focus time** -- find free slots on your Google Calendar and create "Focus Session" events with deep links back to relevant Obsidian notes.
- **Validate vault consistency** -- run a Python script that checks all your meeting notes, account blueprints, and tasks for missing fields, invalid company names, and formatting issues.
- **Download Red Hat docs** -- batch-download all PDF guides for a Red Hat product version.

The assistant also understands your vault schema -- it knows which frontmatter fields are required, which company names are canonical, and how to organize files. When you ask it to do something, it follows the conventions defined here rather than inventing its own.

## Architecture

```
You (SA)
  |
  v
AI CLI (Claude Code / Gemini CLI)
  |
  |-- reads: CLAUDE.md / GEMINI.md   (system instructions)
  |-- reads: *.agent.md              (persona definitions)
  |-- reads: *.skill.md              (procedural workflows)
  |-- reads: $SA_KNOWLEDGE_PATH/     (your Obsidian vault)
  |
  |-- MCP: @a-bonus/google-docs-mcp  (Gmail, Calendar, Drive, Docs, Sheets)
  |
  v
Outputs:
  - Structured meeting notes in Obsidian
  - Email analysis reports
  - Calendar events with deep links
  - Vault consistency reports
```

The repo contains **zero customer data**. It holds only the agent configuration, skill definitions, and processing scripts. All account-specific content lives in your Obsidian vault (pointed to by `$SA_KNOWLEDGE_PATH`).

## Prerequisites

| Requirement | Version | Purpose |
|---|---|---|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) or [Gemini CLI](https://github.com/google-gemini/gemini-cli) | Latest | AI CLI that loads system instructions and runs skills |
| [Node.js](https://nodejs.org/) | 18+ | Required for the Google Workspace MCP server |
| [Python](https://www.python.org/) | 3.7+ | Vault index generator script |
| [Obsidian](https://obsidian.md/) | Latest | Personal knowledge management (the vault) |
| Google account | -- | Gmail, Calendar, Drive access via MCP |

## Setup

### 1. Clone and Configure Environment

```bash
git clone https://github.com/YOUR_USER/sa-assistant-agent.git
cd sa-assistant-agent
cp .env.example .env
```

Edit `.env` and set `SA_KNOWLEDGE_PATH` to the root of your Obsidian vault:

```
SA_KNOWLEDGE_PATH=/home/youruser/ObsidianVault
```

The vault must contain (or you'll create) an `SA_Knowledge/` directory at this path. The assistant reads and writes files under `$SA_KNOWLEDGE_PATH/SA_Knowledge/`.

### 2. Set Up the Obsidian Vault

Create the expected folder structure inside your vault:

```
$SA_KNOWLEDGE_PATH/
  SA_Knowledge/
    Accounts/        # Account Blueprints (one per customer)
    Meetings/        # Meeting notes (one per meeting)
    Tasks/           # Task notes tracked via Obsidian Bases
    Atlas/           # Dashboards, vault map, indexes
    _VAULT_MAP.md    # Folder structure reference (optional)
    _vault_index.md  # Auto-generated by generate-vault-index
```

If you're starting fresh, just create the directories. The assistant will populate files as you process notes and analyze accounts.

**Recommended Obsidian Plugins:**
- **Obsidian Bases** (required) -- used for dashboards, task boards, and interaction logs. The assistant always creates `.base` files instead of Dataview queries.
- **Templater** (optional) -- useful for creating meeting note templates with pre-filled frontmatter.

### 3. Install the Google Workspace MCP

This project uses [`@a-bonus/google-docs-mcp`](https://github.com/a-bonus/google-docs-mcp) to access Gmail, Google Calendar, Google Drive, Google Docs, and Google Sheets through MCP.

#### 3.1 Create Google Cloud Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing one).
3. Enable the following APIs:
   - Gmail API
   - Google Calendar API
   - Google Drive API
   - Google Docs API
   - Google Sheets API
4. Go to **APIs & Services > Credentials**.
5. Click **Create Credentials > OAuth client ID**.
6. Choose **Desktop application** as the application type.
7. Download the credentials JSON file. You'll need the `client_id` and `client_secret` values from it.

#### 3.2 Authenticate

```bash
npx -y @a-bonus/google-docs-mcp auth
```

This opens a browser window for Google OAuth consent. After authorizing, a refresh token is saved to `~/.config/google-docs-mcp/token.json`. Your credentials never leave your machine.

#### 3.3 Configure Claude Code

Create `.claude/settings.json` in the project root (or add to it if it exists):

```json
{
  "mcpServers": {
    "google-sheets": {
      "command": "npx",
      "args": ["-y", "@a-bonus/google-docs-mcp"],
      "env": {
        "GOOGLE_CLIENT_ID": "YOUR_CLIENT_ID_HERE",
        "GOOGLE_CLIENT_SECRET": "YOUR_CLIENT_SECRET_HERE"
      }
    }
  }
}
```

> **Note:** Despite the key name `google-sheets`, this MCP server provides access to all Google Workspace services (Docs, Sheets, Drive, Gmail, Calendar). The name is a convention from the package.

For Gemini CLI, refer to the [Gemini CLI MCP documentation](https://github.com/google-gemini/gemini-cli) for equivalent configuration.

#### 3.4 Verify MCP Connection

Start Claude Code in the project directory and try:

```
"List my upcoming calendar events for this week."
```

If the MCP is configured correctly, the assistant will query your Google Calendar and return results.

### 4. Install Python Dependencies

Required for the `generate-vault-index` skill:

```bash
pip install python-frontmatter python-dotenv
```

### 5. Verify Setup

Run this checklist in Claude Code:

```
"Run the generate-vault-index skill."
```

If everything is configured correctly, the script will scan your vault and generate `_vault_index.md`. If your vault is empty, it will report zero files found (that's fine -- you'll populate it as you work).

---

## Project Structure

```
sa-assistant-agent/
|
|-- CLAUDE.md                         # System instructions for Claude Code
|-- GEMINI.md                         # System instructions for Gemini CLI
|-- AGENTS.md                         # Agent persona architecture & data strategy
|-- SKILLS.md                         # Skills registry (list of all available skills)
|
|-- account-strategist.agent.md       # Persona: strategic account advisor
|
|-- process-notes.skill.md            # Skill: structure raw meeting notes
|-- analyze-emails.skill.md           # Skill: analyze Gmail threads
|-- schedule-tasks.skill.md           # Skill: create calendar focus sessions
|-- generate-vault-index.skill.md     # Skill: validate and index the vault
|
|-- scripts/
|   |-- generate_vault_index.py       # Python: vault indexer & validator
|
|-- rh-docs-downloader/
|   |-- SKILL.md                      # Skill definition
|   |-- scripts/
|       |-- download_rh_docs.js       # Node.js: Puppeteer-based PDF downloader
|       |-- package.json              # Dependencies (puppeteer)
|
|-- .env.example                      # Environment template
|-- .env                              # Your local config (gitignored)
|-- .claude/
|   |-- settings.local.json           # Claude Code permissions (gitignored)
|-- .gitignore
|-- README.md                         # This file
```

### Key Files Explained

| File | Format | Purpose |
|---|---|---|
| `CLAUDE.md` | Markdown | Loaded automatically by Claude Code as system instructions. Defines vault conventions, operational workflows, and data privacy rules. |
| `AGENTS.md` | Markdown | Defines the data strategy (Obsidian vs. Google Workspace roles) and lists available agent personas. |
| `SKILLS.md` | Markdown | Registry of all skills with short descriptions and invocation examples. |
| `*.agent.md` | Markdown | Each file defines a persona the assistant can adopt when asked (e.g., "Act as the Account Strategist"). |
| `*.skill.md` | Markdown | Each file defines a step-by-step procedure the assistant follows when you invoke the skill by name. |

---

## Concepts

### Agents vs. Skills

**Agents** define a *persona* -- a role with specific expertise, tone, and priorities. When you say "Act as the Account Strategist," the assistant adopts that agent's perspective.

**Skills** define a *procedure* -- a repeatable workflow with defined inputs, steps, and output format. When you say "Run the process-notes skill," the assistant follows that skill's instructions step by step.

You can combine them: "As the Account Strategist, analyze my emails with Acme Corp."

### Data Strategy: Obsidian vs. Google Workspace

The system enforces a clear boundary between where data lives and why:

| | Obsidian | Google Workspace |
|---|---|---|
| **Role** | Primary Brain -- knowledge, records, context | Collaboration Output -- sharing, cooperation |
| **Audience** | You (internal) | Team, colleagues, customers |
| **Organization** | Properties, categories, wikilinks, dashboards | Simple folders by purpose |
| **Lifecycle** | Long-term, constantly updated | Per-document snapshots |
| **What goes here** | Meeting notes, account blueprints, tasks, strategy | Shared docs, presentations, emails |

The assistant reads from Google Workspace (emails, docs, calendar) and writes primarily to Obsidian. It never stores customer data in this git repository.

---

## Skills Reference

### process-notes

**Purpose:** Transform raw meeting notes into structured documentation.

**Invoke:** `"Run the process-notes skill on [path/to/file]"` or `"Process my meeting notes from the call with Acme Corp."`

**Input:** A markdown file path (Obsidian note) or raw text from a Google Doc.

**Output sections:**
1. Executive Summary (2-3 sentences)
2. Technical Requirements (products, architecture, constraints)
3. Business Drivers (pain points, timelines, competitive pressure)
4. Stakeholder Insights (decision makers, influencers, blockers)
5. Action Items (assigned to you and to the customer)
6. Suggested Account Plan updates

**Conventions enforced:**
- Adds/validates required frontmatter (`date`, `company`, `participants`, `type`, `summary`, `tags`)
- Uses canonical company names as wikilinks
- Writes summary in English even if source notes are in Czech/Slovak
- Flags Red Hat products mentioned and any competitive risks

---

### analyze-emails

**Purpose:** Scan Gmail threads to extract initiatives, action items, and stalled conversations.

**Invoke:** `"Analyze my emails with Acme Corp"` or `"Run the analyze-emails skill for the migration project."`

**Requires:** Gmail MCP connected.

**Output:** An Email Intelligence Report with four sections:
- **Active Initiatives** -- projects currently moving forward
- **Stalled/Forgotten Items** -- unanswered questions, threads that went cold
- **Pending Action Items (Yours)** -- things you promised to do
- **Waiting On (Others)** -- things you're waiting for from the customer

**Timeframe:** Last 3-6 months by default (configurable).

---

### schedule-tasks

**Purpose:** Find free time on your Google Calendar and create focus blocks linked to Obsidian notes.

**Invoke:** `"Block 90 minutes on Monday for Acme Corp preparation"` or `"When can I work on the migration proposal?"`

**Requires:** Google Calendar MCP connected.

**Constraints:**
- Only schedules within **08:30 - 17:00** work hours.
- Default duration: 60 minutes (override by specifying).
- Avoids back-to-back conflicts.
- If no slot is found on the requested day, proposes the next available day.

**Output:** A Google Calendar event titled `Focus: [Task Name]` with an `obsidian://open?vault=...&file=...` deep link in the description. Clicking the link in Calendar opens the relevant note directly in Obsidian.

---

### generate-vault-index

**Purpose:** Regenerate vault indexes and validate frontmatter consistency.

**Invoke:** `"Run the generate-vault-index skill"` or `"Check my vault consistency."`

**Requires:** Python 3 with `python-frontmatter` and `python-dotenv`.

**What it does:**
1. Runs `scripts/generate_vault_index.py`
2. Scans all files in `Accounts/`, `Meetings/`, and `Tasks/`
3. Generates `_vault_index.md` (statistics and file index) and `_stakeholder_map.md` (relationship map)
4. Reports warnings for:
   - Company names that don't match any Account Blueprint
   - Missing required frontmatter fields (`date`, `company`, `type`)
   - Placeholder values in task files
   - Invalid date formats

**When to run:**
- Before account reviews or strategy sessions
- After processing a batch of meeting notes
- Periodically to catch drift in vault quality

---

### rh-docs-downloader

**Purpose:** Batch-download all PDF guides for a Red Hat product version.

**Invoke:** `"Download the Red Hat OpenShift AI 3.4 documentation."`

**First-time setup:**
```bash
cd rh-docs-downloader/scripts
npm install
```

**How it works:** Uses Puppeteer to navigate the Red Hat docs site, extract PDF URLs for all guides in a product version, and download them via `wget`.

**Example:**
```bash
node rh-docs-downloader/scripts/download_rh_docs.js \
  "https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4" \
  "RedHat_Docs/OpenShift_AI_3.4_PDFs"
```

---

## Vault Schema

This section describes the frontmatter conventions the assistant enforces. Following these conventions is what makes the vault machine-readable -- dashboards, the vault index generator, and the assistant's search all depend on consistent frontmatter.

### Folder Layout

```
SA_Knowledge/
  Accounts/          # One file per customer (Account Blueprint)
  Meetings/          # One file per meeting
  Tasks/             # One file per task or follow-up
  Atlas/             # Dashboards, indexes, vault map
```

### Meeting Notes

**Location:** `SA_Knowledge/Meetings/`
**Naming:** `YYYY-MM-DD Company Topic.md` (recommended, not enforced)

**Required frontmatter:**

```yaml
---
date: 2025-06-15
company: "[[Acme_Corp]]"
participants: "[[John Doe]], [[Jane Smith]]"
type: sync
summary: "Discussed migration timeline and blockers for Q3 rollout"
tags: [openshift, migration]
---
```

**Field details:**

| Field | Type | Rules |
|---|---|---|
| `date` | Date | `YYYY-MM-DD` format (dashes, never slashes) |
| `company` | Wikilink | Must use a canonical company name: `"[[Acme_Corp]]"` |
| `participants` | Wikilink list | Comma-separated wikilinks to attendee names |
| `type` | String | One of: `sync`, `workshop`, `discovery`, `qbr`, `review`, `escalation`, `prep`, `internal`, `demo` |
| `summary` | String | Single English sentence, max 120 characters. English even if notes are in Czech/Slovak. |
| `tags` | List | Free-form tags for products, topics, or themes |

**Meeting type definitions:**

| Type | When to use |
|---|---|
| `sync` | Regular status call or check-in |
| `workshop` | Hands-on technical session |
| `discovery` | Initial requirements gathering |
| `qbr` | Quarterly business review |
| `review` | Architecture or design review |
| `escalation` | Issue escalation or crisis call |
| `prep` | Internal preparation for a customer meeting |
| `internal` | Internal team discussion (no customer present) |
| `demo` | Product demonstration |

### Account Blueprints

**Location:** `SA_Knowledge/Accounts/`
**Naming:** `Company_Name.md` (matches canonical name)

**Typical frontmatter:**

```yaml
---
Industry: "Telecommunications"
Account Tier: "Strategic"
Status: "Active"
Primary SA: "Your Name"
Last Updated: 2025-06-15
region: "CZ"
segment: "Enterprise"
GDrive Folder: "1aBcDeFgHiJkLmNoPqRsTuVwXyZ"
---
```

The `GDrive Folder` field is important -- the assistant uses it to scope Google Drive searches to the correct customer folder instead of searching your entire Drive.

### Task Notes

**Location:** `SA_Knowledge/Tasks/`

**Required frontmatter:**

```yaml
---
status: open
customer: "[[Acme_Corp]]"
project: "[[Cloud Migration]]"
priority: "High"
due_date: 2025-07-01
---
```

**Status values:** Only use `open`, `in-progress`, `blocked`, `done`, or `cancelled`. Obsidian Bases dashboards filter on these exact values. A missing status field is treated as `open`.

### Canonical Company Names

Every company referenced in frontmatter must use a consistent, canonical name. This is critical -- the vault index generator, search, and dashboards all depend on exact matches.

Define your canonical names in `CLAUDE.md` under the "Canonical Company Names" section. Use underscore-separated names without spaces:

```
Good: [[Acme_Corp]], [[Beta_Industries]], [[Gamma_Tech]]
Bad:  [[Acme Corp]], [[acme-corp]], [[ACME]], [[Acme Corporation]]
```

When you fork this project, replace the example company names in `CLAUDE.md` with your own accounts. The `generate-vault-index` skill validates all company references against this list.

### Tags, Properties, and Categories

**When to use each:**

| Mechanism | Purpose | Example |
|---|---|---|
| **Frontmatter properties** | Structured, queryable fields that dashboards and scripts depend on. Use for status, date, company, type. | `status: open`, `type: sync` |
| **Tags** | Lightweight labels for topics, products, or themes. Free-form. Used for filtering in Obsidian search and Bases. | `tags: [openshift, migration, rhel]` |
| **Wikilinks** | Connections between notes. Used for company names, participant names, and project references. Creates navigable relationships in Obsidian's graph view. | `company: "[[Acme_Corp]]"` |
| **Folders** | Broad categorization by note type. Don't over-nest. | `Meetings/`, `Tasks/`, `Accounts/` |

**Tag conventions:**
- Use lowercase, hyphen-separated tags: `cloud-migration`, not `Cloud Migration`
- Product tags match Red Hat naming: `openshift`, `rhel`, `ansible`, `aap`
- Use `tags:` (list format) in frontmatter, not inline `#tags` in body text -- this makes them queryable by Bases

---

## Customizing for Your Accounts

To adapt this project for your own accounts:

1. **Edit `CLAUDE.md`** -- replace the canonical company names under "Canonical Company Names" with your own accounts. Use underscore-separated names.

2. **Update the company list in `scripts/generate_vault_index.py`** -- the `CANONICAL_ACCOUNTS` set must match what's in `CLAUDE.md`.

3. **Adjust meeting types** (if needed) -- the default list covers most SA workflows. Add new types in `CLAUDE.md` and `generate_vault_index.py` if your workflow requires them.

4. **Create Account Blueprints** -- for each customer, create a file in `SA_Knowledge/Accounts/` with the frontmatter schema above. The `GDrive Folder` field is optional but enables scoped Drive searches.

5. **Set your working hours** -- the default is 08:30-17:00. Adjust in `AGENTS.md` and `schedule-tasks.skill.md` if yours differ.

---

## Usage Examples

Start Claude Code in the project directory:

```bash
cd sa-assistant-agent
claude
```

Then interact naturally:

```
# Process meeting notes
"Process the notes from today's sync with Acme Corp -- the file is at
SA_Knowledge/Meetings/2025-06-15 Acme Corp sync.md"

# Analyze emails
"Go through my recent emails with Beta Industries and tell me
what's stalled or needs follow-up."

# Schedule focus time
"Block 2 hours on Wednesday afternoon to work on the Gamma Tech
architecture proposal."

# Validate vault
"Run the generate-vault-index skill and show me any issues."

# Strategic analysis (using the Account Strategist agent)
"As the Account Strategist, analyze the last 3 months of meeting notes
for Acme Corp and identify the top technical blockers."

# Download documentation
"Download the RHEL 10 documentation as PDFs."
```

---

## Troubleshooting

### "MCP not available" or Google Workspace tools not working

- Verify `.claude/settings.json` contains the `mcpServers` block with correct `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`.
- Re-run `npx -y @a-bonus/google-docs-mcp auth` to refresh the OAuth token.
- Check that the required Google APIs are enabled in your Google Cloud Console project.

### "SA_KNOWLEDGE_PATH not set" or vault files not found

- Ensure `.env` exists in the project root (copy from `.env.example`).
- The path should point to the vault root (the directory that contains `SA_Knowledge/`), not to `SA_Knowledge/` itself.
- Use an absolute path, not a relative one.

### generate-vault-index fails with import errors

```bash
pip install python-frontmatter python-dotenv
```

### Vault index reports warnings about company names

- Company names in meeting note frontmatter must exactly match the canonical names defined in `CLAUDE.md`.
- Common issues: spaces instead of underscores (`Acme Corp` vs `Acme_Corp`), missing wikilink brackets, typos.
- The warning message includes the file path and the incorrect value -- fix the frontmatter directly.

### rh-docs-downloader fails

- Run `cd rh-docs-downloader/scripts && npm install` to install Puppeteer.
- Ensure `wget` is available on your system (most Linux distributions include it; on macOS, install via `brew install wget`).
- Puppeteer needs Chromium -- on headless servers, you may need to install system dependencies (`apt install chromium-browser` or similar).

---

## Security and Privacy

- **No customer data in this repo.** The repository contains only agent configuration, skill definitions, and processing scripts. All account-specific content lives in your Obsidian vault (`$SA_KNOWLEDGE_PATH`), which is gitignored.
- **Credentials stay local.** The `.env` file and `.claude/` directory are gitignored. Google OAuth tokens are stored in `~/.config/google-docs-mcp/token.json` on your local machine and never leave it.
- **MCP runs locally.** The `@a-bonus/google-docs-mcp` server runs on your machine and communicates directly with Google APIs. No third party sees your credentials or data.
- **Need-to-know output.** The assistant is instructed to never output raw customer data unless explicitly asked. Czech/Slovak content is translated to English for reports while preserving technical accuracy.
