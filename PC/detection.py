import tensorflow as tf
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from object_detection.utils import label_map_util, visualization_utils
import os
from PIL import Image


cone_thresh = 0.85
box_thresh = 0.7
lane_thresh = 0.95
bump_thresh = 0.8
signal_thresh = 0.35
zebra_thresh = 0.75
thresh = 0.35

PATH_TO_SAVED_MODEL = os.path.join(os.getcwd(), "inference_graph","saved_model")
detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)
category_index = label_map_util.create_category_index_from_labelmap(os.path.join(os.getcwd(), "label_map.pbtxt"), use_display_name=True)

def get_coords(detections):
    # This is the way I'm getting my coordinates
    boxes = detections['detection_boxes']
    # get all boxes from an array
    max_boxes_to_draw = boxes.shape[0]
    # get scores to get a threshold
    scores = detections['detection_scores']
    # # iterate over all objects found
    lane_centers = 0
    lane_count = 0
    unoriented_lane = None
    object_ = None
    speedbump = None
    signal = []
    zebra = None

    for i in range(min(max_boxes_to_draw, boxes.shape[0])):
        class_id = int(detections['detection_classes'][i])
        # ID list is in label_map.pbtxt
        # loop assumes only one unoriented lane and only one object detected at a time
        # single object assumption can be dangerous... but no other possible solution in sight
        # should probaby select the object with the lower y value

        if class_id == 3 and scores[i] > lane_thresh:
            if boxes[i][2]-boxes[i][0] < boxes[i][3]-boxes[i][1]:
                unoriented_lane = {
                        "ypos": 1-(boxes[i][2]+boxes[i][0])/2,
                        "xpos": 1-(boxes[i][3]+boxes[i][1])/2,
                        "box":boxes[i].tolist(),
                        "class_name": category_index[class_id]["name"],
                        "score": scores[i]
                    }
            else:
                lane_centers += 1-(boxes[i][3]+boxes[i][1])/2
                lane_count += 1

        elif class_id == 2 and scores[i] > cone_thresh:
            object_ = {
                    "ypos": 1-(boxes[i][2]+boxes[i][0])/2,
                    "xpos": 1-(boxes[i][3]+boxes[i][1])/2,
                    "box":boxes[i].tolist(),
                    "class_name": category_index[class_id]["name"],
                    "score": scores[i]
                }

        elif class_id == 1 and scores[i] > box_thresh:
            object_ = {
                    "ypos": 1-(boxes[i][2]+boxes[i][0])/2,
                    "xpos": 1-(boxes[i][3]+boxes[i][1])/2,
                    "box":boxes[i].tolist(),
                    "class_name": category_index[class_id]["name"],
                    "score": scores[i]
                }
        
        elif class_id == 7 and scores[i] > bump_thresh:
            speedbump = {
                    "ypos": 1-(boxes[i][2]+boxes[i][0])/2,
                    "xpos": 1-(boxes[i][3]+boxes[i][1])/2,
                    "box":boxes[i].tolist(),
                    "class_name": category_index[class_id]["name"],
                    "score": scores[i]
                }
        elif (class_id == 5 or class_id == 6) and scores[i] > signal_thresh:
            signal.append(category_index[class_id]["name"])
        elif class_id == 4 and scores[i] > zebra_thresh:
            zebra = {
                    "ypos": 1-(boxes[i][2]+boxes[i][0])/2,
                    "xpos": 1-(boxes[i][3]+boxes[i][1])/2,
                    "box":boxes[i].tolist(),
                    "class_name": category_index[class_id]["name"],
                    "score": scores[i]
                }
            

    if lane_count == 0:
        return object_, None, unoriented_lane, speedbump, signal, zebra
    lane_disp = lane_centers/lane_count
    return object_, lane_disp, unoriented_lane, speedbump, signal, zebra

def load_image_into_numpy_array(path):
    return np.array(Image.open(path))

def process(image_path, vis=False, pth=""):
    image_np = load_image_into_numpy_array(image_path)

    # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
    input_tensor = tf.convert_to_tensor(image_np)
    # The model expects a batch of images, so add an axis with `tf.newaxis`.
    input_tensor = input_tensor[tf.newaxis, ...]

    detections = detect_fn(input_tensor)

    # All outputs are batches tensors.
    # Convert to numpy arrays, and take index [0] to remove the batch dimension.
    # We're only interested in the first num_detections.
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                for key, value in detections.items()}
    detections['num_detections'] = num_detections

    # detection_classes should be ints.
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    if vis:
        label_id_offset = 1 
        impop = load_image_into_numpy_array(image_path)
        visualization_utils.visualize_boxes_and_labels_on_image_array(impop,
                detections['detection_boxes'],
                (detections['detection_classes']).astype(int),
                detections['detection_scores'],
                category_index,
                use_normalized_coordinates=True,
                max_boxes_to_draw=200,
                min_score_thresh=thresh,
                agnostic_mode=False)
        im = Image.fromarray(impop)
        im.save(pth)
    
    return get_coords(detections)

if __name__ == "__main__":
    for i in range(0,66):
        try:
            print(i, process(rf"C:\Users\moham\OneDrive\Desktop\auto rc car\PC\outputimages\1677745162.9212718\{i}-Base.jpg", True, rf"C:\Users\moham\OneDrive\Desktop\auto rc car\PC\processed\{i}-Base.jpg"))
        except:
            pass
