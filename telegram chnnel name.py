import requests

# Replace with your bot token and the invite link
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_INVITE_LINK = "https://t.me/+6JXsFKsRX7lmNTM1"

# Get chat details using getChat method
def get_channel_id():
    chat_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChat"
    response = requests.get(chat_url, params={'chat_id': CHANNEL_INVITE_LINK})
    if response.status_code == 200:
        chat_info = response.json()
        print(chat_info)  # This will print the channel ID and other details
    else:
        print("Failed to get channel info.")

get_channel_id()
