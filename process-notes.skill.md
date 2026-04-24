# Skill: process-notes

## Objective
To transform raw, messy meeting notes into high-quality, actionable documentation for a Solutions Architect.

## Inputs
- A file path to a markdown note (Obsidian) or a text dump from a Google Doc.
- (Optional) A specific customer name for context.

## Workflow Steps
1. **Analyze:** Identify participants, date, and the primary objective of the meeting.
2. **Categorize:** Extract information into the following sections:
    - **Executive Summary:** 2-3 sentences on the "big picture."
    - **Technical Requirements:** Specific tools, architectural constraints, or performance needs mentioned.
    - **Business Drivers:** The "Why" - pain points, timelines, or competitive pressures.
    - **Stakeholder Insights:** New info about who makes decisions or technical influencers.
    - **Action Items:** Clearly assigned tasks for the SA and for the Customer.
3. **Draft Updates:** Suggest specific updates to the "Account Plan" based on this new information.

## Instructions
- Maintain technical accuracy. If a specific Google Cloud product is mentioned (e.g., BigQuery, GKE), ensure it is highlighted in the Technical Requirements.
- If notes are in Czech/Slovak, provide the summary in English but keep technical terms as used in the meeting.
- Flag any "Red Flags" or risks (e.g., a competitor being mentioned or a missed deadline).
