from decouple import config
import json


class listItem:
    def __init__(self, youtube):
        self.youtube = youtube
        self.channelId = config('channelId')

    def showItem(self, playListId):
        request = self.youtube.playlistItems().list(
            part="snippet",
            maxResults=250,
            playlistId=playListId,
        )
        response = request.execute()

        resObj = dict()

        for list in response["items"]:
            resObj[list["snippet"]["title"]] = list["snippet"]["resourceId"]["videoId"]

        self.listItens = resObj
        return resObj

    def addItem(self, playListId,vidioId):
        request = self.youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "channelId": self.channelId,
                    "description": "",
                    "playlistId": playListId,
                    "position": 0,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": vidioId,
                    },
                }
            }
        )
        response = request.execute()

    def delItemByName(self, playListId, vidioName):
        request = self.youtube.playlistItems().list(
            part="snippet",
            maxResults=250,
            playlistId=playListId,
        )
        response = request.execute()
        notFound = True
        for item in response["items"]:
            if(vidioName == item["snippet"]["title"]):
                notFound = False
                targetId = item["id"]

        if(notFound):
            return False

        request = self.youtube.playlistItems().delete(
            id = targetId,
        )
        response = request.execute()

    def delItemByVidioId(self, playListId, vidioId):
        request = self.youtube.playlistItems().list(
            part="snippet",
            maxResults=250,
            playlistId=playListId,
        )
        response = request.execute()
        notFound = True
        for item in response["items"]:
            if(vidioId == item["snippet"]["resourceId"]["videoId"]):
                notFound = False
                targetId = item["id"]

        if(notFound):
            return False

        request = self.youtube.playlistItems().delete(
            id = targetId,
        )
        response = request.execute()

    def searchItem(self, playListId, keyword):
        request = self.youtube.playlistItems().list(
            part="snippet",
            maxResults=250,
            playlistId=playListId,
        )
        response = request.execute()

        resObj = dict()

        for list in response["items"]:
            cmpTitle = list["snippet"]["title"].lower()
            cmpTitle = cmpTitle.replace(" ", "")
            if(keyword in cmpTitle):
                resObj[list["snippet"]["title"]] = list["snippet"]["resourceId"]["videoId"]

        self.listItens = resObj
        return resObj
