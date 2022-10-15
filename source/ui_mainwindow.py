# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTabWidget, QTableView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.circulationListTab = QWidget()
        self.circulationListTab.setObjectName(u"circulationListTab")
        self.verticalLayout_2 = QVBoxLayout(self.circulationListTab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.importPushButton = QPushButton(self.circulationListTab)
        self.importPushButton.setObjectName(u"importPushButton")

        self.horizontalLayout.addWidget(self.importPushButton)

        self.deletePushButton = QPushButton(self.circulationListTab)
        self.deletePushButton.setObjectName(u"deletePushButton")

        self.horizontalLayout.addWidget(self.deletePushButton)

        self.printPushButton = QPushButton(self.circulationListTab)
        self.printPushButton.setObjectName(u"printPushButton")

        self.horizontalLayout.addWidget(self.printPushButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.circulationListTableView = QTableView(self.circulationListTab)
        self.circulationListTableView.setObjectName(u"circulationListTableView")

        self.verticalLayout.addWidget(self.circulationListTableView)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.verticalLayout_3.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.verticalLayout_3)

        self.tabWidget.addTab(self.circulationListTab, "")
        self.itemListTab = QWidget()
        self.itemListTab.setObjectName(u"itemListTab")
        self.gridLayout_3 = QGridLayout(self.itemListTab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.itemListTab)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.itemIdTextEdit = QLineEdit(self.itemListTab)
        self.itemIdTextEdit.setObjectName(u"itemIdTextEdit")

        self.horizontalLayout_2.addWidget(self.itemIdTextEdit)

        # self.findItemPushButton = QPushButton(self.itemListTab)
        # self.findItemPushButton.setObjectName(u"findItemPushButton")

        # self.horizontalLayout_2.addWidget(self.findItemPushButton)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.deleteItemRecordPushButton = QPushButton(self.itemListTab)
        self.deleteItemRecordPushButton.setObjectName(u"deleteItemRecordPushButton")

        self.horizontalLayout_2.addWidget(self.deleteItemRecordPushButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.itemRecordTableView = QTableView(self.itemListTab)
        self.itemRecordTableView.setObjectName(u"itemRecordTableView")

        self.verticalLayout_5.addWidget(self.itemRecordTableView)


        self.verticalLayout_4.addLayout(self.verticalLayout_5)


        self.gridLayout_3.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        self.tabWidget.addTab(self.itemListTab, "")

        self.gridLayout_2.addWidget(self.tabWidget, 0, 1, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u6d41\u8f6c\u5355&\u7269\u6599\u5355", None))
        self.importPushButton.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165", None))
        self.deletePushButton.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664", None))
        self.printPushButton.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5370", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.circulationListTab), QCoreApplication.translate("MainWindow", u"\u6d41\u8f6c\u5355", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u90e8\u54c1\u756a\u53f7\uff1a", None))
        # self.findItemPushButton.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u627e", None))
        self.deleteItemRecordPushButton.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.itemListTab), QCoreApplication.translate("MainWindow", u"\u7269\u6599\u5355", None))
    # retranslateUi

