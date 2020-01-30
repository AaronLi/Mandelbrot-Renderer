from multiprocessing import Pool
from PIL import Image
from math import sin, pi
import numpy as np
import time

max_depth = 100

def mandelbrot(c, threshold):
    v = c
    for i in range(max_depth+1):
        if abs(v) > threshold:
            return i
        v = v**2+c
    return i

def mandelbrot_column(real, imaginary_value_scale, num_imaginary_values, threshold):
    imaginary_value_range = imaginary_value_scale[1] - imaginary_value_scale[0]
    return [mandelbrot(complex(real, i/num_imaginary_values*imaginary_value_range+imaginary_value_scale[0]), threshold) for i in range(num_imaginary_values)]
    

if __name__ == '__main__':
    def sin01(x):
        angle = x*pi*2

        sin_out = sin(angle)+1

        return sin_out/2



    def colour(v, mode='rgb'):
        if mode=='rgb':
            return (int(255*(sin01(v/max_depth+(1/3)))), int(255*(sin01(v/max_depth+(0/3)))), int(255*(sin01(v/max_depth+(2/3)))))
        elif mode=='grayscale':
            return (int(255*v/max_depth), int(255*v/max_depth), int(255*v/max_depth))

    thread_pool = Pool(6)

    max_width = 5000
    max_height = int(2/3*max_width)

    total_start_time = time.time()

    for i in range(10, max_width, 50):
        width = i

        height = int(2/3 * width)
        print('(%d, %d)'%(width, height))

        start_time = time.time()
        

        dIn = [(3*i/width-2, (-1, 1), height, 2) for i in range(width)]
        data_result = thread_pool.starmap_async(mandelbrot_column, dIn)

        while not data_result.ready():
            print('Time: %.2f'%(time.time()-start_time), end='\r')
        print('Drawing...'+20*' ', end='\r')

        dOut = data_result.get()

        data_array = np.full((width, height), dOut, dtype=int).transpose()

        a= Image.fromarray(data_array)

        a = a.convert("P")

        a.putpalette([j for i in range(np.max(data_array)+1) for j in colour(i)])

        a.resize((max_width, max_height)).save("Mandelbrot%04d.png"%i)

        print("finished in %.2f seconds"%(time.time()-start_time))
    print("Animation finished rendering in %.2f seconds"%(time.time()-total_start_time))
