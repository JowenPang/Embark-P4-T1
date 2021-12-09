import cv2
import pandas as pd
from vehicle_detector import VehicleDetector

# Load vehicle detector
vd = VehicleDetector()

SIZE = 480
img_path = r'images/train/Mitsubishi Lancer Sedan 2013/00747.jpg'
img = cv2.imread(img_path)
img = cv2.resize(img, (SIZE,SIZE))

vehicle_boxes = vd.detect_vehicles(img)

for box in vehicle_boxes:
    x, y, w, h, = box
    area = w*h
    print(f"top left coordinate is ({x},{y}) and area is {area}")
    cv2.rectangle(img, (x, y), (x+w, y+h), (25, 0, 180), 3)

# declaring global variables (are used later on)
r = g = b = 0

cx = int(x + (w/2))
cy = int(y + (h/2))

# Pick pixel value
pixel_center = img[cy, cx]
b, g, r = int(pixel_center[0]), int(pixel_center[1]), int(pixel_center[2])

# Reading csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('10colors.txt', names=index, header=None)

# function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    minimum = 500
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

print("The colour of this car is ", get_color_name(r,g,b))

while True:
    cv2.rectangle(img, (20, 20), (200, 60), (255, 255, 255), -1)
    cv2.putText(img, get_color_name(r,g,b), (40, 45), 2, 0.7, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.circle(img, (cx, cy), 5, (25, 25, 25), 3)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
        break