from MainWindow import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore
from moilutils import MoilUtils
import cv2
import numpy as np
from mouseController import MouseEvent
from videoController import VideoController


class Controller(Ui_MainWindow):
    def __init__(self, parent):
        super(Controller, self).__init__()
        self.parent = parent
        self.setupUi(self.parent)
        self.title = "ADAS"
        self.typeCamera = None
        self.w = None
        self.h = None
        self.moildev = []
        self.mapsX = []
        self.mapsY = []
        self.singleView = True
        self.treeView = False
        self.sixView = False
        self.image = None
        self.cam = None
        self.cap = None
        self.windowActivated = None
        self.winResultActive = None

        img = np.zeros((400, 400))
        self.imgtry = cv2.merge([img, img, img])

        # draw on it in color
        cv2.rectangle(self.imgtry, (200, 200), (300, 300), (0, 0, 255), 5)

        # odometry
        self.odometry = False
        self.folder_odometry = None
        self.mouseEvent = MouseEvent(self)
        self.videoController = VideoController(self)
        self.initControlFrameView()
        self.connectEvent()

    def initControlFrameView(self):
        self.frame.hide()
        self.buttonBack.hide()
        self.frame6view.hide()
        self.frameSingleParam.hide()
        self.labelInfo.hide()
        self.checkBox_2.setChecked(True)
        self.labelSlam.hide()

    def connectEvent(self):
        self.openImage.clicked.connect(self.onclickOpenImage)
        self.openVideo.clicked.connect(self.load_video)
        self.btnOdometry.clicked.connect(self.onclickOdometry)
        self.openCamera.clicked.connect(self.open_camera)

        self.camConfig.clicked.connect(MoilUtils.openCameraParameters)
        # self.btn_Original.clicked.connect(self.onclickShowOriginal)
        self.btn_threeView.clicked.connect(self.onclickTreeView)
        self.btn_sixView.clicked.connect(self.onclickSixView)

        self.alphaSingle.valueChanged.connect(self.setParamsSingle)
        self.betaSingle.valueChanged.connect(self.setParamsSingle)
        self.zoomSingle.valueChanged.connect(self.setParamsSingle)

        self.alpha6view_window1.valueChanged.connect(self.setParamWindow1)
        self.beta6view_window1.valueChanged.connect(self.setParamWindow1)
        self.zoom6view_window1.valueChanged.connect(self.setParamWindow1)

        self.alpha6view_window2.valueChanged.connect(self.setParamWindow2)
        self.beta6view_window2.valueChanged.connect(self.setParamWindow2)
        self.zoom6view_window2.valueChanged.connect(self.setParamWindow2)

        self.alpha6view_window3.valueChanged.connect(self.setParamWindow3)
        self.beta6view_window3.valueChanged.connect(self.setParamWindow3)
        self.zoom6view_window3.valueChanged.connect(self.setParamWindow3)

        self.alpha6view_window4.valueChanged.connect(self.setParamWindow4)
        self.beta6view_window4.valueChanged.connect(self.setParamWindow4)
        self.zoom6view_window4.valueChanged.connect(self.setParamWindow4)

        self.alpha6view_window5.valueChanged.connect(self.setParamWindow5)
        self.beta6view_window5.valueChanged.connect(self.setParamWindow5)
        self.zoom6view_window5.valueChanged.connect(self.setParamWindow5)

        self.alpha6view_window6.valueChanged.connect(self.setParamWindow6)
        self.beta6view_window6.valueChanged.connect(self.setParamWindow6)
        self.zoom6view_window6.valueChanged.connect(self.setParamWindow6)

        self.label6view_window1.mousePressEvent = self.onclickWindow1
        self.label6view_window2.mousePressEvent = self.onclickWindow2
        self.label6view_window3.mousePressEvent = self.onclickWindow3
        self.label6view_window4.mousePressEvent = self.onclickWindow4
        self.label6view_window5.mousePressEvent = self.onclickWindow5
        self.label6view_window6.mousePressEvent = self.onclickWindow6
        self.labelOriginal.mousePressEvent = self.onclickWindowOriginal
        self.labelSlam.mousePressEvent = self.onclickWindowSlam
        self.buttonBack.clicked.connect(self.onclickBack)
        self.checkBox.stateChanged.connect(self.onclickShowOriginal)
        self.checkBox_2.stateChanged.connect(self.onclickShowSlam)

        # video Controller
        self.btn_play_pouse.clicked.connect(self.videoController.onclickPlayPauseButton)
        self.btn_prev_video.clicked.connect(self.videoController.prev_video)
        self.btn_skip_video.clicked.connect(self.videoController.skip_video)
        self.btn_stop_video.clicked.connect(self.videoController.stop_video)
        self.slider_Video.valueChanged.connect(self.videoController.changeValueSlider)

    # ++++++++++++++++++ open media +++++++++++++++++++
    def onclickOdometry(self):
        self.folderOdometry = MoilUtils.selectDirectory(self.parent)
        if self.folderOdometry:
            self.odometry = True
            self.cam = None
            self.typeCamera = MoilUtils.selectCameraType()
            self.singleViewInFrame()
            self.initParameterMultiVIew()
            self.mapsX, self.mapsY = MoilUtils.createMapsMultipleView(self.numberOfView, self.typeCamera, self.alpha,
                                                                      self.beta, self.zoom)
            self.showInformationCamera()
            self.videoController.next_frame_slot()

    def initParameterMultiVIew(self):
        self.alpha = [self.alpha6view_window1.value(),
                      self.alpha6view_window2.value(),
                      self.alpha6view_window3.value(),
                      self.alpha6view_window4.value(),
                      self.alpha6view_window5.value(),
                      self.alpha6view_window6.value()]
        self.beta = [self.beta6view_window1.value(),
                     self.beta6view_window2.value(),
                     self.beta6view_window3.value(),
                     self.beta6view_window4.value(),
                     self.beta6view_window5.value(),
                     self.beta6view_window6.value()]
        self.zoom = [self.zoom6view_window1.value(),
                     self.zoom6view_window2.value(),
                     self.zoom6view_window3.value(),
                     self.zoom6view_window4.value(),
                     self.zoom6view_window5.value(),
                     self.zoom6view_window6.value()]
        self.numberOfView = len(self.zoom)

    def onclickOpenImage(self):
        filename = MoilUtils.selectFile(self.parent, "Select Image", "../SourceImage",
                                        "Image Files (*.jpeg *.jpg *.png *.gif *.bmg)")
        if filename:
            self.image = MoilUtils.readImage(filename)
            self.h, self.w = self.image.shape[:2]
            self.typeCamera = MoilUtils.readCameraType(filename)
            self.singleViewInFrame()
            self.initParameterMultiVIew()
            self.mapsX, self.mapsY = MoilUtils.createMapsMultipleView(self.numberOfView, self.typeCamera, self.alpha,
                                                                      self.beta, self.zoom)
            self.showInformationCamera()
            self.parent.setWindowTitle(self.title + " - " + filename)
            self.cam = None
            self.odometry = False
            self.showToWindow()

    def load_video(self):
        """
        Open Dialog to search video file from Directory. after you select the video file, it will show the prompt
        to select the type of camera.

        Returns:

        """
        video_source = MoilUtils.selectFile(self.parent,
                                            "Select Video Files",
                                            "../",
                                            "Video Files (*.mp4 *.avi *.mpg *.gif *.mov)")
        if video_source:
            self.typeCamera = MoilUtils.selectCameraType()
            self.singleViewInFrame()
            self.initParameterMultiVIew()
            self.mapsX, self.mapsY = MoilUtils.createMapsMultipleView(self.numberOfView, self.typeCamera, self.alpha,
                                                                      self.beta, self.zoom)
            self.showInformationCamera()
            self.parent.setWindowTitle(self.title + " - " + video_source)
            if self.typeCamera is not None:
                self.running_video(video_source)

    def open_camera(self):
        """
        open the camera from the available source in the system,
        this function provide 2 source namely USB cam and Streaming Cam from Raspberry pi.
        """
        camera_source = MoilUtils.selectCameraSource()
        if camera_source:
            self.typeCamera = MoilUtils.selectCameraType()
            if self.typeCamera is not None:
                self.running_video(camera_source)

    def running_video(self, video_source):
        """
        Open Video following the source given.

        Args:
            video_source (): the source of media, can be camera and video file.
        """
        self.cap = cv2.VideoCapture(video_source)
        success, image = self.cap.read()
        if success:
            self.h, self.w = image.shape[:2]
            self.cam = True
            self.videoController.next_frame_slot()
        else:
            QtWidgets.QMessageBox.information(self.parent, "Information", "No source camera founded")

    def singleViewInFrame(self):
        moil = MoilUtils.connectToMoildev(self.typeCamera)
        self.mapsX_single, self.mapsY_single = moil.getAnypointMaps(self.alphaSingle.value(),
                                                                    self.betaSingle.value(),
                                                                    self.zoomSingle.value(),
                                                                    2)
        if (moil.getImageHeight() / moil.getImageWidth()) == 0.75:
            self.labelOriginal.setGeometry(QtCore.QRect(940, 20, 200, 150))
            self.labelSlam.setGeometry(QtCore.QRect(940, 180, 200, 150))
        else:
            self.labelOriginal.setGeometry(QtCore.QRect(90, 770, 200, 200))
            self.labelSlam.setGeometry(QtCore.QRect(300, 770, 200, 200))

    def setParamsSingle(self):
        alpha = self.alphaSingle.value()
        beta = self.betaSingle.value()
        zoom = self.zoomSingle.value()
        moil = MoilUtils.connectToMoildev(self.typeCamera)
        self.mapsX_single, self.mapsY_single = moil.getAnypointMaps(alpha, beta, zoom, 2)
        self.showToWindow()

    def setParamWindow1(self):
        alpha = self.alpha6view_window1.value()
        beta = self.beta6view_window1.value()
        zoom = self.zoom6view_window1.value()
        self.mapsX[0], self.mapsY[0] = self.moildev[0].getAnypointMaps(alpha, beta, zoom, 2)
        self.showToWindow()

    def setParamWindow2(self):
        alpha = self.alpha6view_window2.value()
        beta = self.beta6view_window2.value()
        zoom = self.zoom6view_window2.value()
        self.mapsX[1], self.mapsY[1] = self.moildev[1].getAnypointMaps(alpha, beta, zoom, 2)
        self.showToWindow()

    def setParamWindow3(self):
        alpha = self.alpha6view_window3.value()
        beta = self.beta6view_window3.value()
        zoom = self.zoom6view_window3.value()
        self.mapsX[2], self.mapsY[2] = self.moildev[2].getAnypointMaps(alpha, beta, zoom, 2)
        self.showToWindow()

    def setParamWindow4(self):
        alpha = self.alpha6view_window4.value()
        beta = self.beta6view_window4.value()
        zoom = self.zoom6view_window4.value()
        self.mapsX[3], self.mapsY[3] = self.moildev[3].getAnypointMaps(alpha, beta, zoom, 2)
        self.showToWindow()

    def setParamWindow5(self):
        alpha = self.alpha6view_window5.value()
        beta = self.beta6view_window5.value()
        zoom = self.zoom6view_window5.value()
        self.mapsX[4], self.mapsY[4] = self.moildev[4].getAnypointMaps(alpha, beta, zoom, 2)
        self.showToWindow()

    def setParamWindow6(self):
        alpha = self.alpha6view_window6.value()
        beta = self.beta6view_window6.value()
        zoom = self.zoom6view_window6.value()
        self.mapsX[5], self.mapsY[5] = self.moildev[5].getAnypointMaps(alpha, beta, zoom, 2)
        self.showToWindow()

    def onclickWindow1(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.winResultActive = None
            self.windowActivated = 1
            self.showToWindow()

    def onclickWindow2(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.winResultActive = None
            self.windowActivated = 2
            self.showToWindow()

    def onclickWindow3(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.winResultActive = None
            self.windowActivated = 3
            self.showToWindow()

    def onclickWindow4(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.winResultActive = None
            self.windowActivated = 4
            self.showToWindow()

    def onclickWindow5(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.winResultActive = None
            self.windowActivated = 5
            self.showToWindow()

    def onclickWindow6(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.winResultActive = None
            self.windowActivated = 6
            self.showToWindow()

    def onclickWindowOriginal(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.winResultActive = 1
            self.showToWindow()

    def onclickWindowSlam(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.winResultActive = 2
            self.showToWindow()

    # ++++++++++++ control View Multiple Window +++++++++++
    def onclickTreeView(self):
        if self.image is not None:
            self.winResultActive = None
            self.windowActivated = 2
            if self.btn_threeView.isChecked():
                self.btn_sixView.setChecked(False)
                self.frame6view.show()
                self.singleView = False
                self.treeView = True
                self.sixView = False

            else:
                self.singleView = True
                self.treeView = False
                self.sixView = False
                self.frame6view.hide()
            self.controlFrame()

    def onclickSixView(self):
        if self.image is not None:
            self.winResultActive = None
            self.windowActivated = 2
            if self.btn_sixView.isChecked():
                self.btn_threeView.setChecked(False)
                self.frame6view.show()
                self.singleView = False
                self.treeView = False
                self.sixView = True
            else:
                self.singleView = True
                self.treeView = False
                self.sixView = False
                self.frame6view.hide()
            self.controlFrame()

    def controlFrame(self):
        if self.treeView:
            self.label6view_window4.hide()
            self.label6view_window5.hide()
            self.label6view_window6.hide()
            self.frameWin4.hide()
            self.frameWin5.hide()
            self.frameWin6.hide()
        elif self.sixView:
            self.label6view_window4.show()
            self.label6view_window5.show()
            self.label6view_window6.show()
            self.frameWin4.show()
            self.frameWin5.show()
            self.frameWin6.show()
        self.showToWindow()

    def onclickShowOriginal(self):
        if self.image is not None:
            if self.checkBox.isChecked():
                self.labelOriginal.hide()
                if self.labelSlam.isVisible():
                    if (self.h / self.w) == 0.75:
                        self.labelSlam.setGeometry(QtCore.QRect(940, 20, 200, 150))
                    else:
                        self.labelSlam.setGeometry(QtCore.QRect(90, 770, 200, 200))
            else:
                self.labelOriginal.show()
                if self.labelSlam.isVisible():
                    if (self.h / self.w) == 0.75:
                        self.labelSlam.setGeometry(QtCore.QRect(940, 180, 200, 150))
                    else:
                        self.labelSlam.setGeometry(QtCore.QRect(300, 770, 200, 200))

    def onclickShowSlam(self):
        if self.image is not None:
            if self.checkBox_2.isChecked():
                self.labelSlam.hide()
            else:
                self.labelSlam.show()
                if self.labelOriginal.isVisible():
                    if (self.h / self.w) == 0.75:
                        self.labelSlam.setGeometry(QtCore.QRect(940, 180, 200, 150))
                else:
                    self.labelSlam.setGeometry(QtCore.QRect(940, 20, 200, 150))

    def onclickBack(self):
        self.winResultActive = None
        self.showToWindow()

    # showing result image on user interface
    def showToWindow(self):
        global imgOri, imgSlam, image
        size = self.sizeResultImage()
        self.controlVideoButton()
        resImage = self.image.copy()
        if self.winResultActive is None:
            self.buttonBack.hide()
            if self.singleView:
                self.frameSingleParam.show()
                image = cv2.remap(resImage, self.mapsX_single, self.mapsY_single, cv2.INTER_CUBIC)
                imgOri = MoilUtils.drawPolygon(resImage, self.mapsX_single, self.mapsY_single)
                imgSlam = MoilUtils.drawPoint(image.copy(), (200, 500), 50)
                MoilUtils.showImageToLabel(self.labelResult, image, size)

            elif self.treeView:
                self.frameSingleParam.hide()
                image = []
                label = [self.label6view_window1, self.label6view_window2, self.label6view_window3]
                for i in range(3):
                    image.append(cv2.remap(resImage, self.mapsX[i], self.mapsY[i], cv2.INTER_CUBIC))
                    MoilUtils.showImageToLabel(label[i], image[i], 200)

                num = int(self.windowActivated - 1)
                MoilUtils.showImageToLabel(self.labelResult, image[num], size)
                imgOri = MoilUtils.drawPolygon(resImage, self.mapsX[num], self.mapsY[num])
                imgSlam = resImage

            elif self.sixView:
                self.frameSingleParam.hide()
                image = []
                label = [self.label6view_window1, self.label6view_window2, self.label6view_window3,
                         self.label6view_window4, self.label6view_window5, self.label6view_window6]
                for i in range(6):
                    image.append(cv2.remap(resImage, self.mapsX[i], self.mapsY[i], cv2.INTER_CUBIC))
                    MoilUtils.showImageToLabel(label[i], image[i], 200)

                num = int(self.windowActivated - 1)
                MoilUtils.showImageToLabel(self.labelResult, image[num], size)
                imgOri = MoilUtils.drawPolygon(resImage, self.mapsX[num], self.mapsY[num])
                imgSlam = resImage

        else:
            self.buttonBack.show()
            if self.winResultActive == 1:
                imgOri = self.image.copy()
                MoilUtils.showImageToLabel(self.labelResult, imgOri, size)
            elif self.winResultActive == 2:
                imgOri = resImage
                MoilUtils.showImageToLabel(self.labelResult, imgOri, size)

        MoilUtils.showImageToLabel(self.labelOriginal, imgOri, 200)
        MoilUtils.showImageToLabel(self.labelSlam, imgSlam, 200)
        MoilUtils.showImageToLabel(self.labelTrajectory, self.imgtry, 380)

    def sizeResultImage(self):
        if (self.h / self.w) == 0.75:
            self.labelInfo.show()
            size = 1140
        else:
            self.labelInfo.hide()
            size = 1000
        return size

    def controlVideoButton(self):
        if self.cam or self.odometry:
            self.frame.show()
        else:
            self.frame.hide()

    # ++++++++ others +++++++++++++
    def showInformationCamera(self):
        moil = MoilUtils.connectToMoildev(self.typeCamera)
        self.labelTypeCamera.setText(self.typeCamera)
        self.labelFoV.setText(str(moil.getCameraFov()))
        self.imgWidth.setText(str(moil.getImageWidth()))
        self.imgHeight.setText(str(moil.getImageHeight()))
        self.imgIcx.setText(str(moil.getIcx()))
        self.imgIcy.setText(str(moil.getIcy()))
