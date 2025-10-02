from __future__ import annotations
import base64
from typing import Optional, Tuple, List
import numpy as np
import cv2
from fer import FER


class AttentionDetector:
    def __init__(self) -> None:
        # FER uses MTCNN/cascade internally to detect faces
        self._fer = FER(mtcnn=True)

    @staticmethod
    def _decode_image(image_base64: str) -> np.ndarray:
        data = base64.b64decode(image_base64)
        nparr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img

    def analyze(self, image_base64: str) -> Tuple[bool, Optional[str], Optional[float]]:
        img = self._decode_image(image_base64)
        results: List[dict] = self._fer.detect_emotions(img)
        if not results:
            return False, None, None
        # Use the first face
        emotions = results[0].get("emotions", {})
        if not emotions:
            return True, None, None
        emotion = max(emotions, key=emotions.get)
        confidence = float(emotions.get(emotion, 0.0))
        attention = True  # face present implies looking-ish; frontality is not guaranteed
        return attention, emotion, confidence


detector = AttentionDetector()
