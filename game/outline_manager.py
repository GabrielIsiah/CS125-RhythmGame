from Sprites.outlines import Outline, outline_positions

class OutlineManager:
    def __init__(self, outlines):
        self.outlines = outlines
        self.key_to_outline_key = {
            'd': 'left_outline',
            'f': 'down_outline',
            'j': 'up_outline',
            'k': 'right_outline'
        }

    def add_outlines(self, outline_group):
        for key in ['d', 'f', 'j', 'k']:
            outline_key = self.key_to_outline_key[key]
            image = self.outlines[outline_key]
            pos = outline_positions[key]
            outline = Outline(image, pos, key)
            outline_group.add(outline) 