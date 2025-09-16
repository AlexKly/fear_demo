import cv2
import time
import numpy as np
from typing import Any

from src import DIR_SCREEN, DIR_WEBCAM


def add_box_on_screen(frame_cam: np.ndarray, found_boxes: list[dict[str, Any]]) -> None:
    if len(found_boxes) > 0:
        for face in found_boxes:
            x, y, w, h = face['box']
            prob = face['probability']
            cv2.rectangle(img=frame_cam, pt1=(x, y), pt2=(x + w, y + h), color=(0, 0, 255), thickness=2)
            cv2.putText(
                img=frame_cam,
                text=f'Probability: {prob: .2f}',
                org=(x, y - 10),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.7,
                color=(0, 0, 255),
                thickness=2,
            )


def take_screenshots(
        frame_cam: np.ndarray,
        frame_screen: np.ndarray,
        session_name: str,
        boxes: list[dict[str, Any]] = None,
        save_with_boxes: bool = True,
) -> None:
    timestamp = int(time.time())

    frame_cam_copy = frame_cam.copy()
    if save_with_boxes and boxes:
        add_box_on_screen(frame_cam_copy, found_boxes=boxes)

    cv2.imwrite(filename=DIR_SCREEN/session_name/f'{timestamp}.png', img=frame_screen)
    cv2.imwrite(filename=DIR_WEBCAM/session_name/f'{timestamp}.png', img=frame_cam_copy)
