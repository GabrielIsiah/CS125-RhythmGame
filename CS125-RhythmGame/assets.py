from Utility.load_scale import  load_scale, rotate_img


IMAGE_SIZE = (250,150)
img_left_outline = load_scale('Graphics/left outline.png', IMAGE_SIZE)
img_down_outline = load_scale('Graphics/down outline.png', IMAGE_SIZE)
img_up_outline = load_scale('Graphics/up outline.png', IMAGE_SIZE)
img_right_outline = load_scale('Graphics/right outline.png', IMAGE_SIZE)
img_left_arrow = load_scale('Graphics/left.png', IMAGE_SIZE)
img_down_arrow = load_scale('Graphics/down.png', IMAGE_SIZE)
img_up_arrow = load_scale('Graphics/up.png', IMAGE_SIZE)
img_right_arrow = load_scale('Graphics/right.png', IMAGE_SIZE)

outlines = {
    'left_outline': img_left_outline,
    'down_outline': img_down_outline,
    'up_outline': img_up_outline,
    'right_outline': img_right_outline,


}

arrows = {
    'left_arrow': img_left_arrow,
    'right_arrow': img_right_arrow,
    'up_arrow': img_up_arrow,
    'down_arrow': img_down_arrow
}
