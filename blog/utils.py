import os
from flask_login import current_user
from PIL import Image
from blog import app


def save_image(picture_form_data):
    filename, extension = os.path.splitext(picture_form_data.filename)
    new_file_name = current_user.username + extension
    file_path = os.path.join(app.root_path, 'static/profile_pictures', new_file_name)
    output_size = (300, 300)
    resized_image = Image.open(picture_form_data)
    resized_image.thumbnail(output_size)
    resized_image.save(file_path)
    return new_file_name