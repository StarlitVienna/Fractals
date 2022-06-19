import numpy
import time
import threading
from functools import partial
import matplotlib.pyplot as plt
from tqdm import tqdm
from PIL import Image as image
import os
import numba as nb
from decimal import Decimal, getcontext
import random
from matplotlib.animation import FuncAnimation
#from gmpy2 import mpfr, get_context
#get_context().precision=10
getcontext().prec=10

if not os.path.isdir(f"{os.getcwd()}/fractals"):
    os.mkdir(f"{os.getcwd()}/fractals")
color = 0
@nb.njit(fastmath=True)
def mandelbrot(Re, Im, max_iter, color):
    c = complex(Re, Im)
    z = 0.0j

    for i in nb.prange(max_iter):
        z = z*z + c
        if z.real*z.real + z.imag*z.imag >= 4:
            return i
    return max_iter

# Image resolution
##################
def request_resolution():
    resolution = input("Resolution: ")
    if not resolution.isnumeric():
        print('\nResolution is supposed to be an integer')
        print('Example: 1000 would be a 1000x1000 pixels image\n')
        return request_resolution()
    return int(resolution)

resolution = request_resolution()

columns = resolution
rows = resolution
##################

result = numpy.zeros([rows, columns])
times = 0
x_original = 2
y_original = 1
nx = times*1.5-x_original
ny = times-y_original
ttx = -1.85
tty = -0.075
zoom = 0
sx = -2
sy = 1
bboundx = -2
eboundx = 1
bboundy = -1
eboundy = 1

if zoom != 0:
    bboundx = sx+(sx/zoom)
    eboundx = sx-(sx/zoom)
    bboundy = sy+(sy/zoom)
    eboundy = sy-(sy/zoom)
#print(nx)

#@nb.njit(fastmath=True)
def gen(iterations):
    global color
    for row_index, Re in enumerate(numpy.linspace(bboundx, eboundx, num=rows)):
        for column_index, Im in enumerate(numpy.linspace(bboundy, eboundy, num=columns)):
            result[row_index, column_index] = mandelbrot(Re, Im, iterations, color)
        color += 1
iterations = input('Iterations: ')
if iterations == '':
    iterations = 100
gen(int(iterations))

possible_answers = ['yes', 'y', 'no', 'n', 'sim', 's', 'não', 'nao']
affirmative_answers = ['yes', 'y', 'sim', 's']
negative_answers = ['no', 'n', 'nao', 'não']



plt.figure(dpi=100)
img = plt.imshow(result.T, cmap='hot', interpolation='bilinear', extent=[bboundx, eboundx, bboundy, eboundy])
plt.xlabel('Re')
plt.ylabel('Im')
#print('show :D')


file_name = None
def get_file_name():
    file_name = input("File name: ")
    current_path = os.getcwd()
    if os.path.exists(f"{current_path}/fractals/{file_name}.png"):
        print("A file with the same name already exists")
        overwrite_file = input("Would you like to overwrite the file? [y/N] ")
        if overwrite_file.lower() not in possible_answers or overwrite_file.lower() in negative_answers:
            return get_file_name()
        elif overwrite_file.lower() in affirmative_answers:
            try:
                os.remove(f"{current_path}/fractals/{file_name}.png")
            except Exception as e:
                print(e)
                return get_file_name()
    return file_name


plt.axis('off')
def save_image():
    save = input('Save image? [Y/n] ')
    if save.lower() not in possible_answers:
        return save_image()
    elif save.lower() in affirmative_answers:
        file_name = get_file_name()
        plt.savefig(f"{os.getcwd()}/{file_name}.png", bbox_inches='tight', pad_inches=0.0)

zoom_mode = False
def request_zoom():
    zoom = input("zoom mode [y/N] ")
    if zoom not in possible_answers or zoom in negative_answers:
        zoom_mode = False
        return False
    elif zoom in affirmative_answers:
        zoom_mode = True
        return True


save_image()
zoomx = 1
img_name = 1
def onclick(event):
    global img
    global zoomx
    global iterations
    global bboundx
    global eboundx
    global bboundy
    global eboundy
    #zoomx = 1
    for i in range(1):
        zoom_regulator = 0.5/zoomx

        cx, cy = event.xdata, event.ydata
        bboundx = (cx-(zoom_regulator*1.5))
        eboundx = (cx+(zoom_regulator*1.5))
        bboundy = (cy-(zoom_regulator))
        eboundy = (cy+(zoom_regulator))
        """
        bboundx = cx-n
        eboundx= cx+n
        bboundy = cy-n
        bboundy = cy+n
        """

        
        gen(int(iterations))
        #if bboundy < 0:
        img = plt.imshow(numpy.flipud(result.T), cmap='hot', interpolation='bilinear', extent=[bboundx, eboundx, bboundy, eboundy])
        #else:
            #img = plt.imshow(result.T, cmap='hot', interpolation='bilinear', extent=[bboundx, eboundx, -bboundy, -eboundy])

        zoomx = zoomx+(zoomx/1.2)
        global img_name
        img_name += 1
        #plt.savefig(f"{os.getcwd()}/vid/{img_name}.png", bbox_inches='tight', pad_inches=0.0, dpi=300)
        #plt.draw()
        #time.sleep(.2)
def click_thread(event):
    threading.Thread(target=partial(onclick, event)).start()

if request_zoom():
    plt.connect('button_press_event', click_thread)

gen_again = True

def repeat():
    global zoom_mode
    plt.axis('off')
    gen_again = input('Generate again? [Y/n] ')

    if gen_again not in possible_answers or gen_again in affirmative_answers:
        gen_again = True
    elif gen_again in negative_answers:
        gen_again = False

    if gen_again:
        global img
        global zoomx
        global columns
        global rows
        global result
        global bboundx
        global eboundx
        global bboundy
        global eboundy

        bboundx = -2
        eboundx = 1
        bboundy = -1
        eboundy = 1

        resolution = request_resolution()

        columns = resolution
        rows = resolution
        result = numpy.zeros([rows, columns])
        iterations = input('Iterations: ')
        if iterations == '':
            iterations = 100
        gen(int(iterations))
        img = plt.imshow(numpy.flipud(result.T), cmap='hot', interpolation='bilinear', extent=[bboundx, eboundx, bboundy, eboundy])

        zoom_mode = request_zoom()
        if zoom_mode:
            plt.connect('button_press_event', click_thread)

        save_image()
        plt.draw()
        plt.show()
        
        return repeat()


    pass
plt.show()
repeat()
