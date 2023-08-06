
from PIL import Image

def crop_center(image_file, left, top, right, bottom):
    image = Image.open(image_file)
    width, height = image.size
    cropped_image = image.crop((left, top, width - right, height - bottom))

    cropped_image.save(image_file)

def create_dummy_image(size, image_file, background_color=(255, 255, 255)): #
    #https://stackoverflow.com/questions/12760389/how-can-i-create-an-empty-nm-png-file-in-python
    width, height = size[0], size[1]
    if background_color == None:
        img = Image.new("RGBA", (width, height), (255, 255, 255))
    else:
        img = Image.new("RGB", (width, height), background_color)
    img.save(image_file, "PNG")
    return img


def read_from_image_file(image_file):
    img = Image.open(image_file)

    return img
