import os
import cv2
import time
import numpy as np
from mss import mss
from datetime import datetime

from src.utils import files, screen
from src.detector import FearDetector
from src import DIR_SCREEN, DIR_WEBCAM

# Parameters from ENV:
DELAY_BETWEEN_SCREENSHOTS = float(os.getenv('DELAY_BETWEEN_SCREENSHOTS', 3.0))
FEAR_BUFFER_SECONDS = float(os.getenv('FEAR_BUFFER_SECONDS', 0.5))
SAVE_SCREENSHOTS_WITH_BOXES = os.getenv('SAVE_SCREENSHOTS_WITH_BOXES', 'True').lower() in ('true', '1', 'yes')


if __name__ == '__main__':
    # Init cam:
    cap = cv2.VideoCapture(0)
    sct = mss()

    # Init fear detector:
    detector = FearDetector()

    session_name = datetime.now().strftime('%Y%m%d-%H%M%S')
    files.mkdir(path=DIR_SCREEN/session_name)
    files.mkdir(path=DIR_WEBCAM/session_name)

    last_fear_time = 0
    fear_active = False
    fear_detected_since = None
    while True:
        ret, frame_cam = cap.read()
        if not ret:
            break

        # Detect screen:
        screen_image = np.array(object=sct.grab(sct.monitors[1]))[..., :3]

        # Detect fear emotion:
        found_fear_boxes = detector.detect(frame=frame_cam)
        current_time = time.time()
        if len(found_fear_boxes) > 0:
            if fear_detected_since is None:
                fear_detected_since = current_time
            elif current_time - fear_detected_since >= FEAR_BUFFER_SECONDS:
                if not fear_active:
                    # First emotion - make screenshots:
                    screen.take_screenshots(
                        frame_cam=frame_cam,
                        frame_screen=screen_image,
                        session_name=session_name,
                        boxes=found_fear_boxes,
                        save_with_boxes=SAVE_SCREENSHOTS_WITH_BOXES,
                    )
                    fear_active = True
                    last_fear_time = current_time
                elif current_time - last_fear_time >= DELAY_BETWEEN_SCREENSHOTS:
                    # Emotion keeps - make screenshots again:
                    screen.take_screenshots(
                        frame_cam=frame_cam,
                        frame_screen=screen_image,
                        session_name=session_name,
                        boxes=found_fear_boxes,
                        save_with_boxes=SAVE_SCREENSHOTS_WITH_BOXES,
                    )
                    last_fear_time = current_time
        else:
            fear_detected_since = None
            fear_active = False

        # Video in the window from webcam:
        screen.add_box_on_screen(frame_cam=frame_cam, found_boxes=found_fear_boxes)
        cv2.imshow(winname='Webcam', mat=frame_cam)
        if cv2.waitKey(delay=1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
