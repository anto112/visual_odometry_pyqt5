import cv2
import os
from PyQt5 import QtCore, QtGui
from souceIcon import ResourceIcon


class VideoController(object):
    def __init__(self, parent):
        super(VideoController, self).__init__()
        self.parent = parent
        self.rs = ResourceIcon()
        self.fps = None
        self.pos_frame = None
        self.frame_count = None
        self.minute = None
        self.minutes = None
        self.seconds = None
        self.sec = None
        self.play = False
        self.frameNumber = 1
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.next_frame_slot)

    # migrate to video controller
    def next_frame_slot(self):
        """
        looping the frame showing in label user interface.

        """
        if self.parent.cam:
            success, self.parent.image = self.parent.cap.read()
            if success:
                self.fps = self.parent.cap.get(cv2.CAP_PROP_FPS)
                self.pos_frame = self.parent.cap.get(cv2.CAP_PROP_POS_FRAMES)
                self.frame_count = float(self.parent.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        else:
            self.frame_count = len(os.listdir(self.parent.folderOdometry))
            self.fps = 10
            if self.frameNumber < self.frame_count:
                self.pos_frame = self.frameNumber
                file = self.parent.folderOdometry + "/" + str(self.frameNumber) + ".png"
                self.parent.image = cv2.imread(file)
                self.parent.h, self.parent.w = self.parent.image.shape[:2]
                self.frameNumber += 1

        duration_sec = int(self.frame_count / self.fps)
        self.minutes = duration_sec // 60
        duration_sec %= 60
        self.seconds = duration_sec
        sec_pos = int(self.pos_frame / self.fps)
        self.minute = int(sec_pos // 60)
        sec_pos %= 60
        self.sec = sec_pos
        self.controller()
        self.parent.show_to_window()
        if self.parent.video_writer is not None:
            image = self.parent.image if self.parent.normal_view else self.parent.result_image
            self.parent.video_writer.write(image)

    def reset_time(self):
        """
        Reset the time when open the new video.

        """
        current = self.parent.label_time_recent
        current.setAlignment(QtCore.Qt.AlignCenter)
        current.setText("00:00")

        end_time = self.parent.label_time_end
        end_time.setAlignment(QtCore.Qt.AlignCenter)
        end_time.setText("00:00")

    def onclickPlayPauseButton(self):
        """
        Control the play and pause video controller button
        for example, if play is true: it will change the icon button

        """
        if self.play:
            self.pause_video()

        else:
            self.play_video()

    def pause_video(self):
        """
        Pause the frame in video or camera mode.

        """
        self.timer.stop()
        self.parent.btn_play_pouse.setIcon(
            QtGui.QIcon(QtGui.QPixmap.fromImage(self.rs.iconPlay())))
        self.play = False

    def play_video(self):
        """
        Play video by connect to timer function.

        """
        self.timer.start(1000 / self.fps)
        self.parent.btn_play_pouse.setIcon(
            QtGui.QIcon(QtGui.QPixmap.fromImage(self.rs.iconPause())))
        self.play = True

    def controller(self):
        """
        Manage the video to setup the current timer.

        """
        dst_value = self.pos_frame * (self.parent.slider_Video.maximum() + 1) / self.frame_count
        self.parent.slider_Video.blockSignals(True)
        self.parent.slider_Video.setValue(dst_value)
        self.parent.slider_Video.blockSignals(False)

        current = self.parent.label_time_recent
        current.setAlignment(QtCore.Qt.AlignCenter)
        current.setText("%02d : %02d" % (self.minute, self.sec))

        if self.minutes < 0:
            "this is for live camera, when the times more than 1000 minutes, it will set to 00:00"
            my_label3 = self.parent.label_time_end
            my_label3.setAlignment(QtCore.Qt.AlignCenter)
            my_label3.setText("00:00")

        else:
            my_label3 = self.parent.label_time_end
            my_label3.setAlignment(QtCore.Qt.AlignCenter)
            my_label3.setText("%02d : %02d" %
                              (self.minutes, self.seconds))

    def stop_video(self):
        """
        Stop video and set the time as a beginning, including the slider time

        """
        self.play = False
        self.parent.btn_play_pouse.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(self.rs.iconPlay())))
        if self.parent.cam:
            self.parent.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        else:
            self.frameNumber = 1

        self.next_frame_slot()
        self.reset_label_time()
        self.timer.stop()

    def reset_label_time(self):
        """
        Reset the time when open the new video.

        """
        current = self.parent.label_time_recent
        current.setAlignment(QtCore.Qt.AlignCenter)
        current.setText("00:00")

        current_1 = self.parent.label_time_end
        current_1.setAlignment(QtCore.Qt.AlignCenter)
        current_1.setText("00:00")

    def prev_video(self):
        """
        Previous video is 5 seconds.

        """
        if self.parent.cam:
            position = self.pos_frame - 5 * self.fps
            self.parent.cap.set(cv2.CAP_PROP_POS_FRAMES, position)

        else:
            self.frameNumber -= 5 * self.fps
            if self.frameNumber <= 1:
                self.frameNumber = 1

        self.next_frame_slot()

    def skip_video(self):
        """
        skip video in 5 seconds.

        """
        if self.parent.cam:
            position = self.pos_frame + 5 * self.fps
            self.parent.cap.set(cv2.CAP_PROP_POS_FRAMES, position)

        else:
            self.frameNumber += 5 * self.fps
            if self.frameNumber >= self.frame_count:
                self.frameNumber = self.frame_count

        self.next_frame_slot()

    def changeValueSlider(self, value):
        """
        Set and control the slider to control the video.

        Args:
            value (): Value from slider

        """
        dst_frame = self.frame_count * value / self.parent.slider_Video.maximum()
        if self.parent.cam:
            self.parent.cap.set(cv2.CAP_PROP_POS_FRAMES, dst_frame)

        else:
            self.frameNumber = round(dst_frame)
            if self.frameNumber <= 1:
                self.frameNumber = 1

        self.next_frame_slot()
        self.pause_video()
        self.play = False
