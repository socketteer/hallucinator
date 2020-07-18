import tkinter
from enum import Enum
from inspect import signature
from typing import NamedTuple, Tuple, get_args

import cv2
import PIL.Image, PIL.ImageTk
import numpy as np



# TODO Add more
class ColorStyle(Enum):
    GRAYSCALE = "grayscale"
    HSV = "hsv"
    ffsd = "sda"

for color in ColorStyle:
    print(color)
for color in ColorStyle.HSV.__class__:
    print(color)

# TODO Add more
class PlotStyle(Enum):
    CONTOUR = "contour"

class ViewSettings(NamedTuple):
    style: ColorStyle = ColorStyle.HSV
    plot_type: PlotStyle = PlotStyle.CONTOUR
    value_range: Tuple[int, int] = (-1, 1)
    resolution: int = 500
    example_complex: complex = 1


def get_param_info(func):
    return {name: param.default for name, param in signature(func).parameters.items()}, \
           {name: param.annotation for name, param in signature(func).parameters.items()}


print(get_param_info(ViewSettings))
print(type(signature(ViewSettings).parameters))
for name, param in signature(ViewSettings).parameters.items():
    print(type(param), param)
    print(name, param.annotation, param.default)
    print(type(param.annotation))
    try:
        print("type args", get_args(param.annotation))
    except Exception as e:
        print(e)
    print("\n\n")

print(PlotStyle(PlotStyle.CONTOUR))

generic_types = {
    int: (int, np.integer),
    float: (float, np.floating),
    complex: (complex, np.complexfloating),
    bool: (bool, np.bool),
    str: (str, np.str),
    tuple: (tuple, np.ndarray),
    Enum: (Enum,)
}



def convert_to_builtin(type_to_convert):
    generic_type = None
    for builtin_type, corresponding_types in generic_types.items():
        if issubclass(type_to_convert, corresponding_types):
            generic_type = builtin_type
    return generic_type



#
# class App:
#     def __init__(self, window, window_title, image_path="imgs/close.gif"):
#         self.window = window
#         self.window.title(window_title)
#
#         # Load an image using OpenCV
#         img = cv2.imread(image_path)
#         img = np.random.randint(0, 255, (1000, 1000), dtype=np.uint8)
#         print(img.shape, img)
#         self.cv_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#
#          # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
#         self.height, self.width, no_channels = self.cv_img.shape
#
#         # Create a canvas that can fit the above image
#         self.canvas = tkinter.Canvas(window, width =10, height=10)# self.width, height = self.height)
#         self.canvas.pack()
#         # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
#         self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))
#
#         # Add a PhotoImage to the Canvas
#         self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
#         print(self.canvas.info())
#         print(self.canvas.winfo_children())
#         print(self.canvas)
#         # Button that lets the user blur the image
#         self.btn_blur=tkinter.Button(window, text="Blur", width=50, command=self.blur_image)
#         self.btn_blur.pack(anchor=tkinter.CENTER, expand=True)
#
#         self.window.mainloop()
#
#     # Callback for the "Blur" button
#     def blur_image(self):
#         self.cv_img = cv2.blur(self.cv_img, (3, 3))
#         self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))
#         self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
#
#
# # Create a window and pass it to the Application object
# App(tkinter.Tk(), "Tkinter and OpenCV")