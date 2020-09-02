from time import time
from tensorflow import function
from numpy import array, newaxis
from tensorflow.keras.models import model_from_json
from tensorflow.image import combined_non_max_suppression as NMS


def load_hand_model(path='data/hand-model'):
    start = time()

    with open(f'{path}/hands.json') as f:
        model = model_from_json(f.read())

    model.load_weights(f'{path}/hands.h5')
    model.call = function(model.call)

    return model, time() - start


def locate_hands(predictions, size):
    boxes = predictions[:, :, :4][..., newaxis, :]
    confs = predictions[:, :, 4:]

    boxes, _, _, detections = NMS(
        boxes=boxes,
        scores=confs,
        max_output_size_per_class=5,
        max_total_size=5,
        iou_threshold=0.45,
        score_threshold=0.7
    )

    num_det = int(detections[0])

    scaling_vector = array(size * 2)
    boxes = (boxes.numpy()[0] * scaling_vector).astype(int)

    return num_det, boxes[:num_det]


def overlay(frame, wheel, gear):
    wheel_alpha = (wheel[:, :, 3] / 255)[:, :, newaxis, ...]
    gear_alpha = (gear[:, :, 3] / 255)[:, :, newaxis, ...]

    frame[108:373, 188:453, :] = wheel_alpha * wheel[:, :, :3] + (1 - wheel_alpha) * frame[108:373, 188:453, :]
    frame[100:400, 30:90, :] = gear_alpha * gear[:, :, :3] + (1 - gear_alpha) * frame[100:400, 30:90, :]


