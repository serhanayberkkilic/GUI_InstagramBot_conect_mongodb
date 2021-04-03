from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from settings_python import Ui_settings

class settings_window(QWidget):

    def __init__(self):
        super().__init__()

        self.ui=Ui_settings()
        self.ui.setupUi(self)

    def show_data(self,fallow,fallowers,post,arenotnumber,imnotnumber,arenotlist,imnotlist):

        self.ui.label_flallow.setText(f"Fallow: {fallow}")
        self.ui.label_fallowers.setText(f"Fallowers: {fallowers}")
        self.ui.lb_post.setText(f"Post: {post}")
        self.ui.label_arenot.setText(f"Are Not Following Back:{arenotnumber}")
        self.ui.label_Im.setText(f"Im Not Following Back:{imnotnumber}")
        self.ui.list_widget_arenot.addItems(arenotlist)
        self.ui.list_widget_imnot.addItems(imnotlist)
        