import cv2
import time
import argparse
import numpy as np
from mss import mss
from datetime import datetime

from src.utils import files, screen
from src.detector import FearDetector
from src import DIR_SCREEN, DIR_WEBCAM


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Parse arguments for Fear Demo App.')
    parser.add_argument(
        '--delay_between_screenshots',
        default=3.0,
        type=float,
        required=False,
        help='Delay between screenshots for doing next screenshot after first.',
    )
    parser.add_argument(
        '--fear_buffer_seconds',
        default=0.5,
        type=float,
        required=False,
        help='Time for stable fear emotion detection (after time of stable detection make first screenshot).',
    )
    parser.add_argument(
        '--save_screenshots_with_boxes',
        default=True,
        type=bool,
        required=False,
        help='Save screenshots with detected emotion boxes.',
    )
    parser.add_argument(
        '--show_webcam_win',
        default=True,
        type=bool,
        required=False,
        help='Show webcam window while app is running.',
    )
    return parser.parse_args()


if __name__ == '__main__':
    # Parse arguments:
    args = parse_args()

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
            elif current_time - fear_detected_since >= args.fear_buffer_seconds:
                if not fear_active:
                    # First emotion - make screenshots:
                    screen.take_screenshots(
                        frame_cam=frame_cam,
                        frame_screen=screen_image,
                        session_name=session_name,
                        boxes=found_fear_boxes,
                        save_with_boxes=args.save_screenshots_with_boxes,
                    )
                    fear_active = True
                    last_fear_time = current_time
                elif current_time - last_fear_time >= args.delay_between_screenshots:
                    # Emotion keeps - make screenshots again:
                    screen.take_screenshots(
                        frame_cam=frame_cam,
                        frame_screen=screen_image,
                        session_name=session_name,
                        boxes=found_fear_boxes,
                        save_with_boxes=args.save_screenshots_with_boxes,
                    )
                    last_fear_time = current_time
        else:
            fear_detected_since = None
            fear_active = False

        # Video in the window from webcam:
        if args.show_webcam_win:
            screen.add_box_on_screen(frame_cam=frame_cam, found_boxes=found_fear_boxes)
            cv2.imshow(winname='Webcam', mat=frame_cam)
            if cv2.waitKey(delay=1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
