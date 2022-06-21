import numpy
import threading
from functools import partial
import matplotlib.pyplot as plt
from PIL import Image as image
import os
import numba as nb
from matplotlib.animation import FuncAnimation
#from gmpy2 import mpfr, get_context
#get_context().precision=10
if not os.path.isdir(f"{os.getcwd()}/fractals"):
    os.mkdir(f"{os.getcwd()}/fractals")
@nb.njit(fastmath=True)
def mandelbrot(Re, Im, max_iter):
    c = complex(Re, Im)
    #c = 1
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

#resolution = request_resolution()

##################

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
bboundx = numpy.int64(-2)
print(bboundx)
print(bboundx)
print(bboundx)
print(bboundx)
print(bboundx)

eboundx = 1
bboundy = -1
eboundy = 1
if zoom != 0:
    bboundx = sx+(sx/zoom)
    eboundx = sx-(sx/zoom)
    bboundy = sy+(sy/zoom)
    eboundy = sy-(sy/zoom)
print(nx)
#@nb.njit(fastmath=True)
def gen(width, height, iterations, axis, cmap, zoom):
    result = numpy.zeros([height, width])
    for row_index, Re in enumerate(numpy.linspace(bboundx, eboundx, num=height)):
        for column_index, Im in enumerate(numpy.linspace(bboundy, eboundy, num=width)):
            result[row_index, column_index] = mandelbrot(Re, Im, iterations)
    print(axis)
    if not axis:
        plt.axis('off')
    if cmap == '':
        cmap = 'hot'
    show(cmap, width, height, axis, result, zoom, iterations)
    
    return result.T
#gen()

possible_answers = ['yes', 'y', 'no', 'n', 'sim', 's', 'não', 'nao']
affirmative_answers = ['yes', 'y', 'sim', 's']
negative_answers = ['no', 'n', 'nao', 'não']

# animation BUTTON
first = True
zooming = False
def show(chosen_cmap, width, height, axis, result, zoom, iterations):
    global zooming
    global first
    #plt.figure(dpi=300)
    img = plt.imshow(result.T, cmap=chosen_cmap, interpolation='bilinear', extent=[bboundx, eboundx, bboundy, eboundy])
    plt.draw()
    if zoom and first:
        plt.connect('button_press_event', partial(click_thread, width, height, iterations, axis, chosen_cmap))
        plt.show()
        first = False
    elif not zoom and not first:
        plt.draw()
        return

    if not axis and zoom:
        plt.axis('off')
        plt.show()
        return
    elif axis and zoom:
        plt.show()
        return
    elif axis and not zoom and not zooming:
        plt.show()
        return
    img = None

#plt.xlabel('Re')
#plt.ylabel('Im')
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


#plt.axis('off')
def save_image():
    save = input('Save image? [Y/n] ')
    if save.lower() not in possible_answers:
        return save_image()
    elif save.lower() in affirmative_answers:
        file_name = get_file_name()
        plt.savefig(f"{os.getcwd()}/{file_name}.png", bbox_inches='tight', pad_inches=0.0)

#save_image()
zoomx = 1
img_name = 1
First = True
def onclick(event, width, height, iterations, axis, cmap, zoom):
    global img
    global zoomx
    global bboundx
    global eboundx
    global bboundy
    global eboundy
    global First
    global zooming
    #zoomx = 1
    for i in range(1):
        zoom_regulator = numpy.float(0.5/zoomx)
        cx, cy = event.xdata, event.ydata

        bboundx = float((cx-(zoom_regulator*1.5)))
        eboundx = float((cx+(zoom_regulator*1.5)))
        bboundy = float((cy-(zoom_regulator)))
        eboundy = float((cy+(zoom_regulator)))
        """
        bboundx = cx-n
        eboundx= cx+n
        bboundy = cy-n
        bboundy = cy+n
        """


        #gen()
        zoomx = zoomx+(zoomx)
        #if bboundy < 0:
        zooming = True
        img = plt.imshow(numpy.flipud(gen(width, height, iterations, axis, cmap, zoom)), cmap='hot', interpolation='bilinear', extent=[bboundx, eboundx, bboundy, eboundy])
        plt.draw()
        #else:
            #img = plt.imshow(result.T, cmap='hot', interpolation='bilinear', extent=[bboundx, eboundx, -bboundy, -eboundy])


def click_thread(width, height, iterations, axis, cmap, event):
    print(event, width, height, iterations, axis, cmap)
    onclick(event, width, height, iterations, axis, cmap, False)
#plt.connect('button_press_event', click_thread)
#plt.show()
