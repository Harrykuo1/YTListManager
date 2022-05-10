import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from decouple import config
from playList import playList
from listItem import listItem
import re
import urllib.parse
from pytube import extract

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def youtubeParser(url):
    regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')

    match = regex.match(url)

    if not match:
        return('no match')
    return (match.group('id'))

def youtube_parser(url):
    """try:
        query = urllib.parse.urlparse(url)
        if query.hostname == 'youtu.be':
            return query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch':
                p = urllib.parse.parse_qs(query.query)
                return p['v'][0]
            if query.path[:7] == '/embed/':
                return query.path.split('/')[2]
            if query.path[:3] == '/v/':
                return query.path.split('/')[2]
    except:
        pass
    return False"""
    id = extract.video_id(url)
    return id


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret_key.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    auth_url, _ = flow.authorization_url(prompt='consent')

    credentials = flow.run_console()

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials
    )

    myPlayList = playList(youtube)
    myListItem = listItem(youtube)

    mode = ''

    while(mode != 'close'):
        print()
        mode = input("輸入功能：")
        mode = mode.replace(' ', '')

        if(mode == 'help'):
            with open('help.txt', 'r') as helpFile:
                print(helpFile.read())
                print()

        elif(mode == 'showList'):
            resObj = myPlayList.showList()
            print("共有%d個播放清單" % len(resObj))
            i = 1
            for resKey, resValue in resObj.items():
                print(i, resKey, resValue)
                i += 1

        elif(mode == 'addList'):
            title = input("請輸入新增播放清單名稱：")
            myPlayList.addList(title)
            print("新增播放清單%s成功" % title)

        elif(mode == 'delList'):
            title = input("請輸入欲刪除播放清單名稱：")
            if(title in myPlayList.playLists):
                myPlayList.delList(title)
                print("刪除播放清單%s成功" % title)
            else:
                print("刪除失敗，播放清單%s不存在" % title)

        elif(mode == 'showItem'):
            title = input("請輸入欲列出的播放清單成員：")
            if(title in myPlayList.playLists):
                playListId = myPlayList.playLists[title]
                resObj = myListItem.showItem(playListId)
                """print("共有%d個影片" % len(resObj))
                i = 1
                for resKey, resValue in resObj.items():
                    print(i, resKey, resValue)
                    i += 1"""
            else:
                print("列出失敗，播放清單%s不存在" % title)

        elif(mode == 'addItem'):
            vidioUrl = input("請輸入欲新增影片網址：")
            vidioId = youtube_parser(vidioUrl)
            if(vidioId == False):
                print("影片網址格式錯誤")
                continue
            targetList = input("請輸入儲存目標清單：")
            if(targetList in myPlayList.playLists):
                playListId = myPlayList.playLists[targetList]
                myListItem.addItem(playListId, vidioId)
                print("新增成功")
            else:
                print("列出失敗，播放清單%s不存在" % targetList)

        elif(mode == 'delItemByUrl'):
            targetList = input("請輸入欲刪除影片所在清單：")
            if(targetList in myPlayList.playLists):
                playListId = myPlayList.playLists[targetList]
            else:
                print("播放清單%s不存在" % targetList)
                continue

            vidioUrl = input("請輸入欲刪除影片網址：")
            vidioId = youtube_parser(vidioUrl)
            if(vidioId == False):
                print("影片網址格式錯誤")
                continue

            status = myListItem.delItemByVidioId(playListId, vidioId)
            if(status == False):
                print("查無此影片")
            else:
                print("刪除成功")

        elif(mode == 'delItemByName'):
            targetList = input("請輸入欲刪除影片所在清單：")
            if(targetList in myPlayList.playLists):
                playListId = myPlayList.playLists[targetList]
            else:
                print("播放清單%s不存在" % targetList)
                continue

            vidioName = input("請輸入欲刪除影片名稱：")
            status = myListItem.delItemByName(playListId, vidioName)
            if(status == False):
                print("查無此影片")
            else:
                print("刪除成功")

        elif(mode == 'searchItem'):
            targetList = input("請輸入欲查詢影片所在清單：")
            if(targetList in myPlayList.playLists):
                playListId = myPlayList.playLists[targetList]
            else:
                print("播放清單%s不存在" % targetList)
                continue
            keyword = input("請輸入關鍵字：")
            resObj = myListItem.searchItem(playListId, keyword)
            """print("共有%d個影片" % len(resObj))
            i = 1
            for resKey, resValue in resObj.items():
                print(i, resKey, resValue)
                i += 1"""

        elif(mode == 'changeOrder'):
            targetList = input("請輸入欲change影片所在清單：")
            targetName = input("input targetname")
            targetOrder = input("input targetOrder")
            if(targetList in myPlayList.playLists):
                playListId = myPlayList.playLists[targetList]
            else:
                print("播放清單%s不存在" % targetList)
                continue

            resObj = myListItem.changeOrder(playListId, targetName, targetOrder)
            print("Modify successful")

        elif(mode == "readFile"):
            txt = input("請輸入檔名")
            file = open(txt+".txt", 'r')
            while True:
                cmd =  file.readline()
                arr = cmd.split()
                if(arr[0] == 'end'):
                    break
                elif(arr[0] == 'add'):
                    targetList = arr[1]
                    vidioUrl = arr[2]
                    vidioId = youtube_parser(vidioUrl)
                    if(vidioId == False):
                        print("影片網址格式錯誤")
                        continue
                    if(targetList in myPlayList.playLists):
                        playListId = myPlayList.playLists[targetList]
                        myListItem.addItem(playListId, vidioId)
                        print("新增成功")
                    else:
                        print("列出失敗，播放清單%s不存在" % targetList)
                    
                elif(arr[0] == 'del'):
                    targetList = arr[1]
                    if(targetList in myPlayList.playLists):
                        playListId = myPlayList.playLists[targetList]
                    else:
                        print("播放清單%s不存在" % targetList)
                        continue

                    vidioUrl = arr[2]
                    vidioId = youtube_parser(vidioUrl)
                    if(vidioId == False):
                        print("影片網址格式錯誤")
                        continue

                    status = myListItem.delItemByVidioId(playListId, vidioId)
                    if(status == False):
                        print("查無此影片")
                    else:
                        print("刪除成功")
                elif(arr[0] == 'move'):
                    targetList = arr[2]
                    vidioUrl = arr[3]
                    vidioId = youtube_parser(vidioUrl)
                    if(vidioId == False):
                        print("影片網址格式錯誤")
                        continue
                    if(targetList in myPlayList.playLists):
                        playListId = myPlayList.playLists[targetList]
                        myListItem.addItem(playListId, vidioId)
                        #print("新增成功")
                    else:
                        print("列出失敗，播放清單%s不存在" % targetList)
                    #
                    targetList = arr[1]
                    if(targetList in myPlayList.playLists):
                        playListId = myPlayList.playLists[targetList]
                    else:
                        print("播放清單%s不存在" % targetList)
                        continue

                    vidioUrl = arr[3]
                    vidioId = youtube_parser(vidioUrl)
                    if(vidioId == False):
                        print("影片網址格式錯誤")
                        continue

                    status = myListItem.delItemByVidioId(playListId, vidioId)
                    if(status == False):
                        print("查無此影片")
                    else:
                        print("搬移成功")
                    
        else:
            print("無此功能")


if __name__ == "__main__":
    main()


# 4/1AX4XfWjHfSARjUVWdxE_hsKzyK4aykSZq09-nvNoKfud1EqdTgWkFV0tD1Y
