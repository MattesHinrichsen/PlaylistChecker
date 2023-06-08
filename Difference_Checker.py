import pandas as pd
from datetime import datetime
import os
import requests

def to_file(res, playlist_id):
    title = []
    videoId = []
    channel = []
    status = []
    playlistItem_id = []


    for i in res:
        for j in range(len(i["items"])):
            title.append(i["items"][j]["snippet"]["title"].replace(',', ''))
            videoId.append(i["items"][j]["snippet"]["resourceId"]["videoId"].replace(',', ''))

            playlistItem_id.append(i["items"][j]["id"])

            if ("videoOwnerChannelTitle" in i["items"][j]["snippet"]):
                channel.append(i["items"][j]["snippet"]["videoOwnerChannelTitle"].strip(" - Topic").replace(',', ''))
            else:
                channel.append("Deleted")

            status.append(i["items"][j]["status"]["privacyStatus"].replace(',', ''))

    data = {"Title": title, "Channel": channel, "VideoId": videoId, "Status": status, "Position": [i+1 for i in range(len(title))], "PlaylistItemId": playlistItem_id}
    dataframe_new = pd.DataFrame(data=data)
    
    dataframe_new.to_csv(os.path.realpath(os.path.dirname(__file__)) + "/data/playlistContent/{}_new.csv".format(playlist_id), encoding='utf-8', sep=",", index=False)




def retrieveData(playlist_id, youtube, pageT = None):
    request = youtube.playlistItems().list(
        part="snippet, status",
        maxResults=50,
        playlistId= playlist_id,
        pageToken= pageT,
        fields="nextPageToken ,items(id, snippet(title,videoOwnerChannelTitle, resourceId/videoId), status/privacyStatus)"
    )
    response = request.execute()
    return response



def compare(playlist_id, current_dataframe):
    path = os.path.realpath(os.path.dirname(__file__)) + "/data/"
    time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    if os.path.exists(path + "playlistContent/{}_old.csv".format(playlist_id)):
        found_difference = False
        old = pd.read_csv(path + "playlistContent/{}_old.csv".format(playlist_id), encoding='utf-8', sep=",")
        new = pd.read_csv(path + "playlistContent/{}_new.csv".format(playlist_id), encoding='utf-8', sep=",")
        new_Id_list = list(new.VideoId)
        old_Id_list = list(old.VideoId)

        change_list= []

        for i in range(len(old.VideoId)):

            if old_Id_list[i] in new_Id_list:
                new_index = new_Id_list.index(old_Id_list[i])
                if old.Status[i] != new.Status[new_index]:
                    
                    if new.Status[new_index] == "private":
                            found_difference = True
                            change_list.append({"VideoName": old.Title[i], "ChannelName": old.Channel[i] , "Reason": "Privated", "Time": time, "Replaced": False, "Position": new.Position[new_index], "VideoId": old.VideoId[i], "PlaylistItemId": new.PlaylistItemId[new_index]})
                    
                    elif new.Status[new_index] == "privacyStatusUnspecified":
                        found_difference = True
                        change_list.append({"VideoName": old.Title[i], "ChannelName": old.Channel[i] , "Reason": "Deleted", "Time": time, "Replaced": False, "Position": new.Position[new_index], "VideoId": old.VideoId[i], "PlaylistItemId": new.PlaylistItemId[new_index]})
                    
            elif old_Id_list[i] not in current_dataframe["VideoId"].tolist():
               #Not in playlist anymore
               found_difference = True
               change_list.append({"VideoName": old.Title[i], "ChannelName": old.Channel[i] , "Reason": "No longer in playlist", "Time": time, "Replaced": False, "Position": old.Position[i], "VideoId": old.VideoId[i], "PlaylistItemId": None})

        if found_difference:
            change_dataframe = pd.DataFrame(change_list)

            current_dataframe = current_dataframe.append(change_dataframe, ignore_index=True)

            print("\nA difference was found in playlist: {}\n".format(playlist_id))


    else:
        print("No old data to compare to for this playlist! It has now been created. Run again for normal use.\n")

    try:
        os.remove(path + "playlistContent/{}_old.csv".format(playlist_id))
    except:
        pass
    os.rename(path + "playlistContent/{}_new.csv".format(playlist_id), path + "playlistContent/{}_old.csv".format(playlist_id))

    return current_dataframe
