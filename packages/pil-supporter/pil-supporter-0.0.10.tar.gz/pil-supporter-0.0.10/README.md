# pil-supporter

https://pypi.org/project/pil-supporter
<pre>
pip install pil-supporter
</pre>

Supported APIs
<pre>
import pil_supporter

pil_supporter.utils.draw_rect(image, point1, point2)
pil_supporter.utils.draw_label(image, text, point, font_color=(255, 255, 255), font_size=28)
pil_supporter.utils.draw_rect_with_label(image, point1, point2, text, font_color=(255, 255, 255), font_size=28)
pil_supporter.utils.draw_point(image, point)
pil_supporter.utils.draw_image(image, image_to_draw, point)

pil_supporter.utils.crop_center(image_file, left, top, right, bottom)
pil_supporter.utils.create_dummy_image(size, image_file, background_color=(255, 255, 255))
pil_supporter.utils.read_from_image_file(image_file)
</pre>
