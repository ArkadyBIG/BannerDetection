#%%
import matplotlib.pyplot as plt
import cv2
import numpy as np
from tqdm import tqdm
import imutils
from time import time, sleep
import json
from datetime import timedelta, datetime
import streamlink


#%%
banner = cv2.imread('banner.jpg')
banner_gray = cv2.cvtColor(banner, cv2.COLOR_BGR2GRAY)
banner_gray = imutils.resize(banner_gray, width=int(banner_gray.shape[1] * 0.7))
banner_edges = cv2.Canny(banner_gray, 50, 200)
plt.imshow(banner_gray)
ght = cv2.createGeneralizedHoughBallard()
ght.setTemplate(banner_gray)
ght.setLevels(360)
ght.setDp(2)
ght.setVotesThreshold(60)
#%%


(tH, tW) = banner_edges.shape[:2]
def detect(frame, do_nms=True):
    boxes = []
    scores = []
    scales = []
    _range = np.linspace(0.8, 1.2, 20)
    for scale in (_range):
        resized = imutils.resize(frame, width=int(frame.shape[1] * scale))
        # _start = time()
        positions = ght.detect(resized)
        # print('Houg:', time() - _start)
        if positions[0] is not None:
            votes = positions[1].reshape(-1, 3)[:, 0]
            scores.extend(votes)
            scales.append(scale)
            center_x = positions[0].reshape(-1, 4)[:, 0]
            center_y = positions[0].reshape(-1, 4)[:, 1]
            
            curboxes = np.array([center_x - tW / 2, center_y - tH / 2,  center_x + tW / 2, center_y + tH / 2])
            curboxes = curboxes.transpose((1, 0)) / scale
            boxes.extend(curboxes)
    if do_nms:
        boxes, scores = nms(boxes, scores)
    return boxes, scores, scales

#%%
streams = streamlink.streams('https://www.twitch.tv/tarik')
url = streams['1080p60'].url
pipeline = f'souphttpsrc location={url} ! decodebin ! videoconvert ! appsink max-buffers=1 drop=true'
cap = cv2.VideoCapture(pipeline)
#%%
time_steps = []
for i in tqdm(range(1_000)):
    ret, frame = cap.read()
    continue
    frame = imutils.resize(frame, width=640)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    boxes, scores, scales = detect(frame_gray)
    time_steps.append((str(datetime.now()), bool(boxes)))

    for box in boxes:
        x1, y1, x2, y2 = box.astype(int)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255))
    plt.imshow(frame)
    plt.show()
    sleep(1)

# %%
sum((t[1] for t in time_steps)) / len(time_steps)

# %%
pattern = "%Y-%m-%d %H:%M:%S.%f"
delta = datetime.strptime(time_steps[-1][0], pattern) - datetime.strptime(time_steps[0][0], pattern)

# %%
