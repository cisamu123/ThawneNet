
#  _______ _                               _   _ ______ _______
# |__   __| |                             | \ | |  ____|__   __|
#    | |  | |__   __ ___      ___ __   ___|  \| | |__     | |
#    | |  | '_ \ / _` \ \ /\ / / '_ \ / _ \ . ` |  __|    | |
#    | |  | | | | (_| |\ V  V /| | | |  __/ |\  | |____   | |
#    |_|  |_| |_|\__,_| \_/\_/ |_| |_|\___|_| \_|______|  |_|
#                                        - By Cisamu

import cv2
def list_available_cameras():
    index = 0
    cameras = []
    while True:
        capture = cv2.VideoCapture(index)
        if not capture.read()[0]:
            break
        camera_name = capture.getBackendName()
        camera_info = {
            'index': index,
            'name': camera_name,
            'fps': capture.get(cv2.CAP_PROP_FPS),
            'width': capture.get(cv2.CAP_PROP_FRAME_WIDTH),
            'height': capture.get(cv2.CAP_PROP_FRAME_HEIGHT),
        }
        cameras.append(camera_info)
        capture.release()
        index += 1
    return cameras