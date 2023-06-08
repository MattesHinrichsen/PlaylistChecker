import os
from pathlib import Path
import sys
import pandas as pd

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QComboBox, QTableView, QMainWindow, QMenu, QDialog
from PySide6.QtCore import QFile, QAbstractTableModel, Qt, QEvent, QPointF
from PySide6.QtUiTools import QUiLoader



class ReplaceMenu(QDialog):
    def __init__(self, data, youtube, playlist_id) -> None:
        super().__init__()
        self.setWindowTitle("Replace Menu")
        
        self.data = data
        self.youtube = youtube
        self.playlist_id = playlist_id

        self.ui = self.load_ui()

        self.ui.checkBox.stateChanged.connect(self.toggle_pos)
        self.ui.buttonBox.accepted.connect(self.run_replacement)
        self.ui.buttonBox.rejected.connect(self.close)

    
    def toggle_pos(self):
        if self.ui.checkBox.isChecked():
            self.ui.posEdit.setEnabled(True)
        else:
            self.ui.posEdit.setEnabled(False)


    def run_replacement(self):
        new_video_id = self.ui.IDEdit.text().strip()
        if "youtu" in new_video_id:
            new_video_id = new_video_id.split("v=")[1].split("&")[0]
        if self.ui.checkBox.isChecked():
            position = int(self.ui.posEdit.text().strip()) - 1
        else: 
            position = int(self.data['Position'].iloc[0]) - 1
        
        #Delete old video
        if self.data['PlaylistItemId'].iloc[0] is not None:
            try:
                request = self.youtube.playlistItems().delete(
                    id=self.data['PlaylistItemId'].iloc[0]
                )
                request.execute()
            except Exception as e:
                print("Deletion failed due to: " + str(e))
            
        resource_Id = None
        #Inserting new video
        try:
            request = self.youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": self.playlist_id,
                        "position": 0,
                        "resourceId": {
                        "kind": "youtube#video",
                        "videoId": new_video_id
                        }
                    }
                }
            )
            response = request.execute()
            resource_Id = response['id']
        except Exception as e:
            print("Insertion failed due to: " + str(e))
            self.close()
               
        #Updating position of new video
        if resource_Id is not None:
            try:
                request = self.youtube.playlistItems().update(
                    part="snippet",
                    body={
                        "id": resource_Id,
                        "snippet": {
                            "playlistId": self.playlist_id,
                            "position": position,
                            "resourceId": {
                            "kind": "youtube#video",
                            "videoId": new_video_id
                            }
                        }
                    }
                )
                response = request.execute()
            except Exception as e:
                print("Updating failed due to: " + str(e))
        else:
            print("You got a problem")

        self.done(1)

    def load_ui(self):
        loader = QUiLoader()
        path = Path(__file__).resolve().parent / "ReplaceMenu.ui"
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file, self)
        ui_file.close()
        return ui
