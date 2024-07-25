import cv2
import mediapipe as mp
import pyautogui as pg

cap = cv2.VideoCapture(0)
hand_detection = mp.solutions.hands.Hands()
screen_width, screen_height = pg.size()
real_y = 0

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    rgb_conv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detection.process(rgb_conv)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            mp.solutions.drawing_utils.draw_landmarks(
                frame, hand
            )  # show the hand landmarks in the frame
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:  # index finger
                    cv2.circle(
                        img=frame, center=(x, y), radius=10, color=(255, 192, 203)
                    )
                    real_x = (
                        screen_width / frame_width * x
                    )  # x axis with respect to screen and not frame
                    real_y = screen_height / frame_height * y  # y axis same
                    pg.moveTo(real_x, real_y)
                if id == 5:
                    closing_x = screen_width / frame_width * x
                    closing_y = screen_height / frame_height * y

                    if (abs(real_y - closing_y)) < 40:
                        pg.click()
                        pg.sleep(2)

    cv2.imshow("Mouse cam", frame)  # show the frame

    k = cv2.waitKey(1) & 0xFF
    if k == 113:
        cv2.destroyAllWindows()
        break
