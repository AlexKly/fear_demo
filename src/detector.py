import numpy as np
from fer import FER
from typing import Any


class FearDetector:
    def __init__(self, threshold: float = 0.5) -> None:
        self.detector = FER(mtcnn=False)
        self.threshold = threshold
        self._emotion = 'fear'

    def detect(self, frame: np.ndarray) -> list[dict[str, Any]]:
        results = list()
        emotions = self.detector.detect_emotions(img=frame)
        if emotions:
            for face in emotions:
                if face['emotions'][self._emotion] > self.threshold:
                    results += [{
                        'box': face['box'],
                        'probability': face['emotions'][self._emotion],
                    }]
        return results
