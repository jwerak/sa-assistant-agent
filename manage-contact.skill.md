# Skill: manage-contact

## Objective
To create or update Contact notes in the Obsidian vault with a dynamic Interactions section powered by Obsidian Bases, ensuring every contact automatically displays all meetings they participated in.

## Inputs
- **Name** (required): Full name of the contact.
- **Company** (required): Canonical account or partner name (see CLAUDE.md / `_VAULT_MAP.md`).
- **Role, email, phone, linkedin** (optional): Contact metadata.
- **Context** (optional): Free-text notes about the person (signals, background, relationships).

## Workflow Steps

### 1. Resolve Vault Path
Read `SA_KNOWLEDGE_PATH` from `.env`. All files go under `$SA_KNOWLEDGE_PATH/SA_Knowledge/`.

### 2. Derive Filename
Convert the contact name to a vault-safe filename: `Firstname_Lastname` (no diacritics in filename, underscores for spaces). Example: `Jan Paleček` → `Jan_Palecek.md`.

### 3. Create or Update the Contact Note
Place the file in `Contacts/`. Use this template:

```yaml
---
name: <Full Name with diacritics>
company: "[[Canonical_Name]]"
role: <job title>
email: <email>
phone: "<phone with country code>"
linkedin: <url>
type: contact
status: active
last_seen: YYYY-MM-DD
tags:
  - contact
  - sa-knowledge
---
```

Body structure (in Czech by default per vault conventions):

```markdown
# <Full Name>

<Brief role description and organizational context. Link related contacts with [[Name]] wikilinks.>

## Key Signals

- <Notable observations, sentiment, technical focus areas>

## Interactions

![[<Filename_without_ext>_Meetings.base]]
```

### 4. Create the Meetings Base File
Place the `.base` file in `Contacts/_bases/`. Filename: `<Filename_without_ext>_Meetings.base`.

Content:

```yaml
filters:
  and:
    - file.tags.contains("meeting")
    - participants.contains("<Filename_without_ext>")
views:
  - type: table
    name: Interactions
    order:
      - date
      - file.name
      - company
      - type
      - summary
    sort:
      - property: date
        direction: DESC
    columns:
      - property: date
        width: 120
      - property: file.name
        header: Meeting
        width: 300
      - property: company
        width: 150
      - property: type
        width: 100
      - property: summary
        width: 350
```

The `participants.contains()` filter matches on the contact's filename (without extension), which corresponds to how meeting notes reference participants: `participants: ["[[Contact_Filename]]"]`.

### 5. Verify Linkability
Confirm that meeting notes in `Meetings/` use `[[<Filename_without_ext>]]` in their `participants` frontmatter. If the contact name uses a different spelling in existing meetings, flag it for the user.

## Rules
- **Never** create static interaction lists. Always use the `.base` embed for dynamic meeting tracking.
- **Never** use `customer:` in frontmatter — always `company:`.
- **Always** create both the contact `.md` and the corresponding `_Meetings.base` file together.
- **Base file location:** `Contacts/_bases/` — keep base files separate from contact notes.
- The `## Interactions` section must contain only the `![[..._Meetings.base]]` embed, nothing else.
- If updating an existing contact that has a static Interactions list, replace it with the base embed.
