from ultralytics import YOLO
import cv2
import pyautogui as pag

model = YOLO('runs/detect/train10/weights/best.pt')

class_names = model.names
screen_size = pag.size()
screen_Centerx = screen_size.width / 2
screen_Centery = screen_size.height / 2

def main():
  cap = cv2.VideoCapture(0)

  while True:
    ret, frame = cap.read()
    result = model(frame)

    detections = result[0].boxes #captures all the objects in each frame
    detected_classes = set()

    for box in detections:
      x1, y1, x2, y2 = box.xyxy[0] 
      x_center = int((x1 + x2) / 2)
      y_center = int((y1 + y2) / 2)
      id = int(box.cls[0])
      class_name = class_names[id]
      detected_classes.add(class_name)

    # if 'thumb_index' in detected_classes:
    #   pag.leftClick(None, None)

    # if 'thumb_middle' in detected_classes:
    #   pag.rightClick(None, None)

    # if 'thumb_out' in detected_classes:
    #   pag.scroll(50) 

    # if 'pinky_out' in detected_classes:
    #   pag.scroll(-50)

    if 'fist' in detected_classes:
      #Treat the middle of the video as the center of screen
      pag.moveTo(screen_Centerx + (x_center * 3), screen_Centery + (y_center * 3))    

    annotated_frame = result[0].plot()
    cv2.imshow('handcursorx', annotated_frame)

    if (cv2.waitKey(30) == ord('f')):
      break


if __name__ == "__main__":
  main()