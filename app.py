import cv2
import numpy as np

cam = cv2.VideoCapture(0)

while cam.isOpened():
    ret, frame = cam.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 🔴 RED
    lower_red1 = np.array([0,120,70])
    upper_red1 = np.array([10,255,255])
    lower_red2 = np.array([170,120,70])
    upper_red2 = np.array([179,255,255])

    mask_r1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_r2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = mask_r1 | mask_r2

    # ⚫ BLACK
    lower_black = np.array([0,0,0])
    upper_black = np.array([179,50,50])
    mask_black = cv2.inRange(hsv, lower_black, upper_black)

    # ⚪ WHITE
    lower_white = np.array([0,0,200])
    upper_white = np.array([179,50,255])
    mask_white = cv2.inRange(hsv, lower_white, upper_white)

    # 🟡 YELLOW
    lower_yellow = np.array([20,100,100])
    upper_yellow = np.array([35,255,255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # 🟠 ORANGE
    lower_orange = np.array([10,100,20])
    upper_orange = np.array([25,255,255])
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)

    # 🟢 GREEN
    lower_green = np.array([40,70,70])
    upper_green = np.array([80,255,255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # 🔵 BLUE
    lower_blue = np.array([100,150,0])
    upper_blue = np.array([140,255,255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # 🟣 PURPLE
    lower_purple = np.array([130,50,50])
    upper_purple = np.array([160,255,255])
    mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)

    # 🎯 DETECTION (IMPORTANT: use countNonZero)
    if cv2.countNonZero(mask_red) > 800:
        color = "Red"
        draw_color = (0,0,255)
        mask = mask_red

    elif cv2.countNonZero(mask_black) > 800:
        color = "Black"
        draw_color = (255,255,255)
        mask = mask_black

    elif cv2.countNonZero(mask_white) > 800:
        color = "White"
        draw_color = (255,255,255)
        mask = mask_white

    elif cv2.countNonZero(mask_yellow) > 800:
        color = "Yellow"
        draw_color = (0,255,255)
        mask = mask_yellow

    elif cv2.countNonZero(mask_orange) > 800:
        color = "Orange"
        draw_color = (0,165,255)
        mask = mask_orange

    elif cv2.countNonZero(mask_green) > 800:
        color = "Green"
        draw_color = (0,255,0)
        mask = mask_green

    elif cv2.countNonZero(mask_blue) > 800:
        color = "Blue"
        draw_color = (255,0,0)
        mask = mask_blue

    elif cv2.countNonZero(mask_purple) > 800:
        color = "Purple"
        draw_color = (255,0,255)
        mask = mask_purple

    else:
        color = None

    # 🧠 DRAW RESULT
    if color is not None:
        text = color + " Detected"

        # White outline (thick)
        cv2.putText(frame, text, (150,250),cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255), 5)

        # Black text (thin)
        cv2.putText(frame, text, (150,250),cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0), 5)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            cnt = max(contours, key=cv2.contourArea)

            if cv2.contourArea(cnt) > 1000:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x,y), (x+w,y+h), draw_color, 2)

    cv2.imshow("Color Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()