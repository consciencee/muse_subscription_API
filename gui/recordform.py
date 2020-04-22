from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import *
import datetime
import pathlib


class RecordForm(QtWidgets.QWidget):
    start_record = pyqtSignal('QString', 'QString')
    stop_record = pyqtSignal()

    def __init__(self):
        super(RecordForm, self).__init__()

        self.record_btt = QtWidgets.QPushButton('Start')
        self.record_status_lbl = QtWidgets.QLabel('')
        self.record_status = 0
        self.record_btt.clicked.connect(self.on_rec_clicked)

        self.record_time_lbl = QtWidgets.QLabel('')
        self.record_timer = QTimer(self)
        self.seconds_recorded = 0
        self.record_timer.timeout.connect(self.update_time_lbl)

        self.dir_edit_btt = QtWidgets.QPushButton('Browse...')
        self.dirname = str(pathlib.Path().absolute())
        self.dirname_lbl = QtWidgets.QLabel(self.dirname)
        self.filename_edit = QtWidgets.QLineEdit('')
        self.dir_edit_btt.clicked.connect(self.show_select_dir_dialog)

        outputsettings_layout = QtWidgets.QVBoxLayout()
        filesettings_layout = QtWidgets.QHBoxLayout()
        dirsettings_layout = QtWidgets.QHBoxLayout()

        filesettings_layout.addWidget(QtWidgets.QLabel('Filename:'))
        filesettings_layout.addWidget(self.filename_edit)

        dirsettings_layout.addWidget(QtWidgets.QLabel('Directory:'))
        dirsettings_layout.addWidget(self.dirname_lbl)
        dirsettings_layout.addWidget(self.dir_edit_btt)

        outputsettings_layout.addLayout(dirsettings_layout)
        outputsettings_layout.addLayout(filesettings_layout)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(outputsettings_layout)
        main_layout.addWidget(QtWidgets.QLabel())
        main_layout.addWidget(self.record_btt)
        main_layout.addWidget(self.record_status_lbl)
        main_layout.addWidget(self.record_time_lbl)

        self.setLayout(main_layout)

    def on_rec_clicked(self):
        if self.record_status == 0:
            self.record_status = 1
            self.start_record_process()
        else:
            self.record_status = 0
            self.stop_record_process()

    def start_record_process(self):
        self.record_btt.setText('Stop')
        self.filename_edit.setEnabled(False)
        self.record_status_lbl.setText('Recording to file ' + self.filename_edit.text() + ' ...')
        self.start_record.emit(self.dirname, self.filename_edit.text())
        self.record_timer.start(1000)
        self.seconds_recorded = 0

    def stop_record_process(self):
        self.record_btt.setText('Start')
        self.filename_edit.setEnabled(True)
        self.record_status_lbl.setText('Record completed: ' + self.filename_edit.text() + ' .')
        self.stop_record.emit()
        self.record_timer.stop()

    def show_select_dir_dialog(self):
        self.dirname = QtWidgets.QFileDialog.getExistingDirectory(self, "Select directory", directory=self.dirname)
        self.dirname_lbl.setText(self.dirname)

    def update_time_lbl(self):
        self.seconds_recorded += 1
        self.record_time_lbl.setText(str(datetime.timedelta(seconds=self.seconds_recorded)))
