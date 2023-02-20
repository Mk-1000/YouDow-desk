from download_section import Download
from apis_section import YoutubeAPI
from services_section import AllYouNeed


class select_mode:
    @classmethod
    def testUrl(cls, url):
        return Download.testLink(url)

    @classmethod
    def youDowPath(cls, userhome):
        youDowPath = AllYouNeed.youDowPath(userhome)
        return youDowPath

    @classmethod
    def youDowPath(cls):
        youDowPath = AllYouNeed.youDowPath()
        return youDowPath

    @staticmethod
    def channel_path(youDowPath, url):

        channel_title = Download.channelInfo("name", url)
        # creat channel path
        if channel_title == "Error Invalid URL":
            return channel_title
        else:
            channelPAth = AllYouNeed.create_path(youDowPath, channel_title)
            return channelPAth

    @classmethod
    def youDow(cls, channelPAth, url, case, download_type):

        # Create a service object
        youtube_api = YoutubeAPI()
        youtube = youtube_api.get_service()

        if case == 1:
            Download.downloadOne(channelPAth, url, download_type)
        elif case == 2:
            Download.onePlaylist(youtube, channelPAth, url, download_type, youtube_api.get_api_key())
        elif case == 3:
            Download.allChannel(youtube, channelPAth, url, download_type)
        elif case == 4:
            Download.AllPlaylists(youtube, channelPAth, url, download_type)
