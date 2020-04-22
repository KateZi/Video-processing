import cv2
import os
from Undistort_func import undistort


def rescale_frame(frame, percent=75):
    height, width = frame.shape[:2]
    _width = int(width * percent/100)
    _height = int(height * percent/100)

    return cv2.resize(frame, (_width, _height), interpolation=cv2.INTER_AREA)


def crop_frame(windowname, frame, box=None):
    if box is None:
        box = cv2.selectROI(windowName=windowname, img=frame, showCrosshair=False)
    _frame = frame[int(box[1]):int(box[1] + box[3]), int(box[0]):int(box[0] + box[2])]
    return _frame, box


path = "../data/"
video_name = "GX050012.mp4"
name_tail = "_undistorted.mp4"

if not os.path.exists(path+video_name[:-4]+name_tail):
    undistort(path+video_name)

video = cv2.VideoCapture(path + video_name[:-4] + name_tail)

frame_count = 0
box = None

screen_res = 1440, 900


if video.isOpened()==True:
    codec = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    FPS = video.get(cv2.CAP_PROP_FPS)
    _, frame = video.read()
    rescaled_frame = rescale_frame(frame)
    first_frame, box = crop_frame(rescaled_frame)
    width = box[3]
    height = box[2]
    out_video = cv2.VideoWriter(str(video_name[:-4]) + '_cropped.mp4', codec, FPS, (width, height), 1)



    ret, frame = video.read()

    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)

    if ret:
        rescaled_frame = rescale_frame(frame)
        cropped_frame, box = crop_frame("Frame", rescaled_frame, box)
        # cv2.resizeWindow("Frame", cropped_frame.shape[1], cropped_frame.shape[0])
        cv2.imshow("Frame", cropped_frame)
    else:
        print("Something's wrong: " + str(frame_count))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_count += 1

video.release()
cv2.destroyAllWindows()