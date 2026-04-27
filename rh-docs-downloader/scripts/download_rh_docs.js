const puppeteer = require('puppeteer');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
if (args.length < 1) {
    console.error("Usage: node download_rh_docs.js <base_url> [target_directory]");
    process.exit(1);
}

const baseUrl = args[0];
const targetDir = path.resolve(args[1] || './RedHat_Docs');

(async () => {
    console.log(`Starting Red Hat Docs Downloader`);
    console.log(`Base URL: ${baseUrl}`);
    console.log(`Target Directory: ${targetDir}`);
    
    // Create target directory if it doesn't exist
    if (!fs.existsSync(targetDir)){
        fs.mkdirSync(targetDir, { recursive: true });
    }

    const browser = await puppeteer.launch({ headless: "new", args: ['--no-sandbox', '--disable-setuid-sandbox'] });
    const page = await browser.newPage();
    
    console.log("Navigating to main documentation page...");
    try {
        await page.goto(baseUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
        await new Promise(r => setTimeout(r, 3000));
    } catch (e) {
        console.error(`Failed to navigate to base URL: ${e.message}`);
        await browser.close();
        process.exit(1);
    }
    
    // Extract version identifier from URL (e.g. "3.4") to filter links
    const urlParts = baseUrl.split('/').filter(p => p.length > 0);
    const versionPart = urlParts[urlParts.length - 1]; 
    
    // Extract all guide URLs from the page
    const guideUrls = await page.evaluate((version) => {
        const anchors = Array.from(document.querySelectorAll('a'));
        const hrefs = anchors.map(a => a.href);
        // Filter out links that are part of the documentation under this version
        return Array.from(new Set(hrefs.filter(h => h.includes(`/${version}/html/`) || h.includes(`/${version}/html-single/`))));
    }, versionPart);
    
    console.log(`Found ${guideUrls.length} guide URLs. Extraction starting...`);
    
    const pdfLinks = [];
    
    for (const url of guideUrls) {
        console.log(`Visiting ${url}...`);
        try {
            await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
            
            // Red Hat Docs are Nuxt apps. The PDF URL is often hidden in the __NUXT__ state object
            const pdfUrl = await page.evaluate(() => {
                if (window.__NUXT__) {
                    const stateStr = JSON.stringify(window.__NUXT__);
                    const match = stateStr.match(/https:[^"]*\.pdf/i);
                    if (match) return match[0];
                }
                
                // Fallback: look for an anchor tag
                const pdfAnchor = Array.from(document.querySelectorAll('a')).find(a => a.innerText.toLowerCase().includes('pdf') || a.href.toLowerCase().endsWith('.pdf'));
                return pdfAnchor ? pdfAnchor.href : null;
            });
            
            if (pdfUrl) {
                console.log(` -> Found PDF: ${pdfUrl}`);
                pdfLinks.push(pdfUrl);
            } else {
                console.log(` -> No PDF link found on page or in Nuxt state.`);
            }
        } catch (e) {
            console.error(` -> Failed to visit ${url}: ${e.message}`);
        }
    }
    
    await browser.close();
    
    // remove duplicates just in case
    const uniquePdfs = Array.from(new Set(pdfLinks));
    
    if (uniquePdfs.length === 0) {
        console.log("No PDF links were found.");
        process.exit(0);
    }

    console.log(`\nFound ${uniquePdfs.length} PDFs. Starting download to ${targetDir}...`);
    
    const listFilePath = path.join(targetDir, 'pdf_urls.txt');
    fs.writeFileSync(listFilePath, uniquePdfs.join('\n'));
    
    try {
        console.log("Downloading files via wget...");
        execSync(`wget -q --show-progress -c -i "${listFilePath}" -P "${targetDir}"`, { stdio: 'inherit' });
        console.log("All downloads completed successfully.");
    } catch (error) {
        console.error("Some downloads may have failed. Please check the target directory and the pdf_urls.txt file.");
    }
})();
