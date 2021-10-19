from __future__ import print_function
import numpy as np
import cv2

def draw_box_and_landmarks_detections(img_raw, dets, vis_thres, w, h):
    for b in dets:
        if b[4] < vis_thres:
            continue
        if b[2] - b[0] < w or b[3] - b[1] < h:
            continue
        text = "{:.4f}".format(b[4])
        b = list(map(int, b))
        cv2.rectangle(img_raw, (b[0], b[1]), (b[2], b[3]), (0, 0, 255), 2)
        cx = b[0]
        cy = b[1] + 12
        cv2.putText(img_raw, text, (cx, cy),
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))

        # landms
        cv2.circle(img_raw, (b[5], b[6]), 1, (0, 0, 255), 4)
        cv2.circle(img_raw, (b[7], b[8]), 1, (0, 255, 255), 4)
        cv2.circle(img_raw, (b[9], b[10]), 1, (255, 0, 255), 4)
        cv2.circle(img_raw, (b[11], b[12]), 1, (0, 255, 0), 4)
        cv2.circle(img_raw, (b[13], b[14]), 1, (255, 0, 0), 4)
    return img_raw


def convert_detection_to_tracker(dets, vis_thres, w, h):
    detections = np.empty((0,5))
    facial_landmarks = []
    for b in dets:
        if b[4] < vis_thres:
            continue
        if b[2] - b[0] < w or b[3] - b[1] < h:
            continue
        detections = np.append(detections, np.array([[b[0], b[1], b[2], b[3], b[4]]]), axis=0)
        facial_landmarks.append([[b[5],b[6]], [b[7],b[8]], [b[9],b[10]], [b[11],b[12]], [b[13],b[14]]])
    return detections, facial_landmarks


def draw_box_resort_trackers(img_raw, trackers):
    for tracker in trackers:
        x1, y1, x2, y2 = int(float(tracker[0])), int(float(tracker[1])), int(float(tracker[2])), int(float(tracker[3]))
        id = str(int(float(tracker[-3]))) + '_' + str(tracker[-1])

        cv2.rectangle(img_raw, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(img_raw, id, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
    return img_raw
    

def draw_box_sort_trackers(img_raw, trackers):
    for tracker in trackers:
        x1, y1, x2, y2 = int(float(tracker[0])), int(float(tracker[1])), int(float(tracker[2])), int(float(tracker[3]))
        id = str(int(float(tracker[-1])))
        cv2.rectangle(img_raw, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(img_raw, id, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
    return img_raw


def draw_box_deepsort_trackers(img_raw, trackers, detections_class):
    if trackers is None or detections_class is None:
        return img_raw
    for track in trackers.tracks:
        if not track.is_confirmed() or track.time_since_update > 1:
            continue
        bbox = track.to_tlbr() 
        id_num = str(track.track_id)
        x1, y1, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        cv2.rectangle(img_raw, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(img_raw, id_num, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
    return img_raw