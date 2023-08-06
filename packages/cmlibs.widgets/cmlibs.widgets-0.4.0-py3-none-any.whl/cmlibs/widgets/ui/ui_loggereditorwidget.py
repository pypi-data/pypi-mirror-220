# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loggereditorwidget.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QPushButton,
    QSizePolicy, QSpacerItem, QTextBrowser, QWidget)
class Ui_LoggerEditorWidget(object):
    def setupUi(self, LoggerEditorWidget):
        if not LoggerEditorWidget.objectName():
            LoggerEditorWidget.setObjectName(u"LoggerEditorWidget")
        LoggerEditorWidget.resize(452, 533)
        self.gridLayout = QGridLayout(LoggerEditorWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.logText = QTextBrowser(LoggerEditorWidget)
        self.logText.setObjectName(u"logText")

        self.gridLayout.addWidget(self.logText, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.clearAllButton = QPushButton(LoggerEditorWidget)
        self.clearAllButton.setObjectName(u"clearAllButton")

        self.horizontalLayout.addWidget(self.clearAllButton)

        self.copyButton = QPushButton(LoggerEditorWidget)
        self.copyButton.setObjectName(u"copyButton")

        self.horizontalLayout.addWidget(self.copyButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.retranslateUi(LoggerEditorWidget)
        self.clearAllButton.clicked.connect(LoggerEditorWidget.clearAll)
        self.copyButton.clicked.connect(LoggerEditorWidget.copyToClipboard)

        QMetaObject.connectSlotsByName(LoggerEditorWidget)
    # setupUi

    def retranslateUi(self, LoggerEditorWidget):
        LoggerEditorWidget.setWindowTitle(QCoreApplication.translate("LoggerEditorWidget", u"Log viewer", None))
        self.clearAllButton.setText(QCoreApplication.translate("LoggerEditorWidget", u"Clear All", None))
        self.copyButton.setText(QCoreApplication.translate("LoggerEditorWidget", u"Copy To Clipboard", None))
    # retranslateUi

