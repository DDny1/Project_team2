import cv2
import mediapipe as mp
import pandas as pd
import os

# MediaPipe Hands 초기화
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# 웹캠 캡처 설정
cap = cv2.VideoCapture(0)

# 라벨링 데이터를 저장할 리스트
data = []

def process_hand_landmarks(hand_landmarks):
    # 21개의 손 랜드마크를 (x, y, z)로 분리하여 데이터 형식에 맞게 정렬
    landmarks = []
    for landmark in hand_landmarks.landmark:
        landmarks.extend([landmark.x, landmark.y, landmark.z])
    return landmarks

# 기존 CSV 파일 로드
csv_file = 'hand_gesture_data.csv'
if os.path.exists(csv_file):
    existing_data = pd.read_csv(csv_file)
    print(f"Loaded existing data from {csv_file}")
else:
    existing_data = pd.DataFrame(columns=[f'x{i}' for i in range(21)] + [f'y{i}' for i in range(21)] + [f'z{i}' for i in range(21)] + ['label'])
    print(f"No existing data found. Creating new file: {csv_file}")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # BGR 이미지를 RGB로 변환
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # MediaPipe로 손 랜드마크 검출
    result = hands.process(frame_rgb)
    
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # 손 랜드마크 데이터를 처리
            landmarks = process_hand_landmarks(hand_landmarks)
            
            # 손 랜드마크를 영상에 그림
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # 키보드 입력 대기 및 라벨링 처리
            key = cv2.waitKey(1) & 0xFF
            if ord('a') <= key <= ord('z'):
                label = chr(key)
                data.append(landmarks + [label])
                print(f'Label {label.upper()} saved')
    
    # 결과 영상 출력
    cv2.imshow('Hand Gesture Labeling', frame)
    
    if cv2.waitKey(1) & 0xFF == 27:  # ESC 키를 눌러 종료
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()

# 새로운 데이터를 데이터프레임으로 변환
new_data = pd.DataFrame(data, columns=[f'x{i}' for i in range(21)] + [f'y{i}' for i in range(21)] + [f'z{i}' for i in range(21)] + ['label'])

# 기존 데이터와 새로운 데이터를 병합
combined_data = pd.concat([existing_data, new_data], ignore_index=True)

# 병합된 데이터를 CSV 파일로 저장
combined_data.to_csv(csv_file, index=False)
print(f'Data saved to {csv_file}')