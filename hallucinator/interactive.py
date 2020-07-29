
import math

import cv2
import numpy as np
import hallucinator as hl


# Tile images with borders between them. Hopefully they are all the same size!
def tile_images(images, num_rows=None, border_width=10):
    # Prefer cols to rows, need cols*cols-1 > n
    if num_rows is None:
        num_rows = math.floor(math.sqrt(len(images)))

    # Create a vertical border and build each row
    border_shape = list(images[0].shape)
    border_shape[1] = border_width
    vertical_border = np.zeros(shape=border_shape, dtype=np.uint8)
    rows = hl.grouper(images, num_rows)
    rows = list(map(np.hstack, [list(hl.intersperse(row, vertical_border))for row in rows]))
    # Add a black box to fill out the final row
    extra_shape = list(rows[-1].shape)
    extra_shape[1] = rows[0].shape[1] - rows[-1].shape[1]
    black_box = np.zeros(shape=extra_shape, dtype=np.uint8)
    rows[-1] = np.hstack([rows[-1], black_box])

    # Create a horizontal border and combine the rows
    border_shape = list(rows[0].shape)
    border_shape[0] = border_width
    horizontal_border = np.zeros(shape=border_shape, dtype=np.uint8)
    image = np.vstack(list(hl.intersperse(rows, horizontal_border)))
    return image


def text_image(text, shape):
    origin = (35, 35)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    thickness = 1
    color = (255, 255, 255)

    black_area = np.zeros(shape=shape, dtype=np.uint8)
    cv2.putText(black_area, text, org=origin, fontFace=font, fontScale=font_scale, color=color, thickness=thickness)
    return black_area


def add_text_bar(image, text):
    text_shape = list(image.shape)
    text_shape[0] = 60
    text_img = text_image(text, shape=text_shape)
    return np.vstack([image, text_img])


# image_func: returns the image to be displayed
# key_func: called when a key is pressed with its unicode. (compare to ord('s'))
# sliders = [
#   ("slider_name", (slider_val_1, ...)[, default_val)]
# ] # default val is optional: looks for the closest val in slider_vals, defaults to mid of slider_vals
# slider_func: called when a slider changes with a dict of all sliders, {slider_name: slider_value}
def start_interactive(image_func, key_callback=None, sliders=None, slider_callback=None, print_keys=False):
    window_name = "interactive"
    cv2.namedWindow(window_name)

    if sliders is not None:
        # Call the slider_callback with a dictionary of {name: value} for each slider and rerender
        def _slider_callback(_):
            slider_callback({
                name: slider_range[cv2.getTrackbarPos(name, window_name)]
                for name, slider_range, *ignore in sliders
            })
            cv2.imshow("interactive", image_func())

        for slider in sliders:
            name, slider_range = slider[:2]
            cv2.createTrackbar(name, window_name, 0, len(slider_range)-1, _slider_callback)

        # Default index is the closest to the value they provided or mid of steps
        def reset_sliders():
            for slider in sliders:
                name, slider_range = slider[:2]
                default_index = np.abs(slider_range-slider[2]).argmin() if len(slider) > 2 else len(slider_range)//2
                cv2.setTrackbarPos(name, window_name, default_index)
        reset_sliders()



    # Show the image and look for key pressed
    cv2.imshow(window_name, image_func())
    while True:
        # esc=27, up=126, down=125, left=123, right=124.
        # Sometimes these stop working...?
        key = cv2.waitKey(1000)
        if key_callback and key != -1:
            key_callback(key & 0xFF)  # & 0xFF (keeps the last 8 bits). Compare key to ord("letter")
            cv2.imshow(window_name, image_func())
        if print_keys:
            print(f"Key press: {key}")

        # ~: reset sliders
        if key == ord("`") or key == ord("~") and sliders is not None:
            reset_sliders()

        # Escape: quit
        if key == 27:
            break

        # If the window was closed in the last 1000ms, it means they want to leave!
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()


def main():
    def zp_product(
            p,
            value_range,
            resolution,
            hsv,
    ):
        xy = hl.xy_plane(value_range=hl.tuplify(value_range), resolution=resolution)
        zp1 = hl.phase_threshold(hl.opl_zp(hl.perspective_plane(p=[0, 0, 10], xy=xy)))
        zp2 = hl.phase_threshold(hl.phase_conjugate(hl.opl_zp(hl.perspective_plane(p=p, xy=xy))))
        zp3 = hl.phase_threshold(zp1 + zp2)

        tiled = tile_images([hl.imagify(zp0, hsv=hsv, bwref=(0, 2 * math.pi)) for zp0 in [zp1, zp2, zp3, zp1]])
        # return hl.imagify(tiled)
        return tiled
        zp1, zp2, zp3 = [hl.imagify(zp0, hsv=hsv, bwref=(0, 2 * math.pi)) for zp0 in [zp1, zp2, zp3]]

        border_shape = list(zp1.shape)
        border_shape[1] = 10
        border = np.zeros(shape=border_shape)
        image = hl.np.hstack([zp1, border, zp2, border, zp3])
        # return hl.imagify(zp3)
        return hl.imagify(image)


    def get_default_params():
        return {
            "p": [0, 0, 10],
            "value_range": np.array([[-1, 1], [-1, 1]], dtype=np.float64),
            "resolution": 300,
            "hsv": True
        }

    def params_string(params):
        return f"p: {hl.tupliround(params['p'])}  " \
               f"range: {hl.tupliround(params['value_range'])} " \
               f"hsv={params['hsv']}  " \
               f"resolution={params['resolution']}  "

    params = get_default_params()
    xy_step = 1/8
    point_step = 0.5
    xy_scale = 1.1
    resolution_step = 100

    def image_func():
        image = zp_product(**params)
        image = add_text_bar(image, params_string(params))
        return image

    def key_func(key):
        length = params["value_range"][1][1] - params["value_range"][1][0]
        if key == ord("s"):  # Image coordinates are reversed! 0,0 is at the top left
            params["value_range"][1] += length*xy_step
        elif key == ord("w"):
            params["value_range"][1] -= length*xy_step
        elif key == ord("d"):
            params["value_range"][0] += length*xy_step
        elif key == ord("a"):
            params["value_range"][0] -= length*xy_step


        elif key == ord("z"):
            params["value_range"][:, 0] -= xy_scale
            params["value_range"][:, 1] += xy_scale
        elif key == ord("x"):
            params["value_range"][:, 0] += xy_scale
            params["value_range"][:, 1] -= xy_scale

        elif key == ord("p"):
            params["p"][1] += point_step
        elif key == ord(";"):
            params["p"][1] -= point_step
        elif key == ord("'"):
            params["p"][0] += point_step
        elif key == ord("l"):
            params["p"][0] -= point_step

        elif key == ord("["):
            params["p"][2] -= point_step
        elif key == ord("]"):
            params["p"][2] += point_step


        elif key == ord("r"):
            params["resolution"] += resolution_step
        elif key == ord("e"):
            params["resolution"] -= resolution_step if params["resolution"] > resolution_step else 0


        elif key == ord("h"):
            params["hsv"] = not params["hsv"]

        if key == ord("."):
            params["value_range"] = get_default_params()["value_range"]

    start_interactive(image_func, key_func, sliders=[("hello", 0, 2, 2, 0)], slider_func=print)


if __name__ == "__main__":
    main()





# # Pipe dreams.... This makes things terrible....
# # Need assignments in lambdas!! but even in 3.8 can't do that with subscripts
#
# # ----------------------------------
#
# def increase_dict_value(d, key, value):
#     setattr(d, key, d[key] + value)
#
# def increase_param(key, dx):
#     setattr(params, key, params[key] + dx)
#
# key_funcs = {
#     "s": increase_param("value_range")
# }
#
# # Dictionary {"k": lambda: setattr(params, "resolution", params["resolution"] + 3)}
# # {"k": lambda: increase_dict_value(params, "resolution", 3)}
# def interactive(images_func, key_funcs):
#     while True:
#         cv2.imshow('image', images_func())
#
#         ord_keys = {ord(c): func for c, func in key_funcs.items()}
#         key = cv2.waitKey() & 0xFF
#         if key in ord_keys:
#             ord_keys[key]()
#         elif key in key_funcs:
#             key_funcs[key]()
#         elif key == 27:  # Escape
#             break
#         else:
#             print(f"Unknown key {key}")
#
#
# # ----------------------------------
#
# # Param should be mutable as its not returned.
# # Delta is a function which gives the delta value or value
# def adjuster(param, delta):
#     def adjust_func():
#         delta = delta() if callable(delta) else delta
#         param += delta
#     return adjust_func
#
#
# # Won't work, obviously...
# def setter(param, value):
#     param = value
#
#
# def combine_funcs(f1, f2):
#     return lambda: f1(), f2()
#
# params = {}
# length = lambda: params["value_range"][1][1] - params["value_range"][1][0]
# xy_step_ratio = 1/8
# point_step = 0.5
# xy_scale = 1.1
# resolution_step = 100
#
#
# key_funcs = {
#     "w": adjuster(params["value_range"][1], lambda: -xy_step_ratio * length()),
#     "s": adjuster(params["value_range"][1], lambda: xy_step_ratio * length()),
#     "a": adjuster(params["value_range"][0], lambda: -xy_step_ratio * length()),
#     "d": adjuster(params["value_range"][0], lambda: xy_step_ratio * length()),
#
#     "z": combine_funcs(
#         adjuster(params["value_range"][:, 0], -xy_scale),
#         adjuster(params["value_range"][:, 1], +xy_scale)
#     ),
#     "x": combine_funcs(
#         adjuster(params["value_range"][:, 0], +xy_scale),
#         adjuster(params["value_range"][:, 1], -xy_scale)
#     ),
#     "p": adjuster(params["p"][1], -point_step),
#     ";": adjuster(params["p"][1], point_step),
#     "l": adjuster(params["p"][0], -point_step),
#     "'": adjuster(params["p"][0], point_step),
#
#     "[": adjuster(params["p"][2], point_step),
#     "]": adjuster(params["p"][2], -point_step),
#
#     "r": adjuster(params["resolution"], resolution_step),
#     "e": adjuster(params["resolution"], resolution_step),
#
#     "h": setter ,
# }
#
# # ----------------------------------
