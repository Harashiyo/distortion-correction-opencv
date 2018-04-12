# -*- coding: utf-8 -*-
import sys
from undistortion import DistortionCorrection
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSlider, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QImage


class App(QWidget):

    def __init__(self, url):
        super().__init__()
        self.dc = DistortionCorrection(url)
        self.title = 'undistortion'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        '''
        focal length用スライダー
        '''
        sld_init_position = 49
        self.fl_min_edit = QLineEdit('1000')
        self.fl_min_edit.setMinimumWidth(38)
        fl_min_vbox = QVBoxLayout()
        fl_min_vbox.addWidget(QLabel('min'), alignment=(Qt.AlignCenter))
        fl_min_vbox.addWidget(self.fl_min_edit)

        self.fl_max_edit = QLineEdit('5000')
        self.fl_max_edit.setMinimumWidth(38)
        fl_max_vbox = QVBoxLayout()
        fl_max_vbox.addWidget(QLabel('max'), alignment=(Qt.AlignCenter))
        fl_max_vbox.addWidget(self.fl_max_edit)

        self.fl = self.calcFocalLength(int(self.fl_max_edit.text()),int(self.fl_min_edit.text()),sld_init_position)
        self.focal_length_label = QLabel('focal length : ' + str(self.fl))
        self.focal_length_sld = QSlider(Qt.Horizontal, self)
        self.focal_length_sld.setFocusPolicy(Qt.NoFocus)
        self.focal_length_sld.setSliderPosition(sld_init_position)
        self.focal_length_sld.valueChanged[int].connect(self.changeValueFl)
        self.focal_length_sld.setMinimumWidth(200)
        focal_length_vbox = QVBoxLayout()
        focal_length_vbox.addWidget(
            self.focal_length_label, alignment=(Qt.AlignCenter))
        focal_length_vbox.addWidget(self.focal_length_sld)

        '''
        k1用スライダー
        '''

        self.k1_min_edit = QLineEdit('-1')
        self.k1_min_edit.setMinimumWidth(38)
        k1_min_vbox = QVBoxLayout()
        k1_min_vbox.addWidget(QLabel('min'), alignment=(Qt.AlignCenter))
        k1_min_vbox.addWidget(self.k1_min_edit)

        self.k1_max_edit = QLineEdit('1')
        self.k1_max_edit.setMinimumWidth(38)
        k1_max_vbox = QVBoxLayout()
        k1_max_vbox.addWidget(QLabel('max'), alignment=(Qt.AlignCenter))
        k1_max_vbox.addWidget(self.k1_max_edit)

        self.k1 = self.calcDistortionCoefficient(int(self.k1_max_edit.text()),int(self.k1_min_edit.text()),sld_init_position)
        self.k1_label=QLabel('k1 : ' + str(self.k1))
        self.k1_sld=QSlider(Qt.Horizontal, self)
        self.k1_sld.setFocusPolicy(Qt.NoFocus)
        self.k1_sld.setSliderPosition(sld_init_position)
        self.k1_sld.valueChanged[int].connect(self.changeValueK1)
        self.k1_sld.setMinimumWidth(200)
        k1_vbox=QVBoxLayout()
        k1_vbox.addWidget(self.k1_label, alignment=(Qt.AlignCenter))
        k1_vbox.addWidget(self.k1_sld)


        '''
        k2用スライダー
        '''

        self.k2_min_edit=QLineEdit('-1')
        self.k2_min_edit.setMinimumWidth(38)
        k2_min_vbox=QVBoxLayout()
        k2_min_vbox.addWidget(QLabel('min'), alignment=(Qt.AlignCenter))
        k2_min_vbox.addWidget(self.k2_min_edit)

        self.k2_max_edit=QLineEdit('1')
        self.k2_max_edit.setMinimumWidth(38)
        k2_max_vbox=QVBoxLayout()
        k2_max_vbox.addWidget(QLabel('max'), alignment=(Qt.AlignCenter))
        k2_max_vbox.addWidget(self.k2_max_edit)

        self.k2 = self.calcDistortionCoefficient(int(self.k2_max_edit.text()),int(self.k2_min_edit.text()),sld_init_position)
        self.k2_label=QLabel('k2 : ' + str(self.k2))
        self.k2_sld=QSlider(Qt.Horizontal, self)
        self.k2_sld.setFocusPolicy(Qt.NoFocus)
        self.k2_sld.setSliderPosition(sld_init_position)
        self.k2_sld.valueChanged[int].connect(self.changeValueK2)
        self.k2_sld.setMinimumWidth(200)
        k2_vbox=QVBoxLayout()
        k2_vbox.addWidget(self.k2_label, alignment=(Qt.AlignCenter))
        k2_vbox.addWidget(self.k2_sld)

        
        '''
        p1用スライダー
        '''

        self.p1_min_edit = QLineEdit('-1')
        self.p1_min_edit.setMinimumWidth(38)
        p1_min_vbox = QVBoxLayout()
        p1_min_vbox.addWidget(QLabel('min'), alignment=(Qt.AlignCenter))
        p1_min_vbox.addWidget(self.p1_min_edit)

        self.p1_max_edit = QLineEdit('1')
        self.p1_max_edit.setMinimumWidth(38)
        p1_max_vbox = QVBoxLayout()
        p1_max_vbox.addWidget(QLabel('max'), alignment=(Qt.AlignCenter))
        p1_max_vbox.addWidget(self.p1_max_edit)

        self.p1 = self.calcDistortionCoefficient(int(self.p1_max_edit.text()),int(self.p1_min_edit.text()),sld_init_position)
        self.p1_label=QLabel('p1 : ' + str(self.p1))
        self.p1_sld=QSlider(Qt.Horizontal, self)
        self.p1_sld.setFocusPolicy(Qt.NoFocus)
        self.p1_sld.setSliderPosition(sld_init_position)
        self.p1_sld.valueChanged[int].connect(self.changeValueP1)
        self.p1_sld.setMinimumWidth(200)
        p1_vbox=QVBoxLayout()
        p1_vbox.addWidget(self.p1_label, alignment=(Qt.AlignCenter))
        p1_vbox.addWidget(self.p1_sld)


        '''
        p2用スライダー
        '''

        self.p2_min_edit=QLineEdit('-1')
        self.p2_min_edit.setMinimumWidth(38)
        p2_min_vbox=QVBoxLayout()
        p2_min_vbox.addWidget(QLabel('min'), alignment=(Qt.AlignCenter))
        p2_min_vbox.addWidget(self.p2_min_edit)

        self.p2_max_edit=QLineEdit('1')
        self.p2_max_edit.setMinimumWidth(38)
        p2_max_vbox=QVBoxLayout()
        p2_max_vbox.addWidget(QLabel('max'), alignment=(Qt.AlignCenter))
        p2_max_vbox.addWidget(self.p2_max_edit)

        self.p2 = self.calcDistortionCoefficient(int(self.p2_max_edit.text()),int(self.p2_min_edit.text()),sld_init_position)
        self.p2_label=QLabel('p2 : ' + str(self.p2))
        self.p2_sld=QSlider(Qt.Horizontal, self)
        self.p2_sld.setFocusPolicy(Qt.NoFocus)
        self.p2_sld.setSliderPosition(sld_init_position)
        self.p2_sld.valueChanged[int].connect(self.changeValueP2)
        self.p2_sld.setMinimumWidth(200)
        p2_vbox=QVBoxLayout()
        p2_vbox.addWidget(self.p2_label, alignment=(Qt.AlignCenter))
        p2_vbox.addWidget(self.p2_sld)


        hbox=QHBoxLayout()
        hbox.addLayout(fl_min_vbox)
        hbox.addLayout(focal_length_vbox)
        hbox.addLayout(fl_max_vbox)
        hbox.addLayout(k1_min_vbox)
        hbox.addLayout(k1_vbox)
        hbox.addLayout(k1_max_vbox)
        hbox.addLayout(k2_min_vbox)
        hbox.addLayout(k2_vbox)
        hbox.addLayout(k2_max_vbox)
        hbox.addLayout(p1_min_vbox)
        hbox.addLayout(p1_vbox)
        hbox.addLayout(p1_max_vbox)
        hbox.addLayout(p2_min_vbox)
        hbox.addLayout(p2_vbox)
        hbox.addLayout(p2_max_vbox)

        self.image_label=QLabel()
        self.image_label.setPixmap(self.get_QPixmap(self.dc.undistort()))
        # self.resize(pixmap.width(), pixmap.height())

        vbox=QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.image_label, alignment=(Qt.AlignCenter))
        self.setLayout(vbox)
        self.show()
    
    def calcFocalLength(self,max_value, min_value, value):
        return round(min_value+(max_value-min_value)*(value / 99)**2,6)

    def calcDistortionCoefficient(self,max_value, min_value, value):
        if value < 49:
            dc = round(min_value*((value -49)/49)**2,6)
        else:
            dc = round(max_value*((value -49)/49)**2,6)
        return dc
    

    def changeValueFl(self, value):
        self.fl = self.calcFocalLength(int(self.fl_max_edit.text()),int(self.fl_min_edit.text()),value)
        self.focal_length_label.setText('focal length: ' + str(self.fl))
        self.image_label.setPixmap(self.get_QPixmap(
            self.dc.undistort(self.fl, self.k1, self.k2, self.p1, self.p2)))

    def changeValueK1(self, value):

        self.k1 = self.calcDistortionCoefficient(int(self.k1_max_edit.text()),int(self.k1_min_edit.text()),value)
        self.k1_label.setText('k1 : ' + str(self.k1))
        self.image_label.setPixmap(self.get_QPixmap(
            self.dc.undistort(self.fl, self.k1, self.k2, self.p1, self.p2)))

    def changeValueK2(self, value):

        self.k2 = self.calcDistortionCoefficient(int(self.k2_max_edit.text()),int(self.k2_min_edit.text()),value)
        self.k2_label.setText('k2 : ' + str(self.k2))
        self.image_label.setPixmap(self.get_QPixmap(
            self.dc.undistort(self.fl, self.k1, self.k2, self.p1, self.p2)))
    
    def changeValueP1(self, value):
    
        self.p1 = self.calcDistortionCoefficient(int(self.p1_max_edit.text()),int(self.p1_min_edit.text()),value)
        self.p1_label.setText('p1 : ' + str(self.p1))
        self.image_label.setPixmap(self.get_QPixmap(
            self.dc.undistort(self.fl, self.k1, self.k2, self.p1, self.p2)))

    def changeValueP2(self, value):

        self.p2 = self.calcDistortionCoefficient(int(self.p2_max_edit.text()),int(self.p2_min_edit.text()),value)
        self.p2_label.setText('p2 : ' + str(self.p2))
        self.image_label.setPixmap(self.get_QPixmap(
            self.dc.undistort(self.fl, self.k1, self.k2, self.p1, self.p2)))
    
    def get_QPixmap(self,image):
        qimage = QImage(image.data, image.shape[1], image.shape[0],
                    image.shape[1] * 3, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        return pixmap


def main(image_path):

    app=QApplication(sys.argv)
    w=App(image_path)
    sys.exit(app.exec_())


if __name__ == '__main__':
    args=sys.argv
    if len(args) == 2:
        image_path=args[1]
        main(image_path)
    else:
        print('$ python main.py [image_path]')
        quit()
