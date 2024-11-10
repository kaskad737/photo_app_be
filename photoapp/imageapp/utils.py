import qrcode
import os
from django.conf import settings
from django.core.files import File
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO


def insert_photo_to_frame(photo_instance, frame_path):
    # Open the frame and photo images
    frame = Image.open(frame_path)
    photo = Image.open(photo_instance.photo.path)

    target_width, target_height = 900, 600

    photo = photo.resize((target_width, target_height), Image.LANCZOS)

    frame_width, frame_height = frame.size
    x = (frame_width - target_width) // 2
    y = (frame_height - target_height) // 2

    # Paste the photo onto the frame at the calculated position
    frame.paste(photo, (x, y), photo if photo.mode == 'RGBA' else None)

    temp_buffer = BytesIO()
    frame.save(temp_buffer, format='PNG')
    temp_buffer.seek(0)

    # Save the image to the 'photo_in_frame' field of the Photo instance
    photo_instance.photo_in_frame.save(
        f"{photo_instance.id}_in_frame.png",
        ContentFile(temp_buffer.read()),
        save=False
    )

    # Ensure to save the model instance after updating the field
    photo_instance.save()


def add_qr_code_to_image(photo_instance):
    # Open the framed photo
    framed_photo = Image.open(photo_instance.photo_in_frame.path)
    qr_code = Image.open(photo_instance.qrcode.path).convert("RGBA")

    target_width, target_height = 200, 200
    qr_code = qr_code.resize((target_width, target_height), Image.LANCZOS)

    qr_position = (1200, 950)
    framed_photo.paste(qr_code, qr_position, qr_code if qr_code.mode == 'RGBA' else None)

    output_buffer = BytesIO()
    framed_photo.save(output_buffer, format="PNG")
    output_buffer.seek(0)  # Rewind the buffer to the beginning

    return output_buffer.getvalue()


def create_qr_code(photo_instance, absolute_download_url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(absolute_download_url)
    qr.make(fit=True)

    qr_dir = os.path.join(settings.MEDIA_ROOT, 'qrcode')
    if not os.path.exists(qr_dir):
        os.makedirs(qr_dir)

    qr_img = qr.make_image(fill='black', back_color='white')
    qr_path = os.path.join(qr_dir, f'{photo_instance.id}_qr.png')
    qr_img.save(qr_path)

    with open(qr_path, 'rb') as f:
        photo_instance.qrcode.save(f'{photo_instance.id}_qr.png', File(f))
