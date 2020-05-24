import os
import re

import cv2
from Undistort_func import *
#/Users/glebzinkovskiy/Documents/Orel_experiments/Original


def choose_box(frame):
    """
        Is called once for choosing the area of the crop
        Undistorts the frame first
        Reduces the size for resolution purposes
        Prompts the user with the smaller frame to choose ROI
        :param frame: first frame in the future video
        :return: area of the crop
        """

    _frame = undistort_frame(frame)
    height, width = _frame.shape[:2]
    _width = int(width / 3)
    _height = int(height / 4)
    resized_frame = cv2.resize(_frame, (_width, _height), interpolation=cv2.INTER_AREA)

    box = cv2.selectROI('Select ROI', img=resized_frame, showCrosshair=False)
    cv2.destroyWindow('Select ROI')
    box = [box[0] * 3, box[1] * 4, box[2] * 3, box[3] * 4]
    return box


def process_frame(frame, box):
    """
    Undistorts and then crops a frame
    :param frame:
    :param box:
    :return:
    """
    frame = undistort_frame(frame)
    frame = frame[int(box[1]):int(box[1] + box[3]), int(box[0]):int(box[0] + box[2])]
    return frame


def set_writer(video, box, filename):
    """
    Sets the writer once per set
    Separated for the clarity
    :param video:
    :param box:
    :param filename: name of the future video based on the set of videos in use
    :return:
    """
    FPS = video.get(cv2.CAP_PROP_FPS)
    size = (box[2], box[3])

    codec = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')  # for MP4 output
    out_video = cv2.VideoWriter(filename, codec, FPS, size, 1)
    return out_video


def main():
    path = input("Please choose the directory with videos\n")
    print("Press space to pause and p to pick the first frame. Press q to quit.")

    # please notice, that the working directory is changed per date
    os.chdir(path)

    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)

    folders = ['Up', 'Down']

    for f in folders:
        box = None
        out_video = None
        prev = None

        videofiles = [vf for vf in os.listdir(f) if vf[-4:]=='.mp4' or vf[-4:]=='.MP4']
        # TODO: FIX
        videofiles = sorted(videofiles, key=lambda item: int(item.partition('X')[2][:-8]))

        out_filename = re.split("X0[0-9]", videofiles[0])[1]

        for vf in videofiles:
            current_frame = 0
            offset = 0

            video = cv2.VideoCapture(os.path.join(f, vf))
            total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)

            while current_frame < total_frames:
                success, frame = video.read()
                current_frame = video.get(cv2.CAP_PROP_POS_FRAMES)
                if success:
                    if box is not None:
                        frame = process_frame(frame, box)
                        out_video.write(frame)
                    cv2.imshow("Frame", frame)
                    prev = frame
                else:
                    print("Non-readable frame: " + str(current_frame + offset))
                    if box is not None:
                        print("Replacing with the previous frame")
                        out_video.write(prev)
                    offset += 1

                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord(' '):
                    cv2.waitKey(-1)

                # if the area hasn't been chosen yet
                # awaits for the the frame for the pick
                if box is None:
                    if key == ord('p'):
                        box = choose_box(frame)
                        out_video = set_writer(video, box, os.path.join(f, out_filename))
                    elif key == ord(' '):
                        if cv2.waitKey(-1) & 0xFF == ord('p'):
                            box = choose_box(frame)
                            out_video = set_writer(video, box, os.path.join(f, out_filename))


            video.release()
            cv2.destroyAllWindows()
        out_video.release()


if __name__=='__main__':
    main()