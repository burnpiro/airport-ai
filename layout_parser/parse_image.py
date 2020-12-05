import cv2
import json
import uuid
import glob
import os

import numpy as np
from no_indent import NoIndent, NoIndentEncoder

COLORS = os.getenv("OBJECT_COLORS")
# COLORS = "248,206,204 restaurant;218,232,252 shop;213,232,212 general;225,213,231 services;204,204,204 route"
# COLORS_HSV = '2.7,17.7,97.3 restaurant;215.3,13.5,98.8 shop;117,8.6,91 general;280,7.8,90.6 services;0,0,80 route'


def filter_min_contour(contours):
    eps = 5
    filtered = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > eps:
            filtered.append(contour)

    return filtered


def contour_to_list(cnt: list):
    out = []
    for point in cnt:
        out.append([int(point[0][0]), int(point[0][1])])

    return out


def parse_objects(img: np.ndarray):
    object_colors = list(map(lambda x: x.split(" "), COLORS.split(";")))

    items = {}
    for object_color in object_colors:
        color = list(map(lambda x: float(x), object_color[0].split(",")))
        low_b = (color[2] - 1, color[1] - 1, color[0] - 1)
        up_b = (color[2] + 1, color[1] + 1, color[0] + 1)
        mask = cv2.inRange(img, low_b, up_b)
        contours, hierarchy = cv2.findContours(
            mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
        )
        filtered = filter_min_contour(contours)
        items[object_color[1]] = {
            "points": filtered,
            "ids": list(map(lambda x: uuid.uuid4().hex, filtered)),
            "color": "#%02x%02x%02x" % (int(color[0]), int(color[1]), int(color[2])),
        }

    return items


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


for file in glob.glob("/in/*"):
    name = file.split("/")[-1]
    print(f"Processing image {name} ...")
    originalImage = cv2.imread(file)

    cnt = parse_layout(originalImage)
    objects = parse_objects(originalImage)

    for idx, item in objects.items():
        canv = originalImage.copy()
        cv2.drawContours(canv, item["points"], -1, (0, 0, 255), 3)
        cv2.imwrite(f"out/{idx}-{name}", canv)

    cv2.drawContours(originalImage, [cnt], 0, (0, 0, 255), 3)
    # cv2.imshow('img1', originalImage)
    # cv2.waitKey()
    cv2.imwrite(f"/out/layout-{name}", originalImage)

    out = {
        "contour": NoIndent(contour_to_list(cnt)),
        "objects": {
            k: {
                "points": NoIndent(list(map(contour_to_list, v["points"]))),
                "ids": NoIndent(v["ids"]),
                "color": v["color"],
            }
            for k, v in objects.items()
        },
        "image-size": [originalImage.shape[1], originalImage.shape[0]],
    }

    with open(f"/out/{name}.json", "w") as write_file:
        write_file.write(json.dumps(out, indent=2, sort_keys=True, cls=NoIndentEncoder))
