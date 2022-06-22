import main
from kivy.uix.screenmanager import Screen

class Settingssc(Screen):
    def go_back(self, x):
        print(x)
        main.App.get_running_app().root.transition.direction = 'right'
        main.App.get_running_app().root.current = 'generator'

    pass
