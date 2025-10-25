import os
from typing import Final
from collections.abc import Sequence

from telegram import Update, InputMediaPhoto, InputMediaVideo
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest
from telegram.constants import ChatAction, MediaGroupLimit

from router import SocialRouter

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

router = SocialRouter()

class MediaType():
    VIDEO: Final[str] = 'video'
    IMAGE: Final[str] = 'image'
    UNKNOWN: Final[str] = 'unknown'

def get_media_type(url: str) -> MediaType:
    if '.mp4' in url:
        return MediaType.VIDEO
    if any(ext in url for ext in ['.jpg', '.jpeg', '.png', '.webp']):
        return MediaType.IMAGE
    print(f'Unknown media type for url: {url}')
    return MediaType.UNKNOWN

def create_media_groups(download_urls) -> Sequence[Sequence[InputMediaPhoto | InputMediaVideo]]:
    flat_media: list[InputMediaPhoto | InputMediaVideo] = []
    for url in download_urls:
        media_type = get_media_type(url)
        if media_type == MediaType.IMAGE:
            flat_media.append(InputMediaPhoto(url))
        elif media_type == MediaType.VIDEO:
            flat_media.append(InputMediaVideo(url))

    result: list[list[InputMediaPhoto | InputMediaVideo]] = [
        flat_media[i:i+MediaGroupLimit.MAX_MEDIA_LENGTH] for i in range(0, len(flat_media), MediaGroupLimit.MAX_MEDIA_LENGTH)
    ]

    return result

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_title = f'"{update.effective_chat.title}"' if update.effective_chat.title else 'Private'
    print(f'Message received from chat {update.effective_chat.id} ({chat_title})')
    print(f'From: "{update.effective_user.full_name}"')
    print(f'Text: "{update.message.text}"\n')

    download_urls = router.handle(update.message.text)
    if not download_urls:
        if update.effective_chat.type == 'private':
            await update.message.reply_text(
                f'⚠️ Couldn\'t handle text "{update.message.text}"',
                reply_to_message_id=update.message.message_id
            )
        return

    try:
        for group in create_media_groups(download_urls):
            action = ChatAction.UPLOAD_VIDEO if isinstance(group[0], InputMediaVideo) else ChatAction.UPLOAD_PHOTO
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=action)
            await update.message.reply_media_group(group, reply_to_message_id=update.message.message_id)
    except Exception as e:
        await update.message.reply_text(
            f'⚠️ Couldn\'t handle text "{update.message.text}", error: {e}',
            reply_to_message_id=update.message.message_id
        )
        raise e
    return

def main():
    request = HTTPXRequest(
        media_write_timeout=1000.0
    )

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).request(request).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_text))
    print("Starting bot")
    app.run_polling()

if __name__ == '__main__':
    main()
