from PyQt5 import QtCore, QtWidgets, QtGui
from moilutils import MoilUtils


class MouseEvent(object):
    def __init__(self, parent):
        super(MouseEvent, self).__init__()
        self.parent = parent

    def mouse_event(self, event):
        """
        Specify coordinate from mouse left event to generate anypoint widget_controller and recenter image.

        Args:
            event (): Coordinate point return by pyqt core

        Returns:

        """
        if self.parent.image is not None:
            if event.button() == QtCore.Qt.LeftButton:
                pos_x = round(event.x())
                pos_y = round(event.y())
                ratio_x, ratio_y = MoilUtils.calculateRatioImage(self.parent.labelOriginal, self.parent.image)
                X = round(pos_x * ratio_x)
                Y = round(pos_y * ratio_y)
                if X <= 0 or X >= self.w and Y <= 0 or Y >= self.h:
                    coordinate_X = int(self.w / 2)
                    coordinate_Y = int(self.h / 2)
                else:
                    coordinate_X = X
                    coordinate_Y = Y
                self.point = (coordinate_X, coordinate_Y)
                self.setIcx.setValue(coordinate_X)
                self.setIcy.setValue(coordinate_Y)
                if self.parent.anypoint_view:
                    self.alpha, self.beta = self.moildev.getAlphaBeta(
                        coordinate_X, coordinate_Y, self.parent.anypoint.anypoint_mode)
                    self.parent.anypoint.anypoint()
                elif self.parent.buttonRecenter.isChecked():
                    self.parent.recenter.alpha, self.parent.recenter.beta = self.parent.moildev.getAlphaBeta(
                        coordinate_X, coordinate_Y)
                    self.parent.show_to_window()
