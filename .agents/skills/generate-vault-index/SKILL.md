---
name: generate-vault-index
description: >
  Regenerate the auto-generated vault index files (_vault_index.md and _stakeholder_map.md)
  from vault frontmatter and report data consistency warnings. Use when asked to refresh the
  vault index, before strategy sessions, or after processing a batch of meeting notes.
---

# Skill: generate-vault-index

## Inputs
- None required. The script reads `$SA_KNOWLEDGE_PATH` from `.env`.

## Workflow Steps
1. **Run the generator:** Execute `python3 scripts/generate_vault_index.py` from the repo root.
2. **Read outputs:** Read the generated files:
   - `$SA_KNOWLEDGE_PATH/SA_Knowledge/_vault_index.md`
   - `$SA_KNOWLEDGE_PATH/SA_Knowledge/_stakeholder_map.md`
3. **Report warnings:** If the script exited with code 2, it found consistency issues. Parse the stderr output and report:
   - Company names that don't match any Account Blueprint
   - Missing required frontmatter fields (`date`, `company`, `type`)
   - Placeholder values in task files
4. **Suggest fixes:** For each warning, suggest the specific correction (e.g., "Change company from 'O2 CZ' to 'O2_CZ' in file X").

## When to Run
- Before strategy sessions or account reviews
- After processing a batch of meeting notes with `process-notes`
- When the user asks to refresh the vault index

## Dependencies
- Python 3 with `python-frontmatter`, `python-dotenv` packages
- `.env` file with `SA_KNOWLEDGE_PATH` configured

## Output
Report the vault statistics (accounts, meetings, tasks counts) and list any consistency warnings found.
