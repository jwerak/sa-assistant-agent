---
name: analyze-emails
description: >
  Analyze recent email threads (via Gmail MCP) with a customer, account team, or stakeholder.
  Extracts active initiatives, pending action items, and stalled conversations needing follow-up.
  Use when asked to go through emails with a company/person or analyze email threads.
---

# Skill: analyze-emails

## Trigger
- "Go through my emails with [Company/Person]..."
- "Analyze my recent email threads about [Topic]..."
- "Run the `analyze-emails` skill for..."

## Workflow
1. **Search & Fetch:** Use the Gmail MCP to search for recent emails matching the user's criteria (e.g., domain:acme-corp.com, or specific keywords). Fetch the most recent and relevant threads (typically last 3-6 months unless specified otherwise).
2. **Analysis:** Read the threads specifically looking for:
   - **Active Initiatives:** Projects or technical discussions that are currently moving forward.
   - **SA Action Items:** Things the Solutions Architect explicitly promised to do, send, or research.
   - **Customer/Partner Action Items:** Things we are waiting for the customer or account team to provide.
   - **Stalled/Forgotten Items:** Questions asked that were never answered, or threads that abruptly stopped without a resolution.
3. **Redaction (Optional):** If requested, ensure no sensitive PII is included in the output.

## Output Format
Present the findings to the user in the following markdown structure. Do not save this directly to Obsidian unless the user asks you to append it to the Account Blueprint.

```markdown
### Email Intelligence Report: [Target/Company]

**Timeframe Analyzed:** [e.g., Last 3 months]

#### Active Initiatives
* **[Initiative Name]:** Brief summary of current status based on emails.
* **[Initiative Name]:** ...

#### Stalled or Forgotten Items
* **[Topic]:** You asked [Name] for [information] on [Date], but there was no reply. *Recommendation: Send a gentle follow-up.*
* **[Topic]:** Discussion about [Subject] ended without a clear next step.

#### Pending Action Items (Yours)
* [ ] Task you need to complete based on email promises.

#### Waiting On (Others)
* [Name]: Waiting for them to provide [X].
```
