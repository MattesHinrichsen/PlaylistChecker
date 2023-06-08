# PlaylistChecker
Tool to automatically check for privated or deleted songs in large Youtube Music playlists. 

## Setup
1. Add all the playlist you want to track to the playlists.txt file. The format it should be added in is \
``` <desired name>, <playlist id> ```. \
Each line represents a new playlist.
2. Setup new credentials for the Youtube-API at console.cloud.google.com/apis/credentials by selecting \
  ``` Create Credentials ``` -> ``` OAuth client ID ```. Then selecting ``` Desktop App ``` and choosing a name.
3. Create the file secrets/client_secret.json.
4. Fill the file with the content of the downloadable json.

## Running
1. Open and run PlaylistChecker.py
2. The first time (and then periodically after when the key expires) a browser window will open. Select the google account the OAuth client ID was set up with and follow the further instructions.
3. A GUI will open where you can select from all playlists.
4. The first time the Difference Check is run it will only take account of the playlist content. From then on every time it is run it will detect any changes to the playlist and display them.
