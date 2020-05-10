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


def process_video(filename):
    # if not os.path.exists(os.path.join(filename, "_undistorted.mp4):
    #     undistort(path+video_name)

    frame_count = 0

    video = cv2.VideoCapture(filename)

    if video.isOpened():
        cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
        total_count = video.get(cv2.CAP_PROP_FRAME_COUNT)

        codec = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        # codec = cv2.VideoWriter_fourcc(*'XVID')
        FPS = video.get(cv2.CAP_PROP_FPS)
        _, frame = video.read()
        # rescaled_frame = rescale_frame(frame)
        first_frame, box = crop_frame("Frame", frame)
        width = box[2]
        height = box[3]
        size = (width, height)
        out_video = cv2.VideoWriter(str(filename[:-4]) + '_cropped.mp4', codec, FPS, size, 1)

        cv2.imshow("Frame", first_frame)
        out_video.write(first_frame)

        while frame_count < total_count:
            ret, frame = video.read()

            if ret:
                frame_count = video.get(cv2.CAP_PROP_POS_FRAMES)

                # rescaled_frame = rescale_frame(frame)
                cropped_frame, _ = crop_frame("Frame", frame, box)
                # cv2.resizeWindow("Frame", cropped_frame.shape[1], cropped_frame.shape[0])
                cv2.imshow("Frame", cropped_frame)
                out_video.write(cropped_frame)
            else:
                print("Something's wrong: " + str(frame_count))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # frame_count += 1

        video.release()
        out_video.release()
        cv2.destroyAllWindows()


def main():
    path = "/Users/glebzinkovskiy/Documents/Orel_experiments/Original/Down/"
    video_name = "GX050012.mp4"

    # process_video(os.path.join(path, video_name))

    processed_path = path.split('/')[:-3]
    print()

    # sequence_videos()


if __name__=='__main__':
    main()