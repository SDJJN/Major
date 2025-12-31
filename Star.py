import os
import subprocess
import re
import time

# Create a folder to store videos
DOWNLOAD_DIR = "only_for_love_videos"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# List of Dailymotion URLs
video_links = [ 
    "https://dai.ly/k5R7RI8LoSWDFLBIaVe", # ep 32
    "https://dai.ly/k1puKxLIdcnecGBIaVc", # ep 33
    "https://dai.ly/k6n0REub0DHTmVBIaVk", # ep 34
]
   
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name).strip()

def get_video_title(url):
    try:
        result = subprocess.run(
            ["yt-dlp", "--get-title", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60
        )
        title = result.stdout.strip()
        return sanitize_filename(title)
    except Exception as e:
        print(f"[❌] Failed to get title: {e}")
        return None

def download_video(url, title):
    filepath = os.path.join(DOWNLOAD_DIR, f"{title}.mp4")
    print(f"   📥 Downloading as: {filepath}")
    try:
        subprocess.run([
            "yt-dlp",
            "-f", "best",
            "--concurrent-fragments", "30",   # High concurrency
            "--hls-prefer-native",
            "-o", filepath,
            url
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[❌] Download failed: {e}")
        return False

def main():
    total = len(video_links)
    success = 0
    start_all = time.time()

    print(f"\n📺 Starting batch download of {total} Dailymotion videos...\n")

    for i, url in enumerate(video_links, start=1):
        print("=" * 60)
        print(f"[{i}/{total}] 🎬 Processing URL:\n   {url}")

        start = time.time()
        title = get_video_title(url)

        if not title:
            print("[⚠️] Skipping: could not fetch title.\n")
            continue

        print(f"   📄 Title: {title}")
        result = download_video(url, title)

        elapsed = time.time() - start
        if result:
            print(f"✅ Completed in {elapsed:.1f}s")
            success += 1
        else:
            print(f"❌ Failed after {elapsed:.1f}s")

    total_elapsed = time.time() - start_all
    print("\n" + "=" * 60)
    print(f"🎉 Finished downloading. Success: {success}/{total} | Time: {total_elapsed:.1f}s")
    print(f"📁 Files saved to: {os.path.abspath(DOWNLOAD_DIR)}\n")

if __name__ == "__main__":
    main()
