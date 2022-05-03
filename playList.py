from decouple import config
import json


class playList:
    def __init__(self, youtube):
        self.youtube = youtube
        self.channelId = config('channelId')
        self.playLists = self.showList()

    def showList(self):
        request = self.youtube.playlists().list(
            part="snippet",
            channelId=self.channelId,
            maxResults = 300,
        )
        response = request.execute()
        resObj = dict()

        for list in response["items"]:
            resObj[list["snippet"]["title"]] = list["id"]

        self.playLists = resObj
        return resObj

    def addList(self, title):
        request = self.youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "channelId": self.channelId,
                    "title": title,
                    "description": "",
                    "channelTitle": "harry kuo",
                    "localized": {
                        "title": title,
                        "description": ""
                    }
                },
                "status": {
                    "privacyStatus": "public"
                }
            }
        )
        response = request.execute()

    def delList(self, title):
        request = self.youtube.playlists().delete(
            id = self.playLists[title]
        )
        response = request.execute()
