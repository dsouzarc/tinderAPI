import sys;
import urllib;
from PyQt4 import QtGui, QtCore

from Tinder import Tinder;
from Person import Person;


class TinderGui(QtGui.QWidget):

    tinder = None;
    recommendations = None;

    currentImageLabel = None;
    swipeRightButton = None;
    swipeLeftButton = None;
    photoIndex = None;

    def __init__(self):
        super(TinderGui, self).__init__();

        self.photoIndex = 0;
        self.tinder = Tinder(fileName="credentials.json");
        self.recommendations = self.tinder.getRecommendations();

        if len(self.recommendations) == 0:
            print("0 RECOMMENDATIONS")
            return;

        self.initUI();

    def initUI(self):

        self.createUIComponents();
        self.displayPhoto();

        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addStretch(1)

        mainLayout.addWidget(self.swipeLeftButton);
        mainLayout.addWidget(self.swipeRightButton);
        mainLayout.addWidget(self.currentImageLabel)

        self.setLayout(mainLayout)

        print("NUM PHOTOS: " + str(len(self.recommendations[0].photos)))

        self.setWindowTitle('Tinder Bot');
        self.setWindowIcon(QtGui.QIcon('tinder_icon.png'));
        self.resize(500, 500);
        self.center();
        self.show()
        
    def keyPressEvent (self, eventQKeyEvent):
        QtGui.QWidget.keyPressEvent(self, eventQKeyEvent)

        key = eventQKeyEvent.key();

        print("HERE: " + str(self.photoIndex))

        if key == QtCore.Qt.Key_Left:
            self.swipeLeft();
        elif key == QtCore.Qt.Key_Right:
            self.swipeRight();

        elif key == QtCore.Qt.Key_Up:
            self.photoIndex -= 1;
            if self.photoIndex < 0:
                self.photoIndex = len(self.recommendations[0].photos) - 1;
            self.displayPhoto();

        elif key == QtCore.Qt.Key_Down:
            self.photoIndex += 1;
            if self.photoIndex >= len(self.recommendations[0].photos):
                self.photoIndex = 0;
            self.displayPhoto();


    def displayPhoto(self):
        url = self.recommendations[0].photos[self.photoIndex];
        data = urllib.urlopen(url).read();

        image = QtGui.QImage()
        image.loadFromData(data)

        self.currentImageLabel.setPixmap(QtGui.QPixmap(image))

    def createUIComponents(self):
        self.currentImageLabel = QtGui.QLabel(self)

        self.swipeRightButton = QtGui.QPushButton('Right', self);
        self.swipeLeftButton = QtGui.QPushButton('Left', self);

        self.swipeRightButton.clicked.connect(self.swipeRight);
        self.swipeLeftButton.clicked.connect(self.swipeLeft);


    def swipeRight(self):
        print("Swiped right");

    def swipeLeft(self):
        print("Swiped left");


    '''
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()        
    '''

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        

def main():
    app = QtGui.QApplication(sys.argv);
    tinderGui = TinderGui();
    sys.exit(app.exec_());


if __name__ == '__main__':
    main();
   
