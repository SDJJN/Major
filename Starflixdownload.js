const puppeteer = require('puppeteer');

const TARGET_URL = 'https://www.starfilx.in/love-is-sweet-hindi-dubbed-starfilx-complete-add-gdrive/';

// Decoding function for terabox links with base64 encoded 'url' param
function decodeAppUrl(encoded) {
  try {
    const binaryString = Buffer.from(encoded, 'base64').toString('latin1');
    const percentEncodedStr = binaryString.split('')
      .map(c => '%' + c.charCodeAt(0).toString(16).padStart(2, '0'))
      .join('');
    return decodeURIComponent(percentEncodedStr);
  } catch (e) {
    console.error('❌ Failed to decode app URL:', e);
    return null;
  }
}

(async () => {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();

  console.log(`[🌐] Navigating to: ${TARGET_URL}`);
  await page.goto(TARGET_URL, { waitUntil: 'domcontentloaded' });

  const links = await page.evaluate(() => {
    const anchorTags = Array.from(document.querySelectorAll('a'));
    return anchorTags.map(a => ({
      href: a.href,
      text: a.textContent.trim()
    }));
  });

  await browser.close();

  const teraboxLinks = links.filter(l => l.href.includes('teraboxapp.com') || l.href.includes('teraboxlinks.com'));
  const gdriveLinks = links.filter(l => l.href.includes('drive.google.com'));

  console.log(`\n🔗 Found ${teraboxLinks.length} Terabox links`);
  teraboxLinks.forEach((link, i) => {
    try {
      const urlObj = new URL(link.href);
      const encodedUrl = urlObj.searchParams.get('url');
      const decoded = decodeAppUrl(encodedUrl);
      console.log(`\n[${i + 1}] ${link.text}\n➡️ Encoded: ${link.href}\n✅ Decoded: ${decoded || 'Invalid or not decodable'}`);
    } catch (err) {
      console.log(`\n[${i + 1}] ${link.text}\n❌ Failed to parse Terabox link`);
    }
  });

  console.log(`\n📁 Found ${gdriveLinks.length} Google Drive links`);
  gdriveLinks.forEach((link, i) => {
    console.log(`\n[${i + 1}] ${link.text}\n➡️ ${link.href}`);
  });

})();
