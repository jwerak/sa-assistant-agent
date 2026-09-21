# Skill: rhdp-demo-search

## Objective
Search the Red Hat Demo Platform (RHDP) catalog for available demos, workshops, labs, and open environments. Match items by keyword, product family, category, or customer context. Return structured results with direct ordering links.

## Data Source
`/home/jveverka/git/sa-assistant-agent/rhdp_catalog_index.json`

This file contains 336 catalog items exported from `catalog.demo.redhat.com` (last export: 2026-09-21). Each item has: `id`, `title`, `description`, `category`, `productFamily`, `keywords`, `catalogUrl`.

## Inputs
- **Query** (required): Free-text search — a keyword (e.g. "virtualization", "AI", "ansible"), a product name (e.g. "OpenShift", "RHEL"), a category (e.g. "Demos", "Workshops"), or a customer-relevant topic (e.g. "migration from VMware").
- **Category filter** (optional): Restrict to: `Demos`, `Workshops`, `Labs`, `Open_Environments`, `Brand_Events`, `Other`.
- **Product family filter** (optional): Restrict to a specific product family (e.g. "Red Hat Ansible Automation Platform").
- **Max results** (optional, default: 15): Limit the number of results returned.

## Available Categories
| Category | Count | Description |
|---|---|---|
| Workshops | 114 | Hands-on multi-user workshops with guided labs |
| Other | 79 | Miscellaneous catalog items |
| Demos | 44 | Pre-built presenter-led demos |
| Labs | 40 | Self-paced individual learning labs |
| Brand_Events | 36 | Large-scale event assets (Summits, Roadshows) |
| Open_Environments | 23 | Blank cloud/cluster environments for custom use |

## Available Product Families (28)
Amazon Web Services, Automation Management, Future Technologies, GCP, InstructLab, Kasten, Microsoft Azure, Project Dance, Red Hat AI, Red Hat Ansible Automation Platform, Red Hat Connectivity Link, Red Hat Developer Hub, Red Hat Device Edge, Red Hat Enterprise Linux, Red Hat Lightspeed, Red Hat OpenShift Container Platform, Red Hat OpenShift Container Platform AI, Red Hat OpenShift Service Mesh, Red Hat Satellite, Red Hat Service Interconnect, Red Hat and IBM, Robot, SAP, Trilio, VMware, Validated Pattern, platform-engineering

## Workflow Steps

### 1. Load Catalog Index
```python
import json
with open('/home/jveverka/git/sa-assistant-agent/rhdp_catalog_index.json') as f:
    catalog = json.load(f)
```

### 2. Search Strategy
Search across these fields in order of relevance:
1. **Title** — exact or substring match (highest weight)
2. **Keywords** — comma-separated tags from the catalog item
3. **Product Family** — the Red Hat product or technology
4. **Description** — full-text search (lowest weight)
5. **Category** — filter, not ranked

When the user provides a customer name or topic instead of a direct keyword:
- Check the Obsidian vault (`$SA_KNOWLEDGE_PATH`) for their Account Blueprint to understand their tech stack
- Map their technology stack to relevant product families and keywords
- E.g. "VMware migration" → productFamily: "VMware" OR keywords: "virtualization, cnv, migration"
- E.g. "security" → keywords: "compliance, STIG, ACS, stackrox, RHACS"
- E.g. "AI/ML" → productFamily: "Red Hat AI" OR "InstructLab" OR "Red Hat OpenShift Container Platform AI"

### 3. Rank Results
Score each matching item:
- Title match: +10 points
- Keyword match: +5 points
- Product family match: +3 points
- Description match: +1 point
- Category match (when filtered): required (filter, not boost)

Sort by score descending. Apply max results limit.

### 4. Format Output

```markdown
## RHDP Demo Search: "<query>"

### Results (N matches)

| # | Title | Product Family | Category | Keywords |
|---|---|---|---|---|
| 1 | [Title](catalogUrl) | ... | Demo | ... |

### Recommended for <context>
<If a customer/company context was provided, add a section explaining which demos are most relevant to their specific use case and why>

### How to Order
1. Click the catalog link for the desired item
2. Log in with Red Hat SSO at [catalog.demo.redhat.com](https://catalog.demo.redhat.com)
3. Click "Order" and configure the deployment options
4. Most demos deploy in 30-60 minutes

### Catalog Freshness
Data exported: <exportDate>. To refresh, re-run the catalog scraping workflow using Playwright MCP against catalog.demo.redhat.com.
```

## Rules
- **Always** search the JSON index file — never guess or hallucinate demo names.
- When returning results, always include the direct `catalogUrl` link so the SA can order immediately.
- If the query returns zero results, suggest broadening the search or list the available product families and categories.
- When a customer/company context is provided, cross-reference with the Obsidian vault to tailor suggestions.
- Output commentary in **Czech** per vault conventions; demo titles and descriptions stay in English (as they are in the catalog).
- If the catalog index is older than 30 days, add a warning suggesting a refresh.
