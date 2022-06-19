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
    def click_thread(event):
        cx, cy = event.xdata, event.ydata

           

    def gen_graph(self, width, height, iterations, axis, cmap, zoom):

        # thread
        # load bar
        if iterations == '':
            iterations = 100
        
        if axis == 'off':
            axis = False
        else:
            axis = True

        if zoom == '':
            zoom = False
        else:
            zoom = True

        try:
            gen(int(width), int(height), int(iterations), axis, cmap, zoom)
        except Exception as e:
            print(e)
    #gen_graph()

    def thread_gen(self, width, height, iterations, axis, cmap, zoom):
        threading.Thread(target=partial(self.gen_graph, width, height, iterations, axis, cmap, zoom)).start()


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
