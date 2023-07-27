from aiogram import Bot, Dispatcher, executor, types
import os
from PIL import Image
from pytesseract import pytesseract
import time


bot = Bot(token=os.environ.get("BOT_TOKEN"))
dp = Dispatcher(bot)

DOWNLOAD_PATH = os.environ.get('DOWNLOAD_PATH')
PATH_TO_TESSERACT = rf"{os.environ.get('PATH_TO_TESSERACT')}"


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.reply("Hello! Im an OCR bot that converts text in images into message")


@dp.message_handler(commands=['help'])
async def helping(message: types.Message):
    await message.reply("Just send me an image that contains some words")


# Handler for messages containing photos
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    photo = message.photo[-1]  # Get the largest available PHOTO
    file_id = photo.file_id  # Get file id
    file = await bot.get_file(file_id)
    photo_url = file.file_path  # Get file url

    # Download the photo
    file_name = os.path.basename(photo_url)
    download_path = os.path.join(DOWNLOAD_PATH, file_name)  # fixing permission issue
    await bot.download_file(photo_url, destination=download_path)
    # Send a confirmation message to the user
    await message.reply("Photo downloaded successfully!")

    image_path = rf"{DOWNLOAD_PATH}/{file_name}"
    # Opening the image and storing it in an image object
    img = Image.open(image_path)
    # Providing the tesseract executable location to pythesseract library
    pytesseract.tesseract_cmd = PATH_TO_TESSERACT
    # Passing the image object to image_to_string() function
    # This function will extract the text from the image
    text = pytesseract.image_to_string(img)

    # replying the sender by the text from the image
    time.sleep(3)
    await message.reply(f"The text in the photo was:\n {text}")


if __name__ == '__main__':
    executor.start_polling(dp)
