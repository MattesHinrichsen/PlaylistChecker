# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QGridLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QTableView, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1200, 500)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Widget.sizePolicy().hasHeightForWidth())
        Widget.setSizePolicy(sizePolicy)
        Widget.setMaximumSize(QSize(100000, 16777215))
        Widget.setBaseSize(QSize(0, 0))
        self.gridLayout = QGridLayout(Widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.PlaylistBox = QComboBox(Widget)
        self.PlaylistBox.setObjectName(u"PlaylistBox")

        self.gridLayout.addWidget(self.PlaylistBox, 0, 2, 1, 1)

        self.PlaylistLabel = QLabel(Widget)
        self.PlaylistLabel.setObjectName(u"PlaylistLabel")

        self.gridLayout.addWidget(self.PlaylistLabel, 0, 1, 1, 1)

        self.diffButton = QPushButton(Widget)
        self.diffButton.setObjectName(u"diffButton")

        self.gridLayout.addWidget(self.diffButton, 1, 2, 1, 1)

        self.DifferenceTable = QTableView(Widget)
        self.DifferenceTable.setObjectName(u"DifferenceTable")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.DifferenceTable.sizePolicy().hasHeightForWidth())
        self.DifferenceTable.setSizePolicy(sizePolicy1)
        self.DifferenceTable.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.DifferenceTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.gridLayout.addWidget(self.DifferenceTable, 3, 1, 1, 2)

        self.ResultLabel = QLabel(Widget)
        self.ResultLabel.setObjectName(u"ResultLabel")
        self.ResultLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.ResultLabel, 2, 1, 1, 2)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.PlaylistLabel.setText(QCoreApplication.translate("Widget", u"Selected Playlist:         ", None))
        self.diffButton.setText(QCoreApplication.translate("Widget", u"Run Difference Check", None))
        self.ResultLabel.setText("")
    # retranslateUi

