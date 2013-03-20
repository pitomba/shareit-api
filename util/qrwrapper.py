import qrcode
from string_generator import get_new_random_file_name

def get_new_qrcode_path(msg):
    image = create_qrcode(msg)
    image_path = save_image(image)

    return image_path


def create_qrcode(msg):
    return qrcode.make(msg)


def save_image(image):
    image_path = get_new_random_file_name()
    image.save(image_path)
    return image_path
