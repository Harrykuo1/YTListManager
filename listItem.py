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
        print("共有"+str(len(response["items"]))+"個影片")
        index = 1
        for list in response["items"]:
            print(str(index)+". "+list["snippet"]["title"])
            index+=1
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
        arr = []
        for list in response["items"]:
            cmpTitle = list["snippet"]["title"].lower()
            cmpTitle = cmpTitle.replace(" ", "")
            keyword = keyword.lower()
            keyword = keyword.replace(" ", "")

            if(keyword in cmpTitle):
                """print("@@"+keyword)
                print("##"+cmpTitle)"""
                arr.append(list["snippet"]["title"])
                resObj[list["snippet"]["title"]] = list["snippet"]["resourceId"]["videoId"]

        print("共有"+str(len(arr))+"個影片")
        index = 1
        for i in arr:
            print(str(index)+". "+i)
            index+=1
            
        self.listItens = resObj
        return resObj

    def changeOrder(self, playListId, targetName, targetOrder):
        request = self.youtube.playlistItems().list(
            part = "snippet",
            playlistId = playListId,
        )
        response = request.execute()

        for item in response["items"]:
            if(targetName == item["snippet"]["title"]):
                targetId = item["id"]
                vidioId = item["snippet"]["resourceId"]["videoId"]

        request = self.youtube.playlistItems().update(
            part="snippet",
            body={
            "id": targetId,
            "snippet": {
                "playlistId": playListId,
                "position": targetOrder,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": vidioId,
                }
            }
            }
        )
        response = request.execute()




        
