from kivy.lang import Builder
from kivymd.app import MDApp as App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from kivy.core.window import Window
from gen_mandelbrot import gen
import threading
from functools import partial
Window.size = (350, 400)

class MainScreen(Screen):
    print(plt.colormaps())
    def switch_screen(self, name):
        App.get_running_app().root.transition.direction = 'left'
        App.get_running_app().root.current = name
        pass


    def click_thread(event):
        cx, cy = event.xdata, event.ydata

           

    def gen_graph(self, width, height, iterations, axis, cmap, zoom):

        # thread
        # load bar
        if iterations == '':
            iterations = 100
        if cmap not in plt.colormaps():
            cmap = 'twilight_shifted'
        
        try:
            gen(int(width), int(height), int(iterations), axis, cmap, zoom, False)
        except Exception as e:
            print(e)
    #gen_graph()

    def thread_gen(self):
        ids = self.ids
        setting_ids = App.get_running_app().root.get_screen('settings').ids
        self.gen_graph(ids.width.text, ids.height.text, ids.iterations.text, setting_ids.axis.active, ids.cmap.text, setting_ids.zoom.active)


class ScreenManager(ScreenManager):
    pass

class KivyApp(App):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Cyan'
        kv = Builder.load_file('./main.kv')
        return kv
    
if __name__ == '__main__':
    KivyApp().run()
