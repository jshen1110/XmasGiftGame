from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.uix.image import Image
from kivy.clock import Clock


class Cube(Widget):
    # Numeric attributes
    # set gap, cap size. others randoms
    GAP_SIZE = NumericProperty(160)  # Height to control difficulty
    CAP_SIZE = NumericProperty(48)  # Height of cube_cap.png
    cube_center = NumericProperty(0)
    bottom_body_position = NumericProperty(0)
    bottom_cap_position = NumericProperty(0)
    top_body_position = NumericProperty(0)
    top_cap_position = NumericProperty(0)

    # Texture
    cube_body_texture = ObjectProperty(None)
    lower_cube_tex_coords = ListProperty((0, 0, 1, 0, 1, 1, 0, 1))
    top_cube_tex_coords = ListProperty((0, 0, 1, 0, 1, 1, 0, 1))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cube_body_texture = Image(source="cube_body.png").texture
        self.cube_body_texture.wrap = 'repeat'

    def on_size(self, *args):
        lower_body_size = self.bottom_cap_position - self.bottom_body_position

        self.lower_cube_tex_coords[5] = lower_body_size / 76.
        self.lower_cube_tex_coords[7] = lower_body_size / 76.

        top_body_size = self.top - self.top_body_position

        self.top_cube_tex_coords[5] = top_body_size / 76.
        self.top_cube_tex_coords[7] = top_body_size / 76.

    def on_cube_center(self, *args):
        Clock.schedule_once(self.on_size, 0)
