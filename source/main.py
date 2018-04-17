# -*- coding: utf-8 -*-
import sys
from undistortion import DistortionCorrection
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSlider, QVBoxLayout, QHBoxLayout, QLineEdit, QSpinBox
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
        self.image_label = QLabel()
        self.image_label.setPixmap(self.get_QPixmap(self.dc.getImage()))
        sld_init_position = 49

        '''
        光学中心x軸用スピンボックス
        '''
        oc_x_label = QLabel('optical center x')
        self.oc_x_spin = QSpinBox()
        self.oc_x_spin.setMinimum(0)
        self.oc_x_spin.setMaximum(self.dc.getWidth() - 1)
        self.oc_x_spin.setValue(self.dc.getWidth() // 2)
        self. oc_x_spin.valueChanged.connect(self.changeValueSpin)
        oc_x_vbox = QVBoxLayout()
        oc_x_vbox.addWidget(oc_x_label)
        oc_x_vbox.addWidget(self.oc_x_spin)

        '''
        光学中心y軸用スピンボックス
        '''
        oc_y_label = QLabel('optical center y')
        self.oc_y_spin = QSpinBox()
        self.oc_y_spin.setMinimum(0)
        self.oc_y_spin.setMaximum(self.dc.getHeight()-1)
        self.oc_y_spin.setValue(self.dc.getHeight()//2)
        self.oc_y_spin.valueChanged.connect(self.changeValueSpin)
        oc_y_vbox = QVBoxLayout()
        oc_y_vbox.addWidget(oc_y_label)
        oc_y_vbox.addWidget(self.oc_y_spin)

        '''
        focal length用スライダー
        '''
        self.fl_min_edit = QLineEdit('1000')
        self.fl_min_edit.setFixedWidth(38)
        fl_min_vbox = QVBoxLayout()
        fl_min_vbox.addWidget(QLabel('min'), alignment=(Qt.AlignCenter))
        fl_min_vbox.addWidget(self.fl_min_edit)

        self.fl_max_edit = QLineEdit('5000')
        self.fl_max_edit.setFixedWidth(38)
        fl_max_vbox = QVBoxLayout()
        fl_max_vbox.addWidget(QLabel('max'), alignment=(Qt.AlignCenter))
        fl_max_vbox.addWidget(self.fl_max_edit)

        self.fl = self.calcFocalLength(float(self.fl_max_edit.text()),float(self.fl_min_edit.text()),sld_init_position)
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
        レイアウト設定
        '''

        hbox1=QHBoxLayout()
        hbox1.addLayout(oc_x_vbox)
        hbox1.addLayout(oc_y_vbox)
        hbox1.addLayout(fl_min_vbox)
        hbox1.addLayout(focal_length_vbox)
        hbox1.addLayout(fl_max_vbox)

        '''
        k1用スライダー
        '''

        self.k1_min_edit = QLineEdit('-1')
        self.k1_min_edit.setFixedWidth(38)
        k1_min_vbox = QVBoxLayout()
        k1_min_vbox.addWidget(QLabel('min'), alignment=(Qt.AlignCenter))
        k1_min_vbox.addWidget(self.k1_min_edit)

        self.k1_max_edit = QLineEdit('1')
        self.k1_max_edit.setFixedWidth(38)
        k1_max_vbox = QVBoxLayout()
        k1_max_vbox.addWidget(QLabel('max'), alignment=(Qt.AlignCenter))
        k1_max_vbox.addWidget(self.k1_max_edit)

        self.k1 = self.calcDistortionCoefficient(float(self.k1_max_edit.text()),float(self.k1_min_edit.text()),sld_init_position)
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
        self.k2_min_edit.setFixedWidth(38)
        k2_min_vbox=QVBoxLayout()
        k2_min_vbox.addWidget(QLabel('min'), alignment=(Qt.AlignCenter))
        k2_min_vbox.addWidget(self.k2_min_edit)

        self.k2_max_edit=QLineEdit('1')
        self.k2_max_edit.setFixedWidth(38)
        k2_max_vbox=QVBoxLayout()
        k2_max_vbox.addWidget(QLabel('max'), alignment=(Qt.AlignCenter))
        k2_max_vbox.addWidget(self.k2_max_edit)

        self.k2 = self.calcDistortionCoefficient(float(self.k2_max_edit.text()),float(self.k2_min_edit.text()),sld_init_position)
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
        self.p1_min_edit.setFixedWidth(38)
        p1_min_vbox = QVBoxLayout()
        p1_min_vbox.addWidget(QLabel('min'), alignment=(Qt.AlignCenter))
        p1_min_vbox.addWidget(self.p1_min_edit)

        self.p1_max_edit = QLineEdit('1')
        self.p1_max_edit.setFixedWidth(38)
        p1_max_vbox = QVBoxLayout()
        p1_max_vbox.addWidget(QLabel('max'), alignment=(Qt.AlignCenter))
        p1_max_vbox.addWidget(self.p1_max_edit)

        self.p1 = self.calcDistortionCoefficient(float(self.p1_max_edit.text()),float(self.p1_min_edit.text()),sld_init_position)
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
        self.p2_min_edit.setFixedWidth(38)
        p2_min_vbox=QVBoxLayout()
        p2_min_vbox.addWidget(QLabel('min'), alignment=(Qt.AlignCenter))
        p2_min_vbox.addWidget(self.p2_min_edit)

        self.p2_max_edit=QLineEdit('1')
        self.p2_max_edit.setFixedWidth(38)
        p2_max_vbox=QVBoxLayout()
        p2_max_vbox.addWidget(QLabel('max'), alignment=(Qt.AlignCenter))
        p2_max_vbox.addWidget(self.p2_max_edit)

        self.p2 = self.calcDistortionCoefficient(float(self.p2_max_edit.text()),float(self.p2_min_edit.text()),sld_init_position)
        self.p2_label=QLabel('p2 : ' + str(self.p2))
        self.p2_sld=QSlider(Qt.Horizontal, self)
        self.p2_sld.setFocusPolicy(Qt.NoFocus)
        self.p2_sld.setSliderPosition(sld_init_position)
        self.p2_sld.valueChanged[int].connect(self.changeValueP2)
        self.p2_sld.setMinimumWidth(200)
        p2_vbox=QVBoxLayout()
        p2_vbox.addWidget(self.p2_label, alignment=(Qt.AlignCenter))
        p2_vbox.addWidget(self.p2_sld)

        '''
        レイアウト設定
        '''

        hbox2=QHBoxLayout()
        hbox2.addLayout(k1_min_vbox)
        hbox2.addLayout(k1_vbox)
        hbox2.addLayout(k1_max_vbox)
        hbox2.addLayout(k2_min_vbox)
        hbox2.addLayout(k2_vbox)
        hbox2.addLayout(k2_max_vbox)
        hbox2.addLayout(p1_min_vbox)
        hbox2.addLayout(p1_vbox)
        hbox2.addLayout(p1_max_vbox)
        hbox2.addLayout(p2_min_vbox)
        hbox2.addLayout(p2_vbox)
        hbox2.addLayout(p2_max_vbox)

        '''
        k3用スライダー
        '''

        self.k3_min_edit = QLineEdit('-1')
        self.k3_min_edit.setFixedWidth(38)
        k3_min_vbox = QVBoxLayout()
        k3_min_vbox.addWidget(QLabel('min'), alignment=(Qt.AlignCenter))
        k3_min_vbox.addWidget(self.k3_min_edit)

        self.k3_max_edit = QLineEdit('1')
        self.k3_max_edit.setFixedWidth(38)
        k3_max_vbox = QVBoxLayout()
        k3_max_vbox.addWidget(QLabel('max'), alignment=(Qt.AlignCenter))
        k3_max_vbox.addWidget(self.k3_max_edit)

        self.k3 = self.calcDistortionCoefficient(float(self.k3_max_edit.text()),float(self.k3_min_edit.text()),sld_init_position)
        self.k3_label=QLabel('k3 : ' + str(self.k3))
        self.k3_sld=QSlider(Qt.Horizontal, self)
        self.k3_sld.setFocusPolicy(Qt.NoFocus)
        self.k3_sld.setSliderPosition(sld_init_position)
        self.k3_sld.valueChanged[int].connect(self.changeValueK3)
        self.k3_sld.setMinimumWidth(200)
        k3_vbox=QVBoxLayout()
        k3_vbox.addWidget(self.k3_label, alignment=(Qt.AlignCenter))
        k3_vbox.addWidget(self.k3_sld)


        '''
        k4用スライダー
        '''

        self.k4_min_edit=QLineEdit('-1')
        self.k4_min_edit.setFixedWidth(38)
        k4_min_vbox=QVBoxLayout()
        k4_min_vbox.addWidget(QLabel('min'), alignment=(Qt.AlignCenter))
        k4_min_vbox.addWidget(self.k4_min_edit)

        self.k4_max_edit=QLineEdit('1')
        self.k4_max_edit.setFixedWidth(38)
        k4_max_vbox=QVBoxLayout()
        k4_max_vbox.addWidget(QLabel('max'), alignment=(Qt.AlignCenter))
        k4_max_vbox.addWidget(self.k4_max_edit)

        self.k4 = self.calcDistortionCoefficient(float(self.k4_max_edit.text()),float(self.k4_min_edit.text()),sld_init_position)
        self.k4_label=QLabel('k4 : ' + str(self.k4))
        self.k4_sld=QSlider(Qt.Horizontal, self)
        self.k4_sld.setFocusPolicy(Qt.NoFocus)
        self.k4_sld.setSliderPosition(sld_init_position)
        self.k4_sld.valueChanged[int].connect(self.changeValueK4)
        self.k4_sld.setMinimumWidth(200)
        k4_vbox=QVBoxLayout()
        k4_vbox.addWidget(self.k4_label, alignment=(Qt.AlignCenter))
        k4_vbox.addWidget(self.k4_sld)

        
        '''
        k5用スライダー
        '''

        self.k5_min_edit=QLineEdit('-1')
        self.k5_min_edit.setFixedWidth(38)
        k5_min_vbox=QVBoxLayout()
        k5_min_vbox.addWidget(QLabel('min'), alignment=(Qt.AlignCenter))
        k5_min_vbox.addWidget(self.k5_min_edit)

        self.k5_max_edit=QLineEdit('1')
        self.k5_max_edit.setFixedWidth(38)
        k5_max_vbox=QVBoxLayout()
        k5_max_vbox.addWidget(QLabel('max'), alignment=(Qt.AlignCenter))
        k5_max_vbox.addWidget(self.k5_max_edit)

        self.k5 = self.calcDistortionCoefficient(float(self.k5_max_edit.text()),float(self.k5_min_edit.text()),sld_init_position)
        self.k5_label=QLabel('k5 : ' + str(self.k5))
        self.k5_sld=QSlider(Qt.Horizontal, self)
        self.k5_sld.setFocusPolicy(Qt.NoFocus)
        self.k5_sld.setSliderPosition(sld_init_position)
        self.k5_sld.valueChanged[int].connect(self.changeValueK5)
        self.k5_sld.setMinimumWidth(200)
        k5_vbox=QVBoxLayout()
        k5_vbox.addWidget(self.k5_label, alignment=(Qt.AlignCenter))
        k5_vbox.addWidget(self.k5_sld)

        '''
        k6用スライダー
        '''

        self.k6_min_edit=QLineEdit('-1')
        self.k6_min_edit.setFixedWidth(38)
        k6_min_vbox=QVBoxLayout()
        k6_min_vbox.addWidget(QLabel('min'), alignment=(Qt.AlignCenter))
        k6_min_vbox.addWidget(self.k6_min_edit)

        self.k6_max_edit=QLineEdit('1')
        self.k6_max_edit.setFixedWidth(38)
        k6_max_vbox=QVBoxLayout()
        k6_max_vbox.addWidget(QLabel('max'), alignment=(Qt.AlignCenter))
        k6_max_vbox.addWidget(self.k6_max_edit)

        self.k6 = self.calcDistortionCoefficient(float(self.k6_max_edit.text()),float(self.k6_min_edit.text()),sld_init_position)
        self.k6_label=QLabel('k6 : ' + str(self.k6))
        self.k6_sld=QSlider(Qt.Horizontal, self)
        self.k6_sld.setFocusPolicy(Qt.NoFocus)
        self.k6_sld.setSliderPosition(sld_init_position)
        self.k6_sld.valueChanged[int].connect(self.changeValueK6)
        self.k6_sld.setMinimumWidth(200)
        k6_vbox=QVBoxLayout()
        k6_vbox.addWidget(self.k6_label, alignment=(Qt.AlignCenter))
        k6_vbox.addWidget(self.k6_sld)

        '''
        レイアウト設定
        '''
        
        hbox3=QHBoxLayout()
        hbox3.addLayout(k3_min_vbox)
        hbox3.addLayout(k3_vbox)
        hbox3.addLayout(k3_max_vbox)
        hbox3.addLayout(k4_min_vbox)
        hbox3.addLayout(k4_vbox)
        hbox3.addLayout(k4_max_vbox)
        hbox3.addLayout(k5_min_vbox)
        hbox3.addLayout(k5_vbox)
        hbox3.addLayout(k5_max_vbox)
        hbox3.addLayout(k6_min_vbox)
        hbox3.addLayout(k6_vbox)
        hbox3.addLayout(k6_max_vbox)

        vbox=QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
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

    def convert(self):
        pixmap= self.get_QPixmap(
            self.dc.undistort(self.oc_x_spin.value(),self.oc_y_spin.value(),self.fl, k1=self.k1, k2=self.k2, p1=self.p1, p2=self.p2, k3=self.k3, k4=self.k4, k5=self.k5, k6=self.k6))
        return pixmap

    def changeValueSpin(self):
        self.image_label.setPixmap(self.convert())
        
    def changeValueFl(self, value):
        self.fl = self.calcFocalLength(float(self.fl_max_edit.text()),float(self.fl_min_edit.text()),value)
        self.focal_length_label.setText('focal length: ' + str(self.fl))
        self.image_label.setPixmap(self.convert())

    def changeValueK1(self, value):

        self.k1 = self.calcDistortionCoefficient(float(self.k1_max_edit.text()),float(self.k1_min_edit.text()),value)
        self.k1_label.setText('k1 : ' + str(self.k1))
        self.image_label.setPixmap(self.convert())

    def changeValueK2(self, value):

        self.k2 = self.calcDistortionCoefficient(float(self.k2_max_edit.text()),float(self.k2_min_edit.text()),value)
        self.k2_label.setText('k2 : ' + str(self.k2))
        self.image_label.setPixmap(self.convert())
    
    def changeValueP1(self, value):
    
        self.p1 = self.calcDistortionCoefficient(float(self.p1_max_edit.text()),float(self.p1_min_edit.text()),value)
        self.p1_label.setText('p1 : ' + str(self.p1))
        self.image_label.setPixmap(self.convert())

    def changeValueP2(self, value):

        self.p2 = self.calcDistortionCoefficient(float(self.p2_max_edit.text()),float(self.p2_min_edit.text()),value)
        self.p2_label.setText('p2 : ' + str(self.p2))
        self.image_label.setPixmap(self.convert())
    
    def changeValueK3(self, value):
    
        self.k3 = self.calcDistortionCoefficient(float(self.k3_max_edit.text()),float(self.k3_min_edit.text()),value)
        self.k3_label.setText('k3 : ' + str(self.k3))
        self.image_label.setPixmap(self.convert())

    def changeValueK4(self, value):
    
        self.k4 = self.calcDistortionCoefficient(float(self.k4_max_edit.text()),float(self.k4_min_edit.text()),value)
        self.k4_label.setText('k4 : ' + str(self.k4))
        self.image_label.setPixmap(self.convert())
    
    def changeValueK5(self, value):
    
        self.k5 = self.calcDistortionCoefficient(float(self.k5_max_edit.text()),float(self.k5_min_edit.text()),value)
        self.k5_label.setText('k5 : ' + str(self.k5))
        self.image_label.setPixmap(self.convert())
    
    def changeValueK6(self, value):
    
        self.k6 = self.calcDistortionCoefficient(float(self.k6_max_edit.text()),float(self.k6_min_edit.text()),value)
        self.k6_label.setText('k6 : ' + str(self.k6))
        self.image_label.setPixmap(self.convert())

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
