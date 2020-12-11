import cv2
import json
import uuid
import glob
import os

import numpy as np
from absl import app, flags
from absl.flags import FLAGS
from no_indent import NoIndent, NoIndentEncoder

# COLORS = os.getenv("OBJECT_COLORS")
# COLORS_HSV = '2.7,17.7,97.3 restaurant;215.3,13.5,98.8 shop;117,8.6,91 general;280,7.8,90.6 services;0,0,80 route'
# SMALL_ITEMS = os.getenv("ITEMS_COLORS")
# SMALL_ITEMS = "0,0,0 planes;208,198,166 chair;221,221,221 lines"


def filter_min_contour(contours, max_eps, eps=5.0, debug=False):
    filtered = []
    for contour in contours:
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        area = cv2.contourArea(box)
        if debug:
            print(area, box)
        if max_eps is not None and area > max_eps:
            continue
        if area > eps:
            filtered.append(contour)

    return filtered


def contour_to_list(cnt: list):
    out = []
    for point in cnt:
        out.append([int(point[0][0]), int(point[0][1])])

    return out


def split_obj_def(str_def: str):
    """
    :param str_def: R,G,B name fill min_size max_size
    :return: dict
    {
        "color": [R,G,B],
        "name": str,
        "should_fill": boolean,
        "min": int (px) or None,
        "max": int (px) or None
    }
    """
    result = {
        "color": [],
        "name": "",
        "should_fill": True,
        "min": None,
        "max": None
    }
    parts = str_def.split(" ")
    result["color"] = list(map(lambda x: float(x), parts[0].split(",")))
    result["name"] = parts[1]
    result["should_fill"] = False if len(parts) > 2 and parts[2] == "nofill" else True
    result["min"] = int(parts[3]) if len(parts) > 3 and parts[3] not in ["none", "None"] else None
    result["max"] = int(parts[4]) if len(parts) > 4 else None
    return result



def parse_objects(img: np.ndarray, colors, eps=0.01, max_eps=1.0):
    objects_def = list(map(lambda x: split_obj_def(x), colors.split(";")))
    area = img.shape[0] * img.shape[1]

    items = {}
    for object_def in objects_def:
        color = object_def["color"]
        low_b = (
            color[2] - 1 if color[2] - 1 > 0 else 0,
            color[1] - 1 if color[1] - 1 > 0 else 0,
            color[0] - 1 if color[0] - 1 > 0 else 0,
        )
        up_b = (
            color[2] + 1 if color[2] + 1 < 255 else 255,
            color[1] + 1 if color[1] + 1 < 255 else 255,
            color[0] + 1 if color[0] + 1 < 255 else 555,
        )
        mask = cv2.inRange(img, low_b, up_b)
        contours, hierarchy = cv2.findContours(
            mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
        )
        min_area = eps * area if object_def["min"] is None else object_def["min"]
        max_area = max_eps * area if object_def["max"] is None else object_def["max"]
        filtered = filter_min_contour(contours, eps=min_area, max_eps=max_area)
        items[object_def["name"]] = {
            "points": filtered,
            "ids": list(map(lambda x: uuid.uuid4().hex, filtered)),
            "fill": object_def["should_fill"],
            "color": "#%02x%02x%02x" % (int(color[0]), int(color[1]), int(color[2])),
        }

    return items


# def parse_items(img: np.ndarray):
#     hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
#
#     object_colors = list(map(lambda x: x.split(" "), SMALL_ITEMS.split(";")))
#
#     items = {}
#     for object_color in object_colors:
#         color = list(map(lambda x: float(x), object_color[0].split(",")))
#         low_b = (color[2] - 1, color[1] - 1, color[0] - 1)
#         up_b = (color[2] + 1, color[1] + 1, color[0] + 1)
#         color_hsv = cv2.cvtColor(
#             np.uint8([[[color[2], color[1], color[0]]]]), cv2.COLOR_BGR2HSV
#         )
#         low_b = np.array([
#             color_hsv[0][0][0] - 10 if color_hsv[0][0][0] - 10 > 0 else 0,
#             color_hsv[0][0][1] - 5 if color_hsv[0][0][1] - 5 > 0 else 0,
#             color_hsv[0][0][2] - 10 if color_hsv[0][0][2] - 10 > 0 else 0,
#         ])
#         up_b = np.array([
#             color_hsv[0][0][0] + 50 if color_hsv[0][0][0] + 50 < 360 else 360,
#             color_hsv[0][0][1] + 5 if color_hsv[0][0][1] + 5 < 255 else 255,
#             color_hsv[0][0][2] + 10 if color_hsv[0][0][2] + 10 < 255 else 255,
#         ])
#         # print(color)
#         # print(color_hsv)
#         # print(low_b)
#         # print(up_b)
#         mask = cv2.inRange(img, low_b, up_b)
#         # cv2.imshow(object_color[1], mask)
#         # cv2.waitKey()
#         contours, hierarchy = cv2.findContours(
#             mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
#         )
#         filtered = filter_min_contour(contours, eps=2)
#         items[object_color[1]] = {
#             "points": filtered,
#             "ids": list(map(lambda x: uuid.uuid4().hex, filtered)),
#             "color": "#%02x%02x%02x" % (int(color[0]), int(color[1]), int(color[2])),
#         }
#
#     return items


def parse_layout(img: np.ndarray):
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh, blackAndWhiteImage = cv2.threshold(grayImage, 250, 255, cv2.THRESH_BINARY)
    # cv2.imshow('BW', blackAndWhiteImage)

    contours, hierarchy = cv2.findContours(
        blackAndWhiteImage, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
    )

    longest = (0, 0)
    for i, ct in enumerate(contours):
        if ct.shape[0] > longest[1]:
            longest = (i, ct.shape[0])

    return contours[longest[0]]


flags.DEFINE_string(
    "objects",
    "248,206,204 restaurant;218,232,252 shop;213,232,212 general;225,213,231 services;204,204,204 route;0,0,0 planes",
    "List of `R,G,B object_name` paris separated by `;`",
)
flags.DEFINE_string(
    "small_objects",
    "0,0,0 chair;221,221,221 lines",
    "List of `R,G,B object_name` paris separated by `;`",
)
flags.DEFINE_string(
    "eps_large",
    "0.0001",
    "min percent of an image that has to be covered by the standard object",
)
flags.DEFINE_string(
    "eps_small",
    "0.0",
    "min percent of an image that has to be covered by the small object",
)


def main(_argv):
    if type(os.getenv("OBJECT_COLORS")) == str and len(os.getenv("OBJECT_COLORS")) > 0:
        FLAGS.objects = os.getenv("OBJECT_COLORS")
    if type(os.getenv("SMALL_ITEMS")) == str and len(os.getenv("SMALL_ITEMS")) > 0:
        FLAGS.small_objects = os.getenv("SMALL_ITEMS")
    if type(os.getenv("OBJECTS_EPS")) == float:
        FLAGS.eps_large = os.getenv("OBJECTS_EPS")
    if type(os.getenv("SMALL_ITEMS_EPS")) == float:
        FLAGS.eps_small = os.getenv("SMALL_ITEMS_EPS")

    for file in glob.glob("in/*"):
        name = file.split("/")[-1]
        print(f"Processing image {name} ...")
        originalImage = cv2.imread(file)

        cnt = parse_layout(originalImage)
        objects = parse_objects(originalImage, FLAGS.objects, eps=float(FLAGS.eps_large))
        small_items = parse_objects(originalImage, FLAGS.small_objects, eps=float(FLAGS.eps_small), max_eps=float(FLAGS.eps_large))

        for idx, item in objects.items():
            canv = originalImage.copy()
            cv2.drawContours(canv, item["points"], -1, (0, 0, 255), 3)
            cv2.imwrite(f"out/{idx}-{name}", canv)

        for idx, item in small_items.items():
            canv = originalImage.copy()
            cv2.drawContours(canv, item["points"], -1, (0, 0, 255), 3)
            cv2.imwrite(f"out/{idx}-{name}", canv)

        cv2.drawContours(originalImage, [cnt], 0, (0, 0, 255), 3)
        # cv2.imshow('img1', originalImage)
        # cv2.waitKey()
        cv2.imwrite(f"out/layout-{name}", originalImage)

        out = {
            "contour": NoIndent(contour_to_list(cnt)),
            "objects": {
                k: {
                    "points": NoIndent(list(map(contour_to_list, v["points"]))),
                    "ids": NoIndent(v["ids"]),
                    "fill": v["fill"],
                    "color": v["color"],
                }
                for k, v in objects.items()
            },
            "items": {
                k: {
                    "points": NoIndent(list(map(contour_to_list, v["points"]))),
                    "ids": NoIndent(v["ids"]),
                    "fill": v["fill"],
                    "color": v["color"],
                }
                for k, v in small_items.items()
            },
            "image-size": [originalImage.shape[1], originalImage.shape[0]],
        }

        with open(f"out/{name}.json", "w") as write_file:
            write_file.write(
                json.dumps(out, indent=2, sort_keys=True, cls=NoIndentEncoder)
            )


if __name__ == "__main__":
    try:
        app.run(main)
    except SystemExit:
        pass
