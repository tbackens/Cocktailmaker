from PyQt5 import QtWidgets, uic, QtCore ,QtTest, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, QSize
from PyQt5.QtWidgets import *
import sys
from config import drink_list, pump_config
import time
import json

class ProgressThread(QThread):
    _progSignal = pyqtSignal(int)
    def __init__(self, runtime):
        super(ProgressThread, self).__init__()
        self.runtime = runtime
    def __del__(self):
        self.wait()
    def run(self):
        for i in range(101):
            time.sleep(self.runtime/100)
            self._progSignal.emit(i)

class PumpThread(QThread):
    _statusSignal = pyqtSignal(str)
    def __init__(self,ings=[], pumps=[], values=[],gpio=[], factor=0):
        super(PumpThread, self).__init__()
        self.ings = ings
        self.pumps = pumps
        self.values = values
        self.gpio = gpio
        self.factor = factor
    def __del__(self):
        self.wait()
    def run(self):
        for ing, pump, value, gpio in zip(self.ings, self.pumps, self.values, self.gpio):
            print(f'Pump {pump}, {value}ml. GPIO: {gpio}')
            self._statusSignal.emit(f'PUMPE {pump}: {ing} -- {value}ml')
            time.sleep(value * self.factor)

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('PumpSet.ui', self)

class SizeWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('sizeSet.ui', self)

class PumpWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('sizeSet.ui', self)



class Ui(QtWidgets.QMainWindow):
#-Init---------------------------------------------------------------------
    def __init__(self):
        super().__init__()
        uic.loadUi('app.ui', self)
        #self.show()

        self.action_btn = self.findChild(QtWidgets.QPushButton, 'action_btn') 
        self.action_btn.clicked.connect(self.start_request)
        self.action_btn.pressed.connect(self.action_hold)
        self.action_btn.released.connect(self.action_release)

        self.action_btn.hide()

        self.option_btn = self.findChild(QtWidgets.QPushButton, 'option_btn') 
        self.option_btn.clicked.connect(self.option_btn_pressed)
        self.option_btn.setText('Info...')

        self.option_btn.hide()

        self.toggle_btn = self.findChild(QtWidgets.QPushButton, 'toggle_btn') 
        self.toggle_btn.clicked.connect(self.toggle_menu)

        self.list_widget = self.findChild(QtWidgets.QListWidget, 'list_widget')
        self.list_widget.itemClicked.connect(self.selection_handler)


        self.name_label = self.findChild(QtWidgets.QLabel, 'name_label')
        self.name_label.setText('')

        self.progressbar = self.findChild(QtWidgets.QProgressBar, 'progressBar')
        self.progressbar.setValue(0)

        self.statusbar = self.findChild(QtWidgets.QStatusBar, 'statusbar')

        self.settings_btn = self.findChild(QtWidgets.QPushButton, 'settingsButton') 
        self.settings_btn.clicked.connect(self.settings_btn_clicked)



        self.pump_list = []
        self.get_pumps()

        self.manual_mode = False
        self.pumping = False
        self.selected = False
        self.cocktail_number = 0
        self.show_cocktail_list()


    def get_pumps(self):
        self.pump_list= json.load(open('pump_config.json'))


    def show_cocktail_list(self):
        self.selected = False
        self.list_widget.clear()
        self.manual_mode = False
        index = 0
        for i in drink_list:
            self.list_widget.insertItem(index, i['name'].upper())
            index += 1
        self.toggle_btn.setText('Manuell...')
        self.action_btn.setText('START')
        self.name_label.setText('<-- Bitte auswählen')
        self.action_btn.hide()

    def show_manu_list(self):
        self.selected = False
        self.list_widget.clear()
        self.manual_mode = True
        index = 0
        for pump in self.pump_list:
            self.list_widget.insertItem(index, pump['name'].upper())
            index += 1
        self.toggle_btn.setText('Cocktails...')
        self.name_label.setText('<-- Bitte auswählen')
        self.option_btn.hide()
        self.action_btn.hide()
        self.action_btn.setText('PUSH and HOLD')


    def selection_handler(self):
        self.selected = True
        self.action_btn.show()
        self.name_label.setText((self.list_widget.currentItem().text()).upper())
        if not self.manual_mode:
            self.option_btn.show()

    def start_request(self):
        if not self.manual_mode and self.selected == True:
            try:
                req_box = QMessageBox()
                req_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                req_box.setText((self.list_widget.currentItem().text()).upper())
                req_box.setIcon(QMessageBox.Question)
                req_box.setInformativeText('Starten?')
                ings = []
                for i in drink_list[self.list_widget.currentRow()]['ingredients'].keys():
                    ings.append(i)
                message = '\n'.join(ings).upper()
                req_box.setDetailedText(message)
                req_box.exec()
                button = req_box.clickedButton()
                sb = req_box.standardButton(button)
                if sb == QMessageBox.Ok:
                    self.start()
            except AttributeError:
                print("no selection!")

    def hide_buttons(self):
        self.action_btn.hide()
        self.option_btn.hide()
        self.toggle_btn.hide()
    def show_buttons(self):
        self.action_btn.show()
        self.option_btn.show()
        self.toggle_btn.show()

    def start(self):
        if not self.manual_mode and self.selected == True:
            try:
                print(self.list_widget.currentRow(), self.list_widget.currentItem().text())
                self.hide_buttons()
                self.cocktail_number = self.list_widget.currentRow()
                factor = 0.1
                pumps = []
                ings = []
                gpio = []
                values = []
                runtime = 0
                self.get_pumps()
                for pump in self.pump_list:
                    if pump['name'] in drink_list[self.list_widget.currentRow()]['ingredients'].keys():
                        pumps.append(pump['pump'])
                        gpio.append(pump['GPIO'])
                for value in drink_list[self.list_widget.currentRow()]['ingredients'].values():
                    values.append(value)
                    runtime += (value * factor)
                for ing in drink_list[self.list_widget.currentRow()]['ingredients'].keys():
                    ings.append(ing)
                
                self.pump_thread = PumpThread(ings, pumps, values, gpio, factor)
                self.pump_thread._statusSignal.connect(self.status_signal)
                self.pump_thread.start()

                self.prog_thread = ProgressThread(runtime)
                self.prog_thread._progSignal.connect(self.progress_signal)
                self.prog_thread.start()
            except AttributeError:
                print("no selection!")

    def progress_signal(self, msg):
        self.progressbar.setValue(int(msg))
        if self.progressbar.value() == 100:
            self.statusbar.showMessage('Fertig', 2000)
            self.progressbar.setValue(0)
            ready = QMessageBox()
            ready.setStandardButtons(QMessageBox.Ok)
            ready.setText(self.list_widget.currentItem().text())
            ready.setInformativeText('Fertig! -- PROST!')
            ready.exec()
            button = ready.clickedButton()
            bt = ready.standardButton(button)
            if bt == QMessageBox.Ok:
                self.show_buttons()

    
    def status_signal(self, msg):
        self.statusbar.showMessage(msg)

    def action_hold(self):
        try:
            if self.manual_mode:
                print(f'pump {self.list_widget.currentRow()} START! -- {self.list_widget.currentItem().text()}')
        except AttributeError:
            print("no selection!")

    def action_release(self):
        try:
            if self.manual_mode:
                print(f'pump {self.list_widget.currentRow()} STOP! -- {self.list_widget.currentItem().text()}')
        except AttributeError:
            print("no selection!")


    def settings_btn_clicked(self):
        self.w = SettingsWindow()
        self.w.show()

    def size_btn_clicked(self):
        self.size_window = SizeWindow()
        self.size_window.show()


    def option_btn_pressed(self):
        ings = []
        for i in drink_list[self.list_widget.currentRow()]['ingredients'].keys():
            ings.append(i)
        message = '\n'.join(ings).upper()
        msbx = QMessageBox()
        msbx.setIcon(msbx.Information)
        msbx.setText('Zutaten')
        msbx.setInformativeText(message)
        msbx.exec()


    def show_settings(self):

        pass




    def toggle_menu(self):
        if self.manual_mode:
            self.show_cocktail_list()
            self.name_label.setText('')
        else:
            self.show_manu_list()
            self.name_label.setText('')



app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()