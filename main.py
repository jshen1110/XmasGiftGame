from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.image import Image
from random import randint

from cube import Cube


class Background(Widget):
    snowflake_texture = ObjectProperty(None)
    winter_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # create - match snowflake texture
        self.snowflake_texture = Image(source="xmas.png").texture
        self.snowflake_texture.wrap = 'repeat'
        self.snowflake_texture.uvsize = (Window.width / self.snowflake_texture.width, -1)

        # create - match floor snow texture
        self.winter_texture = Image(source="snowHouse.png").texture
        self.winter_texture.wrap = 'repeat'
        self.winter_texture.uvsize = (Window.width / self.winter_texture.width, -1)

    def on_size(self, *args):
        self.snowflake_texture.uvsize = (self.width / self.snowflake_texture.width, -1)
        self.winter_texture.uvsize = (self.width / self.winter_texture.width, -1)

    def scroll_textures(self, time_passed):
        # Update the uv position of the texture
        # where the snow are run + go left - go right
        self.snowflake_texture.uvpos = ((self.snowflake_texture.uvpos[0] + time_passed / 2.0) % Window.width, self.snowflake_texture.uvpos[1])
        self.winter_texture.uvpos = ((self.winter_texture.uvpos[0] + time_passed) % Window.width, self.winter_texture.uvpos[1])

        # Redraw the texture
        texture = self.property('snowflake_texture')
        texture.dispatch(self)

        texture = self.property('winter_texture')
        texture.dispatch(self)


class Gift(Image):
    velocity = NumericProperty(0)

    def on_touch_down(self, touch):
        self.source = "gift.png"
        self.velocity = 150
        super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.source = "gift.png"
        super().on_touch_up(touch)


class MainApp(App):
    cubes = []
    GRAVITY = 300
    was_colliding = False

    def move_gift(self, time_passed):
        gift = self.root.ids.gift
        gift.y = gift.y + gift.velocity * time_passed
        gift.velocity = gift.velocity - self.GRAVITY * time_passed
        self.check_collision()

    # check gift with cubes collision
    def check_collision(self):
        gift = self.root.ids.gift
        # Go through each cube and check if it collides
        is_colliding = False
        for cube in self.cubes:
            if cube.collide_widget(gift):
                is_colliding = True
                # Check if gift is between the gap
                if gift.y < (cube.cube_center - cube.GAP_SIZE / 2.0):
                    self.game_over()
                if gift.top > (cube.cube_center + cube.GAP_SIZE / 2.0):
                    self.game_over()
        if gift.y < 128:
            self.game_over()
        if gift.top > Window.height:
            self.game_over()

        if self.was_colliding and not is_colliding:
            self.root.ids.score.text = str(int(self.root.ids.score.text) + 1)
        self.was_colliding = is_colliding

    def game_over(self):
        self.root.ids.gift.pos = (100, (self.root.height - 128) / 2.0)
        for cube in self.cubes:
            self.root.remove_widget(cube)
        self.frames.cancel()
        self.root.ids.start_button.disabled = False
        self.root.ids.start_button.opacity = 1

    def next_frame(self, time_passed):
        self.move_gift(time_passed)
        self.move_cubes(time_passed)
        self.root.ids.background.scroll_textures(time_passed)

    # def on_start(self):
    #     Clock.schedule_interval(self.root.ids.background.scroll_textures, 1 / 60.)

    def start_game(self):
        self.root.ids.score.text = "0"
        self.was_colliding = False
        self.cubes = []
        self.frames = Clock.schedule_interval(self.next_frame, 1 / 60.)

        # Create the cubes
        num_cubes = 5
        distance_between_cubes = Window.width / (num_cubes - 1)
        for i in range(num_cubes):
            cube = Cube()
            # 400 - 850
            cube.cube_center = randint(128 + 200, self.root.height - 200)
            cube.size_hint = (None, None)
            # 100 - 1150 ，128
            cube.pos = (Window.width + i * distance_between_cubes, 128)
            cube.size = (108, self.root.height - 128)

            self.cubes.append(cube)
            self.root.add_widget(cube)

        # Move the cubes
        # Clock.schedule_interval(self.move_cubes, 1/60.)

    def move_cubes(self, time_passed):
        # Move cubes
        for cube in self.cubes:
            cube.x -= time_passed * 200

        # Check if we need to reposition the cubes at the right side
        num_cubes = 5
        distance_between_cubes = Window.width / (num_cubes - 1)
        cube_xs = list(map(lambda cube: cube.x, self.cubes))
        right_most_x = max(cube_xs)
        if right_most_x <= Window.width - distance_between_cubes:
            most_left_cube = self.cubes[cube_xs.index(min(cube_xs))]
            most_left_cube.x = Window.width
    # pass


MainApp().run()
