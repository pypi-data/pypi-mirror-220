from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np
import matplotlib.pyplot as plt
import platform

def draw_rect(image, point1, point2):
    draw = ImageDraw.Draw(image)
    draw.rectangle((point1, point2), outline=(0, 0, 255), width=3)

    return image

def draw_label(image, text, point, font_color=(255, 255, 255), font_size=28):
    x, y = point
    draw = ImageDraw.Draw(image)
    if platform.system() == 'Darwin': #맥
        font = 'AppleGothic.ttf'
    elif platform.system() == 'Windows': #윈도우
        font = 'malgun.ttf'
    elif platform.system() == 'Linux': #리눅스 (구글 콜랩)
        '''
        !wget "https://www.wfonts.com/download/data/2016/06/13/malgun-gothic/malgun.ttf"
        !mv malgun.ttf /usr/share/fonts/truetype/
        import matplotlib.font_manager as fm 
        fm._rebuild() 
        '''
        font = 'malgun.ttf'
    try:
        imageFont = ImageFont.truetype(font, font_size)
    except:
        imageFont = ImageFont.load_default()
    text_width, text_height = imageFont.getsize(text)
    draw.text((x, y - text_height), text, font=imageFont, fill=font_color)

    return image

def draw_rect_with_label(image, point1, point2, text, font_color=(255, 255, 255), font_size=28):
    draw = ImageDraw.Draw(image)
    draw.rectangle((point1, point2), outline=(0, 0, 255), width=3)

    x1, y1 = point1
    if platform.system() == 'Darwin': #맥
        font = 'AppleGothic.ttf'
    elif platform.system() == 'Windows': #윈도우
        font = 'malgun.ttf'
    elif platform.system() == 'Linux': #리눅스 (구글 콜랩)
        '''
        !wget "https://www.wfonts.com/download/data/2016/06/13/malgun-gothic/malgun.ttf"
        !mv malgun.ttf /usr/share/fonts/truetype/
        import matplotlib.font_manager as fm 
        fm._rebuild() 
        '''
        font = 'malgun.ttf'
    try:
        imageFont = ImageFont.truetype(font, font_size)
    except:
        imageFont = ImageFont.load_default()
    text_width, text_height = imageFont.getsize(text)
    draw.rectangle(((x1, y1 - text_height), (x1 + text_width, y1)), fill=(0, 0, 255)) #채워진 사각형
    draw.text((x1, y1 - text_height), text, font=imageFont, fill=font_color)

    return image

def draw_point(image, point):
    x, y = point
    draw = ImageDraw.Draw(image)
    radius = 2
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(0, 0, 255))

    return image

def draw_image(image, image_to_draw, point):
    alpha_range = image_to_draw.getextrema()[-1]
    print(alpha_range)
    if alpha_range == (0, 255):
        image.paste(image_to_draw, point, mask=image_to_draw)
    else:
        image.paste(image_to_draw, point)

    return image
