import os
from pathlib import Path
import sys
import pandas as pd

from ReplaceMenu import ReplaceMenu
from Difference_Checker import to_file, retrieveData, compare

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QComboBox, QTableView, QMainWindow, QMenu, QDialog, QHeaderView
from PySide6.QtCore import QFile, QAbstractTableModel, Qt, QEvent, QPointF
from PySide6.QtUiTools import QUiLoader

import googleapiclient.discovery
import googleapiclient.errors
from oauth2client import client 
from oauth2client import tools 
from oauth2client.file import Storage 
from oauth2client.tools import argparser


class PandasModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row()][index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

class Playlists:
    def __init__(self, id, name, difference_data) -> None:
        self.id = id
        self.name = name
        self.difference_data = difference_data


class PlaylistChecker(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = self.load_ui()

        self.setWindowTitle("Youtube Playlist Checker")
        self.resize(1000,500)

        self.playlists = []
        
        self.youtube = self.setup_api()
        self.setup_playlists()
        self.generate_table()

        self.ui.PlaylistBox.currentIndexChanged.connect(self.generate_table)
        self.ui.diffButton.clicked.connect(self.run_difference_check)
        self.ui.DifferenceTable.installEventFilter(self)  


    def closeEvent(self, event):
        for playlist in self.playlists:
            if playlist.difference_data is not None:
                playlist.difference_data.to_csv(os.path.realpath(os.path.dirname(__file__)) + "/data/playlistDifferences/{}.csv".format(playlist.id), encoding='utf-8', sep=",", index=False, mode='w')

    def eventFilter(self, object, event):
        if (object.objectName() == "DifferenceTable"):
            if event.type() == QEvent.Type.ContextMenu and self.ui.DifferenceTable.selectedIndexes():
                # Row print(self.ui.DifferenceTable.selectedIndexes()[0].row())
                menu = QMenu(self)
                replace = menu.addAction('Replace with new video')
                delete = menu.addAction('Delete entry')
                replace.triggered.connect(self.open_replace_menu)
                delete.triggered.connect(self.delete_entry)
                menu.exec(event.globalPos())

        return super().eventFilter(object, event)   

    def open_replace_menu(self):
        row_index = self.ui.DifferenceTable.selectedIndexes()[0].row()
        playlist_index = self.ui.PlaylistBox.currentIndex()
        dialog = ReplaceMenu(self.playlists[playlist_index].difference_data.iloc[[row_index]], self.youtube, self.playlists[playlist_index].id)   
        result = dialog.exec()  
        if result == 1: #Success
            self.playlists[playlist_index].difference_data.at[row_index, "Replaced"] = True


    def delete_entry(self):
        row_index = self.ui.DifferenceTable.selectedIndexes()[0].row()
        playlist_index = self.ui.PlaylistBox.currentIndex()
        self.playlists[playlist_index].difference_data = self.playlists[playlist_index].difference_data.drop(row_index)
        self.generate_table()


    def load_ui(self):
        loader = QUiLoader()
        path = Path(__file__).resolve().parent / "mainwindow.ui"
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file, self)
        ui_file.close()
        return ui


    def generate_table(self):
        playlist_index = self.ui.PlaylistBox.currentIndex()
        if self.playlists[playlist_index].difference_data is not None:
            self.model = PandasModel(self.playlists[playlist_index].difference_data)
            self.ui.DifferenceTable.setModel(self.model)
        else:
            df = pd.DataFrame({"VideoName": [], "ChannelName": [] , "Reason": [], "Time": [], "Replaced": [], "Position": [], "VideoId": []})
            self.model = PandasModel(df)
            self.ui.DifferenceTable.setModel(self.model)

        self.ui.DifferenceTable.setColumnHidden(7,True)
        self.ui.DifferenceTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        for i in range(1,7):
            self.ui.DifferenceTable.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        

    def setup_playlists(self):
        with open(os.path.realpath(os.path.dirname(__file__)) + "/playlists.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                name  = line.split(",")[0].strip()
                id = line.split(",")[1].strip()
                print(name, id)
                path = os.path.realpath(os.path.dirname(__file__)) + "/data/playlistDifferences/" + id + ".csv"
                if os.path.isfile(path):
                    difference_data = pd.read_csv(path, encoding='utf-8', sep=",")
                else:   
                    difference_data = pd.DataFrame({"VideoName": [], "ChannelName": [] , "Reason": [], "Time": [], "Replaced": [], "Position": [], "VideoId": []})
                self.playlists.append(Playlists(id, name, difference_data))
                self.ui.PlaylistBox.insertItem(len(self.playlists),name)

    def run_difference_check(self):
        playlist_index = self.ui.PlaylistBox.currentIndex()
        playlist_id = self.playlists[playlist_index].id

        playlist_content = []
        response = retrieveData(playlist_id, self.youtube)
        playlist_content.append(response)
        while 'nextPageToken' in response:
            newPageToken = response['nextPageToken']
            response = retrieveData(playlist_id, self.youtube, newPageToken)
            playlist_content.append(response)

        to_file(playlist_content, playlist_id)
    
        self.playlists[playlist_index].difference_data = compare(playlist_id, self.playlists[playlist_index].difference_data)

        self.generate_table()

        print("Done")


    def setup_api(self):
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = os.path.realpath(os.path.dirname(__file__)) + "/secrets/client_secret.json"
        scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

        # Get credentials and create an API client
        credential_path = os.path.join(os.path.realpath(os.path.dirname(__file__)) + "/secrets", 'credential_sample.json')
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(client_secrets_file, scopes)
            
            flags= argparser.parse_args(args=[])
            
            credentials = tools.run_flow(flow, store, flags)

        youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
        
        return youtube

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = PlaylistChecker()
    widget.show()
    sys.exit(app.exec())
