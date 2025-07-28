

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Rectangle

import constants


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.dropdown import DropDown
        from kivy.uix.button import Button
        from kivy.uix.label import Label

        layout = BoxLayout(orientation='vertical', padding=40, spacing=30)

        title = Label(text="Gravitational Slingshot", font_size='30sp')
        
        self.planet_options = list(constants.PLANET_MASSES.keys())
        self.selected_planet = None

        self.spinner = Spinner(
            text = "Select Planet",
            values=[val[0].upper() + val[1:] for val in self.planet_options],
            size_hint=(1, 0.2)
        )

        self.spinner.bind(text=self.select_planet)

        self.start_btn = Button(text="Start Simulation", 
                        size_hint=(1, 0.2),
                        font_size='20sp',
                        background_color=(0.5, 0.0, 0.5, 1),
                        disabled=True
                    )
        self.start_btn.bind(on_press=self.start_simulation)

        quit_btn = Button(text="Quit", 
                        size_hint=(1, 0.2),
                        font_size='20sp',
                        background_color=(0.8, 0.1, 0.1, 1)
                    )
        quit_btn.bind(on_press=self.quit_app)

        with self.canvas.before:
            self.bg_rect = Rectangle(source='images/menu_image.jpg', size=self.size, pos=self.pos)
        
        self.bind(size=self.update_bg, pos=self.update_bg)

        layout.add_widget(title)
        layout.add_widget(self.spinner)
        layout.add_widget(self.start_btn)
        layout.add_widget(quit_btn)
        
        self.add_widget(layout)

    def select_planet(self, spinner, text):
        self.selected_planet = text.lower()
        self.start_btn.disabled = False
        

    def start_simulation(self, instance):
        sim_screen = self.manager.get_screen("sim")
        sim_screen.set_planet(self.selected_planet)

        self.manager.current = "sim"

    def quit_app(self, instance):
        App.get_running_app().stop()

    def on_pre_enter(self):
        self.spinner.text = "Select a Planet"
        self.start_btn.disabled = True
        self.selected_planet = None

    def update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

