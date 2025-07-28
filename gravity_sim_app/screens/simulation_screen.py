
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from widgets.gravity_sim_widget import GravitySimWidget


class SimulationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')

        back_btn = Button(
            text="Back",
            size_hint=(1, 0.1),
            font_size='18sp',
            background_color=(0.2, 0.2, 0.5, 1)
        )

        back_btn.bind(on_press=self.go_back)

        self.sim_widget = GravitySimWidget(size_hint=(1, 1))

        # widgets are added from top to bottom
        self.add_widget(self.sim_widget)

        self.add_widget(back_btn)

        self.add_widget(layout)

    def set_planet(self, name):
        self.sim_widget.set_planet(name)

    def go_back(self, instance):
        self.manager.current = "menu"