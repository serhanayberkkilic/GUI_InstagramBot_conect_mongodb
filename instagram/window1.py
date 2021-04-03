from PyQt5.QtWidgets import QApplication
from main import main_window

app=QApplication([])
window=main_window()
window.show()
result=app.exec_()


class window():

    def __init__(self):
        super(window,self).__init__()
        self.a=main_window()
        
        if result==0:
            self.a.driver.close()