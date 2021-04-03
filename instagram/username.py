from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from username_search_python import Ui_search


class username_window(QWidget):

    def __init__(self):
        super().__init__()

        self.ui=Ui_search()
        self.ui.setupUi(self)
        self.ui.pb_reset.clicked.connect(self.search_reset)        
        
    def search_username(self,followers_list,follows_list):
        self.ui.lb_text_followers.setText(f"Followers: {len(followers_list)}")
        self.ui.lb_text_follows.setText(f"Follows: {len(follows_list)}")      
        self.ui.lw_followers.addItems(followers_list)
        self.ui.lw_follows.addItems(follows_list)
        
    def search_reset(self):
        self.ui.lb_text_follows.clear()
        self.ui.lb_text_followers.clear()
        self.ui.le_search.clear()
        self.ui.lw_follows.clear()
        self.ui.lw_followers.clear()
        

        



