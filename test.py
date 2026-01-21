import pickle
import face_recognition
import numpy as np


with open("artifacts/face_encoding/encodings.pkl", "rb") as f:
    known_encodings = pickle.load(f)


test_image_path = "data/dataset/jeet/jeet01.jpeg"  # change this
image = face_recognition.load_image_file(test_image_path)


face_locations = face_recognition.face_locations(image)

if len(face_locations) == 0:
    print("❌ No face detected in test image")
    exit()

# Encode face
test_encoding = face_recognition.face_encodings(image, face_locations)[0]

# ---------------------------
# Compare with known encodings
# ---------------------------
THRESHOLD = 0.5
best_match = "Unknown"
best_distance = float("inf")

for person_name, enc_list in known_encodings.items():
    for enc in enc_list:
        distance = np.linalg.norm(enc - test_encoding)
        if distance < best_distance:
            best_distance = distance
            best_match = person_name

# ---------------------------
# Decision
# ---------------------------
print("Best match:", best_match)
print("Distance:", best_distance)

if best_distance < THRESHOLD:
    print(f"✅ Recognized as: {best_match}")
else:
    print("❌ Face is UNKNOWN")
