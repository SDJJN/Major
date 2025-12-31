import gdown
import os

# List of tuples (Episode number, Google Drive URL)
data = [
    (1, "https://drive.google.com/file/d/1VZw1zLGtqyOwaCZEdcBe2piaMvIVj-E7/preview"),
    (2, "https://drive.google.com/file/d/1-Qt0BiIWn1rbOVrmrdLlt8hG4USnLNQY/preview"),
    (3, "https://drive.google.com/file/d/1p7Gu9QmIh_YrGZU65ZayMEbDWKPTHlHt/preview"),
    (4, "https://drive.google.com/file/d/1dii4Z5stAXJXAZe2uZ17z6dzl1NPJvpD/preview"),
    (5, "https://drive.google.com/file/d/1IH8sqprmRsZjBtERtUGta7gf4K-W3G6H/preview"),
    (6, "https://drive.google.com/file/d/11gXQaatp-G_M3V3ka_hrbC5TW8eY91SK/preview"),
    (7, "https://drive.google.com/file/d/1Sc4M5qMp0mt9iZtMcI8VyH83TeifANwv/preview"),
    (8, "https://drive.google.com/file/d/1gZ3hw92hpkROR-EUXMwG7SL7TrOLLuQH/preview"),
    (9, "https://drive.google.com/file/d/1UxfXUdtkkN0Fjr0rDTi5W5vmNV5eA-zT/preview"),
    (10, "https://drive.google.com/file/d/1GkkKqT0spUFFUibC_vOYlmwsw15Y82aP/preview"),
    (11, "https://drive.google.com/file/d/1Q7yU8A_FZc2fZNSY1L4J72YclwAx6Xqy/preview"),
    (12, "https://drive.google.com/file/d/1kV-TIpO-aa4y0V3TzJiVzJ2BlyYD6ble/preview"),
    (13, "https://drive.google.com/file/d/1arMiPM_4YAoq_WYhumErerjm5wLXoCmE/preview"),
    (14, "https://drive.google.com/file/d/1xf9q9eL7fL93vLZCbUE3Yu85G5caWtec/preview"),
    (15, "https://drive.google.com/file/d/1DqacPCOEzuN6dyLvWedhapHnBUXmHwzg/preview"),
    (16, "https://drive.google.com/file/d/1axT_nhyjr5zS0tLHCK3pfHXV73Z1F6vd/preview")
]



# Download all episodes
for ep_num, url in data:
    file_id = url.split("/d/")[1].split("/")[0]
    direct_url = f"https://drive.google.com/uc?id={file_id}"
    output_filename = f"Episode{ep_num}.mp4"
    
    if os.path.exists(output_filename):
        print(f"[✓] Episode {ep_num} already exists. Skipping...")
        continue

    print(f"⬇️  Downloading Episode {ep_num}...")
    try:
        gdown.download(direct_url, output_filename, quiet=False)
        print(f"[✔] Episode {ep_num} downloaded successfully!\n")
    except Exception as e:
        print(f"[✘] Failed to download Episode {ep_num}: {e}\n")
