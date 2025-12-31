const puppeteer = require('puppeteer');
const { exec, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const archiver = require('archiver');

const TARGET_URL = 'https://www.starfilx.in/love-is-sweet-hindi-dubbed-starfilx-complete-add-gdrive/';
const DOWNLOAD_DIR = path.resolve(__dirname, 'downloads');
const ZIP_OUTPUT = path.resolve(__dirname, 'videos.zip');

// Decoding function based on how the site encodes URLs
function decodeAppUrl(encoded) {
  try {
    const binaryString = Buffer.from(encoded, 'base64').toString('latin1');
    const percentEncodedStr = binaryString.split('')
      .map(c => '%' + c.charCodeAt(0).toString(16).padStart(2, '0'))
      .join('');
    return decodeURIComponent(percentEncodedStr);
  } catch (e) {
    console.error('Failed to decode app URL:', e);
    return null;
  }
}

function execPromise(cmd) {
  return new Promise((resolve, reject) => {
    exec(cmd, (error, stdout, stderr) => {
      if (error) reject(error);
      else resolve({ stdout, stderr });
    });
  });
}

async function getVideoTitle(videoUrl) {
  const cmd = `yt-dlp --get-title "${videoUrl}"`;
  try {
    const { stdout } = await execPromise(cmd);
    return stdout.trim();
  } catch (err) {
    console.error('Failed to get title:', err.message);
    return null;
  }
}

function sanitizeFilename(name) {
  return name.replace(/[/\\?%*:|"<>]/g, '-').substring(0, 100);
}

function downloadVideo(videoUrl, filename) {
  return new Promise((resolve, reject) => {
    const filepath = path.join(DOWNLOAD_DIR, filename + '.mp4');
    console.log(`\n[Download] Starting: "${filename}"`);

    const ytProcess = spawn('yt-dlp', [
      '-f', 'bestvideo+bestaudio',
      '--merge-output-format', 'mp4',
      '-o', filepath,
      '--newline',
      videoUrl,
    ]);

    ytProcess.stdout.on('data', (data) => {
      const line = data.toString().trim();
      if (line.startsWith('[download]')) {
        const progressMatch = line.match(/(\d+\.\d+)%/);
        if (progressMatch) {
          process.stdout.write(`\r[Download Progress] ${progressMatch[1]}%`);
        }
      }
    });

    ytProcess.stderr.on('data', (data) => {
      // Optional: log errors if needed
    });

    ytProcess.on('close', (code) => {
      process.stdout.write('\n');
      if (code === 0) {
        console.log(`[Download] Completed: "${filename}"`);
        resolve(filepath);
      } else {
        reject(new Error(`yt-dlp exited with code ${code}`));
      }
    });
  });
}

async function createZipFromFiles(files, outputZipPath) {
  return new Promise((resolve, reject) => {
    console.log(`\n[ZIP] Creating zip archive: ${outputZipPath}`);

    const output = fs.createWriteStream(outputZipPath);
    const archive = archiver('zip', { zlib: { level: 9 } });

    output.on('close', () => {
      console.log(`[ZIP] Archive created successfully, total size: ${(archive.pointer() / 1024 / 1024).toFixed(2)} MB`);
      resolve();
    });
    archive.on('error', (err) => reject(err));

    archive.on('progress', (progress) => {
      process.stdout.write(`\r[ZIP] Processed files: ${progress.entries.processed}/${progress.entries.total}`);
    });

    archive.pipe(output);
    files.forEach((file) => {
      const nameInZip = path.basename(file);
      archive.file(file, { name: nameInZip });
    });
    archive.finalize();
  });
}

(async () => {
  if (!fs.existsSync(DOWNLOAD_DIR)) {
    fs.mkdirSync(DOWNLOAD_DIR);
  }

  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();

  console.log(`[Browser] Navigating to ${TARGET_URL}`);
  await page.goto(TARGET_URL, { waitUntil: 'networkidle2' });

  // Grab all Terabox links and remove duplicates
  const allLinks = await page.evaluate(() => {
    const anchors = Array.from(document.querySelectorAll('a[href*="teraboxlinks.com/full"]'));
    const hrefs = anchors.map(a => a.href.trim()).filter(href => href.length > 0);
    return [...new Set(hrefs)]; // Deduplicate
  });

  // ✅ Filter only even-numbered (1-based: 2nd, 4th, etc.)
  const teraboxLinks = allLinks.filter((_, index) => (index + 1) % 2 === 0);

  console.log(`[Browser] Found ${teraboxLinks.length} even-numbered Terabox links.`);

  const downloadedFiles = [];

  for (const [index, link] of teraboxLinks.entries()) {
    console.log(`\n[${index + 1}/${teraboxLinks.length}] Processing link: ${link}`);

    const urlObj = new URL(link);
    const encodedUrl = urlObj.searchParams.get('url');
    if (!encodedUrl) {
      console.error('[Error] No "url" param found in the link.');
      continue;
    }

    const videoUrl = decodeAppUrl(encodedUrl);
    if (!videoUrl) {
      console.error('[Error] Failed to decode video URL.');
      continue;
    }

    console.log(`[Decoded URL] ${videoUrl}`);

    const title = await getVideoTitle(videoUrl);
    if (!title) {
      console.error('[Error] Failed to get title.');
      continue;
    }

    const safeTitle = sanitizeFilename(title);

    try {
      const downloadedFile = await downloadVideo(videoUrl, safeTitle);
      downloadedFiles.push(downloadedFile);
    } catch (e) {
      console.error(`[Error] Failed to download video "${safeTitle}":`, e.message);
    }
  }

  await browser.close();

  if (downloadedFiles.length > 0) {
    await createZipFromFiles(downloadedFiles, ZIP_OUTPUT);
    // Optional cleanup:
    // downloadedFiles.forEach(f => fs.unlinkSync(f));
    // console.log('[Cleanup] Removed individual video files.');
  } else {
    console.log('[Result] No videos downloaded, zip not created.');
  }
})();
