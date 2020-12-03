import cv2
import json
import glob

for file in glob.glob("/in/*"):
    name = file.split("/")[-1]
    print(f"Processing image {name} ...")
    originalImage = cv2.imread(file)
    grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    thresh, blackAndWhiteImage = cv2.threshold(grayImage, 250, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(
        blackAndWhiteImage, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
    )

    cnt = contours[-1]

    cv2.drawContours(originalImage, [cnt], 0, (0, 0, 255), 1)
    cv2.imwrite(f"/out/with-cnt-{name}", originalImage)

    out = {"contour": []}

    for point in cnt:
        out["contour"].append([int(point[0][0]), int(point[0][1])])

    with open(f"/out/{name}.json", "w") as write_file:
        json.dump(out, write_file)
