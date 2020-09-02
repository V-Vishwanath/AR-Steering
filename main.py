import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


import cv2
from imutils import rotate
from imutils.video import WebcamVideoStream

from tensorflow.config.experimental import list_physical_devices
from tensorflow.config.experimental import set_memory_growth

from utils import *


def main():
    print('[INFO] Loading model...')
    model, time_taken = load_hand_model()
    print(f'[INFO] Loaded model in {time_taken:.2f}s')

    wheel = cv2.resize(cv2.imread('data/wheel.png', -1), (265, 265))

    forward_gear = cv2.resize(cv2.imread('data/gear-rod/forward.png', -1), (60, 300))
    normal_gear = cv2.resize(cv2.imread('data/gear-rod/normal.png', -1), (60, 300))
    reverse_gear = cv2.resize(cv2.imread('data/gear-rod/reverse.png', -1), (60, 300))

    current_gear = forward_gear
    
    src = WebcamVideoStream().start()
    trackers = None
    frame_count = 1

    while True:
        start = time()

        frame = cv2.flip(src.read(), 1)
        centroids = []

        if frame_count == 7: 
            trackers = None 
            frame_count = 1

        if trackers:
            ret, boxes = trackers.update(frame)
            for box in boxes:
                x, y, w, h = [int(coord) for coord in box]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 1)

                cx, cy = (x + w//2), (y + h//2)
                cv2.circle(frame, (cx, cy), 3, (0, 255, 0), -1)
                centroids.append((cx, cy))

            frame_count += 1

        else:
            img_vector = cv2.resize(frame, (320, 320))[..., ::-1]
            img_vector = img_vector[newaxis, ...] / 255

            predictions = model(img_vector, training=False).numpy()

            num_det, boxes = locate_hands(predictions, frame.shape[:2])

            if num_det > 0:
                trackers = cv2.MultiTracker_create()
                for i in range(num_det):
                    y1, x1, y2, x2 = boxes[i]
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    cv2.circle(frame, (cx, cy), 3, (0, 255, 0), -1)
                    centroids.append((cx, cy))

                    trackers.add(cv2.TrackerKCF_create(), frame, (x1, y1, x2-x1, y2-y1))


        if len(centroids) > 1:
            right, left = (0, 1) if centroids[0][0] > centroids[1][0] else (1, 0)
            angle = int((centroids[left][1] - centroids[right][1]) / 4)

            left = centroids[left]
            right = centroids[right]

            if 20 <= left[0] <= 100:
                if left[1] <= 130:
                    current_gear = forward_gear
                    print('FORWARD', end='\r')

                elif 140 <= left[1] <= 340:
                    current_gear = normal_gear
                    print('NORMAL', end='\r')

                else:
                    current_gear = reverse_gear
                    print('REVERSE', end='\r')

        else:
            angle = 0

        overlay(frame, rotate(wheel, angle), current_gear)
        
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) == 27: break

        # print(f'[INFO] FPS : {1 / (time() - start):.2f}', end='\r')
        

    src.stop()
    cv2.destroyAllWindows()


devices = list_physical_devices('GPU')
if len(devices) > 0: set_memory_growth(devices[0], True)

main()