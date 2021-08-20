#########################################################################
#   MoilApp (Applications for sophisticated fisheye image processing)   #
#   Written by Haryanto (haryanto@o3635.mcut.edu.tw)                    #
#   Based on Moil-Lab (Ming Chi University of Technology)               #
#########################################################################
import sys
from controller import *


def main():
    """
    Create instance Main window to create the main window of Application.

    Returns:
        None.
    """
    apps = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Controller(MainWindow)
    MainWindow.show()
    sys.exit(apps.exec_())


if __name__ == '__main__':
    main()

