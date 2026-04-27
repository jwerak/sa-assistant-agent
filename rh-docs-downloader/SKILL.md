---
name: rh-docs-downloader
description: Downloads Red Hat documentation as PDFs when given a base URL. Use this skill when the user asks to download Red Hat product documentation.
---

# Red Hat Docs Downloader

This skill uses a Puppeteer-based Node.js script to extract and download all PDF guides from a Red Hat product documentation base URL.

## Setup

Before running the script for the first time, ensure dependencies are installed:

```bash
cd <path-to-skill>/scripts
npm install
```

## Usage

To download documentation, run the `download_rh_docs.js` script with the base URL and an optional target directory.

```bash
node <path-to-skill>/scripts/download_rh_docs.js "<base_url>" [target_directory]
```

- `<base_url>`: The URL to the Red Hat documentation version page (e.g., `https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4`)
- `[target_directory]`: (Optional) The directory to save the downloaded PDFs. Defaults to `./RedHat_Docs`.

Example:

```bash
node <path-to-skill>/scripts/download_rh_docs.js "https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4" "OpenShift_AI_3.4_PDFs"
```

The script will automatically navigate the site, identify the available HTML guides, locate their corresponding PDF versions, and download them to the specified directory.
