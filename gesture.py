import cv2
import mediapipe as mp
import pyautogui
import time
import os

if not os.path.exists("shot_saver"):
    os.makedirs("shot_saver")

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

mp_draw = mp.solutions.drawing_utils

tip_ids=[4,8,12,16,20]

screenshot_taken=False

def process_frame(img):

    global screenshot_taken

    rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(rgb)

    finger_count=0

    if results.multi_hand_landmarks:

        for handLms in results.multi_hand_landmarks:

            lm_list=[]

            for id,lm in enumerate(handLms.landmark):

                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)

                lm_list.append((cx,cy))

            if len(lm_list)!=0:

                if lm_list[4][0] > lm_list[3][0]:
                    finger_count+=1

                for id in range(1,5):

                    if lm_list[tip_ids[id]][1] < lm_list[tip_ids[id]-2][1]:
                        finger_count+=1

            mp_draw.draw_landmarks(img,handLms,mp_hands.HAND_CONNECTIONS)

    cv2.putText(img,f'Fingers:{finger_count}',(20,60),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    if finger_count==5 and not screenshot_taken:

        filename=f"shot_saver/screenshot_{int(time.time())}.png"
        pyautogui.screenshot().save(filename)

        screenshot_taken=True

    if finger_count<5:
        screenshot_taken=False

    return img