import os
from pytube import YouTube
import time
from urllib.parse import urlsplit, parse_qs
import requests
from services_section import AllYouNeed


class Download:
    # clone the channel id or name or any details you need

    @classmethod
    def testLink(cls, link):
        try:
            # Attempt to create a pytube YouTube object from the link
            video = YouTube(link)

            # Check if the video details could be obtained
            if not video.title:
                raise Exception("Video details could not be obtained.\n\n")

            # Check if the video is available
            response = requests.get(link)
            if response.status_code != 200:
                raise Exception("Video is not available.\n\n")

            return "Link is valid and exists."

        except Exception as e:
            return "Link is not valid or does not exist:\n\n", e

    @classmethod
    def channelInfo(cls, choose, url):
        try:
            video = YouTube(url)
        except Exception as e:
            return "Error: Invalid URL"

        if choose == "id":
            return video.channel_id
        if choose == "url":
            return video.channel_url
        if choose == "name":
            return video.author
        else:
            return "Error: Invalid choice, choose either 'id', 'url', or 'name'"

    @classmethod
    def download_me(cls, downloadType, url, path, video_title):
        start_time = time.time()
        # video path
        videoPath = os.path.join(path, AllYouNeed.make_clean(video_title))
        # scrapping
        try:
            yt = YouTube(url)
        except Exception as e:
            print(f"Error occured while scraping video: {e}")
            return

        if downloadType == 'mp4':
            if not (os.path.exists(videoPath + '.mp4')):
                # download allYouNeedtion
                # video = yt.streams.filter(mime_type='video/mp4', res='720p').first()
                try:
                    video = yt.streams.filter(mime_type='video/mp4').first()
                    video.download(output_path=path, filename=video_title + ".mp4")
                except Exception as e:
                    print(f"Error occured while downloading mp4: {e}")
                    return
            else:
                print(f"{video_title}.mp4 already exists, skipping download.")

        elif downloadType == 'mp4_hd':
            if not (os.path.exists(videoPath + 'hd.mp4')):
                # download allYouNeedtion
                try:
                    video = yt.streams.filter(mime_type='video/mp4', res='720p').first()
                    # video = yt.streams.filter(mime_type='video/mp4').first()
                    video.download(output_path=path, filename=video_title + "hd.mp4")
                except Exception as e:
                    print(f"Error occured while downloading hd mp4: {e}")
                    return
            else:
                print(f"{video_title}hd.mp4 already exists, skipping download.")

        elif downloadType == 'mp3':
            if not (os.path.exists(videoPath + '.mp3')):
                # download allYouNeedtion
                try:
                    audio = yt.streams.filter(only_audio=True).first()
                    audio.download(output_path=path, filename=video_title + ".mp3")
                except Exception as e:
                    print(f"Error occured while downloading mp3: {e}")
                    return
            else:
                print(f"{video_title}.mp3 already exists, skipping download.")
        else:
            return "error"
        end_time = time.time()
        processing_time = end_time - start_time
        print("download time: ", processing_time)

    @classmethod
    # download all playlist
    def downloadOne(cls, channelpath, url, downloadType):

        # scrapping
        try:
            yt = YouTube(url)
        except Exception as e:
            return "Error: Invalid URL"
        video_title = yt.title
        # download video
        try:
            cls.download_me(downloadType, url, channelpath, video_title)
        except Exception as e:
            print(f"Error occured while downloading verify your url: {e}")

    @classmethod
    def onePlaylist(cls, youtube, channelpath, url, downloadType, api_key):

        # scraping
        try:
            yt = YouTube(url)
        except Exception as e:
            return "Error: Invalid URL"

        try:
            # get playlist id from url video
            query = urlsplit(url).query
            params = parse_qs(query)
            playlist_id = params['list'][0]

            # all of that for playlist title
            url2 = f'https://www.googleapis.com/youtube/v3/playlists?part=snippet&id={playlist_id}&key={api_key}'
            response = requests.get(url2)
            data = response.json()
            playlist_title = data['items'][0]['snippet']['title']
            print(playlist_title)
        except:
            playlist_title = "My Mix"

        # create Playlist path
        playlistPath = AllYouNeed.create_path(channelpath, playlist_title)

        nb = 0
        next_page_token = None
        while True:
            videos_response = youtube.playlistItems().list(
                part='contentDetails',
                maxResults=50,
                playlistId=playlist_id,
                pageToken=next_page_token
            ).execute()

            for video in videos_response['items']:
                video_id = video["contentDetails"]["videoId"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                if 'snippet' in video and 'contentDetails' in video:
                    video_title = video["snippet"]["title"]

                else:
                    try:
                        video_response = youtube.videos().list(
                            part='snippet',
                            id=video_id
                        ).execute()
                        video_title = video_response['items'][0]['snippet']['title']
                    except IndexError:
                        video_title = nb

                try:
                    cls.download_me(downloadType, video_url, playlistPath, AllYouNeed.make_clean(video_title))
                except:
                    pass

                nb = nb + 1
            if 'nextPageToken' in videos_response:
                next_page_token = videos_response['nextPageToken']
            else:
                break
        print(nb)

    @classmethod
    # download all playlist
    def allChannel(cls, youtube, channelpath, url, downloadType):

        # creat All channel path in Youdowpath
        allChannelPath = AllYouNeed.create_path(channelpath, "AllChannel")

        # Get the channel's uploads playlist ID
        channel_uploads_playlist_id = youtube.channels().list(
            part="contentDetails",
            id=cls.channelInfo("id", url)
        ).execute()["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        # Retrieve all videos in the uploads playlist
        videos = []
        next_page_token = None
        while True:
            playlist_items_response = youtube.playlistItems().list(
                part="snippet",
                maxResults=50,
                playlistId=channel_uploads_playlist_id,
                pageToken=next_page_token
            ).execute()
            videos += playlist_items_response["items"]
            next_page_token = playlist_items_response.get("nextPageToken")
            if next_page_token is None:
                break

        nb = 0
        # Print the video links
        for video in videos:
            nb += 1
            video_id = video["snippet"]["resourceId"]["videoId"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_title = video["snippet"]["title"]
            # print(video_url)
            try:
                cls.download_me(downloadType, video_url, allChannelPath, AllYouNeed.make_clean(video_title))
            except:
                pass

        print(nb)

    @classmethod
    # download one video or mp3
    def AllPlaylists(cls, youtube, channelpath, url, downloadType):

        channelId = cls.channelInfo("id", url)

        # Get all playlists from the channel
        playlists = youtube.playlists().list(
            part="snippet",
            channelId=channelId,
            maxResults=200
        ).execute()
        nb_pl = 0

        # creat file for every playlist
        for playlist in playlists["items"]:
            playlist_id = playlist["id"]
            playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
            # print(playlist_url)
            playlist_title = playlist["snippet"]["title"]

            # creat Playlis path
            playlistPath = AllYouNeed.create_path(channelpath, playlist_title)

            next_page_token = None
            while True:
                # sleep time request
                # time.sleep(2)
                videos_response = youtube.playlistItems().list(
                    part='contentDetails',
                    maxResults=50,
                    playlistId=playlist_id,
                    pageToken=next_page_token
                ).execute()
                nb = 0
                nb_pl += 1
                print("\nplaylist : ", nb_pl)
                for video in videos_response['items']:
                    try:
                        # sleep time request
                        # time.sleep(2)
                        video_id = video["contentDetails"]["videoId"]
                        video_url = f"https://www.youtube.com/watch?v={video_id}"
                        if 'snippet' in video and 'contentDetails' in video:
                            video_title = video["snippet"]["title"]

                        else:
                            video_response = youtube.videos().list(
                                part='snippet',
                                id=video_id
                            ).execute()
                            video_title = video_response['items'][0]['snippet']['title']

                        # download video or mp3
                        cls.download_me(downloadType, video_url, playlistPath, AllYouNeed.make_clean(video_title))
                    except:
                        pass
                    # videopath=create_path(playlistPath,video_id)

                    nb += 1
                if 'nextPageToken' in videos_response:
                    next_page_token = videos_response['nextPageToken']
                else:
                    break
                print(nb)
