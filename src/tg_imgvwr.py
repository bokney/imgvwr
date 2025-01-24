
import os
import random
import logging
from dotenv import dotenv_values
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


class TG_IMGVWR:
    def __init__(self, token: str, image_dir: str):
        self.image_dir = image_dir

        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)

        self.application = Application.builder().token(token).build()

        self.add_handlers()

    def add_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.send_random_image))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Send me any message and I'll send you a random image!")
        self.logger.info(f"User {update.effective_user.username} started the bot.")

    async def send_random_image(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user.username
        message_text = update.message.text
        self.logger.info(f"Recieved message from {user}: {message_text}")
        images = [
            f for f in os.listdir(self.image_dir)
            if f.lower().endswith(('.png', '.gif', '.jpeg', '.jpg'))
        ]
        if not images:
            await update.message.reply_text("Uh-oh! No images found in directory?!")
            self.logger.warning("No images found in the directory!")
            return None
        
        random_image = random.choice(images)
        img_path = os.path.join(self.image_dir, random_image)

        with open(img_path, 'rb') as img_file:
            if random_image.lower().endswith('.gif'):
                await update.message.reply_animation(img_file)
                self.logger.info(f"Sent animated GIF '{random_image}' to {user}.")
            else:
                await update.message.reply_photo(img_file)
                self.logger.info(f"Sent image '{random_image}' to {user}.")
        
    def run(self):
        self.logger.info("Bot is starting...")
        self.application.run_polling()


def main():
    config = dotenv_values(".env")
    bot_token = config.get("TG_BOT_KEY")

    if not bot_token:
        raise ValueError("No Bot token in .env file!")

    img_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/data"

    bot = TG_IMGVWR(token=bot_token, image_dir=img_dir)
    bot.run()

if __name__ == "__main__":
    main()
