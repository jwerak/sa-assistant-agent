---
name: schedule-tasks
description: >
  Bridge Obsidian tasks to Google Calendar by creating focus session events with obsidian://
  deep links. Use when asked to schedule time, block calendar for a task, or find available
  slots for focused work.
---

# Skill: schedule-tasks

## Trigger
- "Schedule time for..."
- "Block my calendar to work on..."
- "When can I work on [Task/Project]?"

## Workflow
1. **Context Discovery:** Identify the source file in Obsidian (Account Atlas, Project note, or Daily Note).
2. **Availability Check:** Query Google Calendar for a free slot on the requested day.
3. **Constraint Validation:**
    - Slots must be between **08:30 and 17:00**.
    - Avoid back-to-back conflicts if possible.
4. **Execution:**
    - Create the Google Calendar event.
    - Title format: `Focus: [Task Name]`.
    - **Crucial:** Generate and insert an `obsidian://open?vault=...&file=...` deep link into the event description.
5. **Confirmation:** Report the scheduled time and provide the calendar link to the user.

## Instructions
- If the user doesn't specify a duration, default to **60 minutes**.
- If no slot is found within the 08:30-17:00 window, propose the next available day rather than scheduling outside the window.
