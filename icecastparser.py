""" Prints stats for icecast2 status page """
from collections import namedtuple
from bs4 import BeautifulSoup

Mountpoint = namedtuple('Mountpoint', ['mountpoint_url', \
    'stream_title', \
    'stream_description', \
    'content_type', \
    'mount_started', \
    'bitrate', \
    'current_listeners', \
    'peak_listeners', \
    'stream_genre', \
    'stream_url', \
    'current_song'])

class IcecastStatus():
    """ Single mountpoint status """
    icecast_url = ""

    def __init__(self, url):
        self.icecast_url = url

    def __repr__(self):
        return "IcecastStatus()"

    def __str__(self):
        return '\n'.join(["Mountpoint: %s" % (mountpoint.mountpoint_url) \
            for mountpoint in self.get_mountpoints()])

    def __get_html_from_url__(self):
        """ Returns HTML content for chosen URL """
        import urllib.request
        with urllib.request.urlopen(self.icecast_url) as response:
            html = response.read()
            return html

    def get_mountpoints(self):
        """ Returns mountpoints """
        html = self.__get_html_from_url__()

        soup = BeautifulSoup(html, 'html.parser')

        mountpoints = []

        for block in soup.findAll("div", {"class" : "newscontent"}):
            statusdata = block.find_all("td", {"class": "streamdata"})

            mountpoint = Mountpoint(mountpoint_url="%s%s" \
                    % (self.icecast_url, block.find('h3').get_text().split()[2]), \
                stream_title=statusdata[0].get_text(), \
                stream_description=statusdata[1].get_text(), \
                content_type=statusdata[2].get_text(), \
                mount_started=statusdata[3].get_text(), \
                bitrate=statusdata[4].get_text(), \
                current_listeners=int(statusdata[5].get_text()), \
                peak_listeners=int(statusdata[6].get_text()), \
                stream_genre=statusdata[7].get_text(), \
                stream_url=statusdata[8].get_text(), \
                current_song=statusdata[9].get_text())

            mountpoints.append(mountpoint)

        return mountpoints