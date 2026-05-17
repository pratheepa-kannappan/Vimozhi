"""import cv2
import mediapipe as mp
import pandas as pd
import os

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

gesture_name = input("Enter gesture label (e.g., NeedHelp, SFH): ")
num_samples = int(input("Enter number of samples to capture (e.g., 300): "))

data = []

cap = cv2.VideoCapture(0)
with mp_hands.Hands(static_image_mode=False,
                    max_num_hands=1,
                    min_detection_confidence=0.7) as hands:
    count = 0
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.extend([lm.x, lm.y, lm.z])
                data.append(landmarks)
                count += 1

        cv2.putText(frame, f"{gesture_name}: {count}/{num_samples}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Collecting Data', frame)

        if cv2.waitKey(1) & 0xFF == 27 or count >= num_samples:  # ESC to exit
            break

cap.release()
cv2.destroyAllWindows()

# Save collected data
df = pd.DataFrame(data)
os.makedirs('dataset', exist_ok=True)
df['label'] = gesture_name
df.to_csv(f'dataset/{gesture_name}.csv', index=False)
print(f"✅ Saved {count} samples for '{gesture_name}' in dataset/{gesture_name}.csv")"""