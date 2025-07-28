
#main.py

### Contains application class that builds widget system, and then runs it

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.menu_screen import MainMenuScreen
from screens.simulation_screen import SimulationScreen

class GravitySimApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name="menu"))
        sm.add_widget(SimulationScreen(name="sim"))
        return sm

if __name__ == '__main__':
    GravitySimApp().run()