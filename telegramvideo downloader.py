import os
import asyncio
import aiohttp
import shutil
from fpdf import FPDF
from telegram import Bot
from telegram.ext import Updater, CommandHandler

# Set your bot token and channel name here
BOT_TOKEN = "AAHYJwOLeV7JQ7mU2k2SSNQ6OEYdq4mmMgM"
CHANNEL_NAME = "Codebasic - Gen AI & Data Science Bootcamp"

# Initialize the Telegram bot
bot = Bot(token=BOT_TOKEN)

# Set up an async function to download files concurrently
async def download_file(session, url, file_path):
    try:
        async with session.get(url) as response:
            with open(file_path, 'wb') as f:
                f.write(await response.read())
            print(f"Downloaded file to {file_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

async def download_files(update, context):
    async with aiohttp.ClientSession() as session:
        # Fetch messages from the Telegram channel
        messages = bot.get_chat_history(CHANNEL_NAME, limit=100)

        # Create a folder to store the downloaded files
        if not os.path.exists("downloaded_files"):
            os.makedirs("downloaded_files")

        # List of download tasks
        download_tasks = []

        for message in messages:
            if message.document:
                # If the message has a document, prepare to download it
                file = bot.get_file(message.document.file_id)
                file_url = file.file_path
                file_name = message.document.file_name
                file_path = os.path.join("downloaded_files", file_name)
                download_tasks.append(download_file(session, file_url, file_path))
            elif message.video:
                # If the message has a video, prepare to download it
                file = bot.get_file(message.video.file_id)
                file_url = file.file_path
                file_name = f"{message.video.file_id}.mp4"
                file_path = os.path.join("downloaded_files", file_name)
                download_tasks.append(download_file(session, file_url, file_path))

        # Run all download tasks concurrently
        await asyncio.gather(*download_tasks)

    update.message.reply_text("Files have been downloaded at highest speed.")

def start(update, context):
    update.message.reply_text('Hello! I am your bot. Send /download to start downloading files.')

def organize_files():
    # Create subdirectories for categorization
    categories = ['videos', 'text', 'zips']
    for category in categories:
        if not os.path.exists(f"downloaded_files/{category}"):
            os.makedirs(f"downloaded_files/{category}")

    # Move files based on their type
    for filename in os.listdir("downloaded_files"):
        file_path = os.path.join("downloaded_files", filename)
        if os.path.isfile(file_path):
            if filename.endswith('.mp4'):
                shutil.move(file_path, f"downloaded_files/videos/{filename}")
            elif filename.endswith('.txt'):
                shutil.move(file_path, f"downloaded_files/text/{filename}")
            elif filename.endswith('.zip'):
                shutil.move(file_path, f"downloaded_files/zips/{filename}")
                
    print("Files have been organized into categories.")

def convert_text_to_pdf(text_file_path, output_pdf_path):
    # Create PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    with open(text_file_path, 'r') as file:
        content = file.read()

    pdf.multi_cell(0, 10, content)
    pdf.output(output_pdf_path)

def convert_all_texts_to_pdfs():
    text_folder = "downloaded_files/text"
    pdf_folder = "downloaded_files/pdfs"
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)

    for filename in os.listdir(text_folder):
        if filename.endswith('.txt'):
            text_file_path = os.path.join(text_folder, filename)
            output_pdf_path = os.path.join(pdf_folder, f"{filename.replace('.txt', '.pdf')}")
            convert_text_to_pdf(text_file_path, output_pdf_path)
            print(f"Converted {filename} to PDF.")

def main():
    # Initialize the updater and dispatcher
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Create command handlers
    start_handler = CommandHandler('start', start)
    download_handler = CommandHandler('download', download_files)
    
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(download_handler)

    # Start the bot
    updater.start_polling()

    # Once bot has finished downloading, organize files
    print("Organizing files...")
    organize_files()

    # Convert text files to PDFs
    print("Converting text files to PDFs...")
    convert_all_texts_to_pdfs()

    print("Process complete!")

if __name__ == "__main__":
    asyncio.run(main())
