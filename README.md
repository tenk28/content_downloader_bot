# Content Downloader Bot

This project is a Telegram bot for downloading Instagram content using RapidAPI.

## Setup

1. **Obtain API keys:**

   - `TELEGRAM_BOT_TOKEN` — your Telegram bot token from [BotFather](https://t.me/Botfather)  
   - `RAPID_API_KEY` — your RapidAPI key from [RapidAPI Instagram120](https://rapidapi.com/3205/api/instagram120)  

2. **Create a `.env` file** in the project root and add the tokens:

   ```env
   TELEGRAM_BOT_TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>
   RAPID_API_KEY=<YOUR_RAPID_API_KEY>

---

## Build and Run

Run the bot using Docker Compose:

```bash
docker compose up -d
