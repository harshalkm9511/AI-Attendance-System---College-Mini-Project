from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


DeepFace = None
DEEPFACE_IMPORT_ATTEMPTED = False


def get_deepface():
    global DeepFace, DEEPFACE_IMPORT_ATTEMPTED
    if DEEPFACE_IMPORT_ATTEMPTED:
        return DeepFace
    DEEPFACE_IMPORT_ATTEMPTED = True
    try:  
        from deepface import DeepFace as deepface_module
    except Exception:
        DeepFace = None
    else:
        DeepFace = deepface_module
    return DeepFace


@dataclass
class QualityReport:
    is_usable: bool
    message: str
    score: float
    face_count: int
    blur_score: float
    brightness: float


class RecognitionEngine:
    def __init__(self, storage_dir: Path):
        self.storage_dir = Path(storage_dir)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.deepface_available = self._check_deepface_assets()

    def _check_deepface_assets(self) -> bool:
        weights = Path.home() / ".deepface" / "weights" / "facenet_weights.h5"
        if not weights.exists():
            return False
        if weights.stat().st_size <= 1_000_000:
            return False
        return get_deepface() is not None

    def detect_faces(self, image_bgr: np.ndarray, min_size=(60, 60)) -> list[tuple[int, int, int, int]]:
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=min_size)
        if faces is None:
            return []
        return [tuple(int(v) for v in face) for face in faces]

    def crop_face(self, image_bgr: np.ndarray, box: tuple[int, int, int, int], padding: int = 28) -> np.ndarray:
        x, y, w, h = box
        x1 = max(x - padding, 0)
        y1 = max(y - padding, 0)
        x2 = min(x + w + padding, image_bgr.shape[1])
        y2 = min(y + h + padding, image_bgr.shape[0])
        return image_bgr[y1:y2, x1:x2]

    def annotate_image(self, image_bgr: np.ndarray, boxes: list[tuple[int, int, int, int]]) -> np.ndarray:
        annotated = image_bgr.copy()
        for index, (x, y, w, h) in enumerate(boxes, start=1):
            cv2.rectangle(annotated, (x, y), (x + w, y + h), (30, 144, 255), 2)
            cv2.putText(annotated, f"Face {index}", (x, max(20, y - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (30, 144, 255), 2)
        return annotated

    def assess_enrollment_image(self, image_bgr: np.ndarray) -> QualityReport:
        faces = self.detect_faces(image_bgr, min_size=(40, 40))
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        brightness = float(gray.mean())

        if len(faces) == 0:
            return QualityReport(False, "No clear face detected in the uploaded image.", 0, 0, blur_score, brightness)
        if len(faces) > 1:
            return QualityReport(False, "Multiple faces detected. Upload a single-student image.", 0, len(faces), blur_score, brightness)
        if blur_score < 45:
            return QualityReport(False, "Image is too blurry for reliable enrollment.", 0.25, len(faces), blur_score, brightness)
        if brightness < 35:
            return QualityReport(False, "Image is too dark. Use a brighter photo.", 0.35, len(faces), blur_score, brightness)

        score = min(1.0, 0.55 + min(blur_score, 180) / 300 + min(brightness, 180) / 500)
        return QualityReport(True, "Image quality looks good for enrollment.", score, len(faces), blur_score, brightness)

    def build_embedding(self, image_bgr: np.ndarray) -> tuple[np.ndarray, str]:
        if self.deepface_available:
            try:
                rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
                result = DeepFace.represent(
                    img_path=rgb,
                    model_name="Facenet",
                    detector_backend="opencv",
                    enforce_detection=False,
                )
                if result:
                    return np.array(result[0]["embedding"], dtype=np.float32), "deepface_facenet"
            except Exception:
                pass
        return self._build_local_descriptor(image_bgr), "local_descriptor_v2"

    def _build_local_descriptor(self, image_bgr: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (96, 96))
        gray = cv2.equalizeHist(gray)

        hist = cv2.calcHist([gray], [0], None, [32], [0, 256]).flatten()
        hist = hist / (np.linalg.norm(hist) + 1e-6)

        gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        magnitude, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)

        orientation_bins = np.zeros(16, dtype=np.float32)
        bin_index = np.floor(angle / 22.5).astype(int) % 16
        for idx in range(16):
            orientation_bins[idx] = float(magnitude[bin_index == idx].sum())
        orientation_bins = orientation_bins / (np.linalg.norm(orientation_bins) + 1e-6)

        blocks = cv2.resize(gray, (24, 24)).astype(np.float32).flatten() / 255.0
        blocks = blocks - blocks.mean()
        blocks = blocks / (np.linalg.norm(blocks) + 1e-6)

        descriptor = np.concatenate([hist, orientation_bins, blocks]).astype(np.float32)
        descriptor = descriptor / (np.linalg.norm(descriptor) + 1e-6)
        return descriptor

    def similarity(self, embedding_a: np.ndarray, embedding_b: np.ndarray) -> float:
        denom = (np.linalg.norm(embedding_a) * np.linalg.norm(embedding_b)) + 1e-6
        return float(np.dot(embedding_a, embedding_b) / denom)

    def classify_similarity(self, similarity: float, provider: str) -> str:
        if provider.startswith("deepface"):
            if similarity >= 0.82:
                return "matched"
            if similarity >= 0.69:
                return "uncertain"
            return "unknown"
        if similarity >= 0.93:
            return "matched"
        if similarity >= 0.84:
            return "uncertain"
        return "unknown"

    @staticmethod
    def dumps_embedding(embedding: np.ndarray) -> str:
        return json.dumps([round(float(item), 8) for item in embedding.tolist()])

    @staticmethod
    def loads_embedding(raw: str) -> np.ndarray:
        return np.array(json.loads(raw), dtype=np.float32)
