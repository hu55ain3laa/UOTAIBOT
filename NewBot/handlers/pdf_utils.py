# pdf_utils.py
from telebot import types
from telebot.types import Message
from io import BytesIO
import img2pdf
from PIL import Image
from sqlmodel import Session, select
from models import User
from database import engine
from texts import (
    PDF_UTILS_MENU, PHOTO_TO_PDF, SEND_PHOTOS_FOR_PDF,
    PDF_CREATION_ERROR, PDF_CREATED_SUCCESSFULLY,
    PHOTO_ADDED_TO_PDF, FINISH_PDF_CREATION, CANCEL_PDF_CREATION,
    PDF_CREATION_CANCELLED, NO_PHOTOS_FOR_PDF
)

def pdf_utils_menu(message, send_message_once):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton(PHOTO_TO_PDF, callback_data="photo_to_pdf"))
    send_message_once(message.chat.id, PDF_UTILS_MENU, reply_markup=keyboard)

def photo_to_pdf_prompt(call, send_message_once):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_id == call.from_user.id)).first()
        if user:
            user.photo_ids = ""
            session.commit()
    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(FINISH_PDF_CREATION))
    keyboard.add(types.KeyboardButton(CANCEL_PDF_CREATION))
    
    send_message_once(call.message.chat.id, SEND_PHOTOS_FOR_PDF, reply_markup=keyboard)

def handle_photo_for_pdf(message: Message, bot, send_message_once):
    if message.photo:
        with Session(engine) as session:
            user = session.exec(select(User).where(User.telegram_id == message.from_user.id)).first()
            if user:
                photo_id = message.photo[-1].file_id
                if user.photo_ids:
                    user.photo_ids += f",{photo_id}"
                else:
                    user.photo_ids = photo_id
                session.commit()
                send_message_once(message.chat.id, PHOTO_ADDED_TO_PDF)
            else:
                send_message_once(message.chat.id, PDF_CREATION_ERROR.format(error="User not found"))
    elif message.text == FINISH_PDF_CREATION:
        create_pdf_from_photos(message, bot, send_message_once)
    elif message.text == CANCEL_PDF_CREATION:
        cancel_pdf_creation(message, send_message_once)
    else:
        send_message_once(message.chat.id, SEND_PHOTOS_FOR_PDF)

def create_pdf_from_photos(message: Message, bot, send_message_once):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_id == message.from_user.id)).first()
        if user and user.photo_ids:
            try:
                photo_ids = user.photo_ids.split(',')
                image_data = []
                for photo_id in photo_ids:
                    file_info = bot.get_file(photo_id)
                    downloaded_file = bot.download_file(file_info.file_path)
                    image = Image.open(BytesIO(downloaded_file))
                    
                    # Convert image to RGB if it's not already
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    
                    img_byte_arr = BytesIO()
                    image.save(img_byte_arr, format='JPEG')
                    image_data.append(img_byte_arr.getvalue())

                # Convert images to PDF
                pdf_bytes = img2pdf.convert(image_data)

                # Send the PDF file
                pdf_file = BytesIO(pdf_bytes)
                pdf_file.name = "combined_images.pdf"
                send_message_once(message.chat.id, PDF_CREATED_SUCCESSFULLY, document=pdf_file)

                # Clear photo_ids after successful PDF creation
                user.photo_ids = None
                session.commit()
            except Exception as e:
                send_message_once(message.chat.id, PDF_CREATION_ERROR.format(error=str(e)))
        else:
            send_message_once(message.chat.id, NO_PHOTOS_FOR_PDF)
    
    # Return to start menu after PDF creation
    from .general import start
    start(message, send_message_once)

def cancel_pdf_creation(message: Message, send_message_once):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_id == message.from_user.id)).first()
        if user:
            user.photo_ids = None
            session.commit()
    send_message_once(message.chat.id, PDF_CREATION_CANCELLED)
    
    # Return to start menu after cancellation
    from .general import start
    start(message, send_message_once)