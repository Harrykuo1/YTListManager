import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from decouple import config
from playList import playList

mode = ''

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

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
    myPlayList = playList()

    while(mode != 'close'):
        mode = input("輸入功能：")
        if(mode == 'help'):
            with open('help.txt', 'r') as helpFile:
                print(helpFile.read())
                print()

        elif(mode == 'showList'):
            request = showList(youtube)
        elif(mode == ''):
            pass
        elif(mode == ''):
            pass

    response = request.execute()

    print(response)


if __name__ == "__main__":
    main()


# 4/1AX4XfWjHfSARjUVWdxE_hsKzyK4aykSZq09-nvNoKfud1EqdTgWkFV0tD1Y


