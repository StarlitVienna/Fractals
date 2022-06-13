import os
import numpy
from tqdm import tqdm
import matplotlib.pyplot as plt
from PIL import Image as image


def mandelbrot(Re, Im, max_iter):
    c = complex(Re, Im)
    z = 0.0j

    for i in range(max_iter):
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

for row_index, Re in enumerate(tqdm(numpy.linspace(-2, 1, num=rows))):
    for column_index, Im in enumerate(numpy.linspace(-1, 1, num=columns)):
        result[row_index, column_index] = mandelbrot(Re, Im, 100)

possible_answers = ['yes', 'y', 'no', 'n', 'sim', 's', 'não', 'nao']
affirmative_answers = ['yes', 'y', 'sim', 's']
negative_answers = ['no', 'n', 'nao', 'não']



plt.figure(dpi=100)
plt.imshow(result.T, cmap='hot', interpolation='bilinear', extent=[-2, 1, -1, 1])
plt.xlabel('Re')
plt.ylabel('Im')
#print('show :D')


file_name = None
def get_file_name():
    file_name = input("File name: ")
    current_path = os.getcwd()
    if os.path.exists(f"{current_path}/{file_name}.png"):
        print("A file with the same name already exists")
        overwrite_file = input("Would you like to overwrite the file? [y/N] ")
        if overwrite_file.lower() not in possible_answers or overwrite_file.lower() in negative_answers:
            return get_file_name()
        elif overwrite_file.lower() in affirmative_answers:
            try:
                os.remove(f"{current_path}/{file_name}.png")
            except Exception as e:
                print(e)
                return get_file_name()
    return file_name



save = input('Save image? [Y/n] ')
if save.lower() not in possible_answers or save.lower() in affirmative_answers:
    save = True
    #get_file_name()
    file_name = get_file_name()
    plt.savefig(f"{os.getcwd()}/{file_name}.png")
img = image.open(f"{os.getcwd()}/{file_name}.png")
img.save('ic.ico')


plt.show()
