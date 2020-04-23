from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import *
import datetime
import pathlib


class RecordForm(QtWidgets.QFrame):
    start_record = pyqtSignal('QString', 'QString')
    stop_record = pyqtSignal()

    def __init__(self):
        super(RecordForm, self).__init__()

        self.record_btt = QtWidgets.QPushButton('Start')
        self.record_status_lbl = QtWidgets.QLabel('')
        self.record_status = 0
        self.record_btt.clicked.connect(self.on_rec_clicked)
        self.record_btt.setProperty('class', 'record-btt')

        self.record_time_lbl = QtWidgets.QLabel('')
        self.record_timer = QTimer(self)
        self.seconds_recorded = 0
        self.record_timer.timeout.connect(self.update_time_lbl)
        self.record_time_lbl.setProperty('class', 'time-lbl')

        self.dir_edit_btt = QtWidgets.QPushButton('Browse...')
        self.dirname = str(pathlib.Path().absolute())
        self.dirname_lbl = QtWidgets.QLabel(self.dirname)
        self.filename_edit = QtWidgets.QLineEdit('')
        self.file_check_status = QtWidgets.QLabel('')
        self.dir_edit_btt.clicked.connect(self.show_select_dir_dialog)
        self.dir_edit_btt.setProperty('class', 'browse-btt')
        self.filename_edit.textEdited.connect(self.check_file_status)
        self.file_check_status.setProperty('class', 'warn-lbl')

        outputsettings_layout = QtWidgets.QVBoxLayout()
        filesettings_layout = QtWidgets.QHBoxLayout()
        dirsettings_layout = QtWidgets.QHBoxLayout()

        filesettings_layout.addWidget(QtWidgets.QLabel('Filename:'))
        filesettings_layout.addWidget(self.filename_edit)
        filesettings_layout.addWidget(self.file_check_status)
        filesettings_layout.setAlignment(self.filename_edit, Qt.AlignLeft)
        filesettings_layout.setAlignment(self.file_check_status, Qt.AlignLeft)
        filesettings_layout.addStretch(1)

        dirsettings_layout.addWidget(QtWidgets.QLabel('Directory:'))
        dirsettings_layout.addWidget(self.dirname_lbl)
        dirsettings_layout.addWidget(self.dir_edit_btt)
        dirsettings_layout.setAlignment(Qt.AlignLeft)

        outputsettings_layout.addLayout(dirsettings_layout)
        outputsettings_layout.addLayout(filesettings_layout)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(outputsettings_layout)
        main_layout.addWidget(QtWidgets.QLabel())
        main_layout.addWidget(self.record_btt)
        main_layout.setAlignment(self.record_btt, Qt.AlignCenter)

        status_layout = QtWidgets.QHBoxLayout()
        status_layout.addWidget(self.record_status_lbl)
        status_layout.addWidget(self.record_time_lbl)
        status_layout.setAlignment(self.record_time_lbl, Qt.AlignRight)

        main_layout.addLayout(status_layout)

        self.setLayout(main_layout)

    def on_rec_clicked(self):
        if self.record_status == 0:
            self.start_record_process()
        else:
            self.stop_record_process()

    def start_record_process(self):
        if not self.check_file_status(self.filename_edit.text()):
            return
        self.record_status = 1
        self.record_btt.setText('Stop')
        self.filename_edit.setEnabled(False)
        self.record_status_lbl.setText('Recording to file ' + self.filename_edit.text() + ' ...')
        self.start_record.emit(self.dirname, self.filename_edit.text())
        self.record_timer.start(1000)
        self.seconds_recorded = 0

    def stop_record_process(self):
        self.record_status = 0
        self.record_btt.setText('Start')
        self.filename_edit.setEnabled(True)
        self.record_status_lbl.setText('Record completed: ' + self.filename_edit.text() + ' .')
        self.stop_record.emit()
        self.record_timer.stop()

    def show_select_dir_dialog(self):
        dirname = QtWidgets.QFileDialog.getExistingDirectory(self, "Select directory", directory=self.dirname)
        if dirname != '':
            self.dirname = dirname
        self.dirname_lbl.setText(self.dirname)

    def update_time_lbl(self):
        self.seconds_recorded += 1
        self.record_time_lbl.setText(str(datetime.timedelta(seconds=self.seconds_recorded)))

    def check_file_status(self, filename):
        if filename == '':
            self.file_check_status.setText('Enter file name')
            return False
        if (pathlib.Path(self.dirname) / filename).is_file():
            self.file_check_status.setText('File already exists. Its contents will be overwritten.')
            return True
        if (pathlib.Path(self.dirname) / filename).is_dir():
            self.file_check_status.setText('Directory names are not allowed.')
            return False
        self.file_check_status.setText('')
        return True
