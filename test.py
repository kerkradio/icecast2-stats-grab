""" Simple test """

from icecastparser import IcecastStatus

def test_sample_icecast():
    """ Test sample server """
    icecast_status = IcecastStatus('http://200.137.217.155:8010')

    for status in icecast_status.get_mountpoints():
        print("%s - Listeners: %s" % (status.mountpoint_url, status.current_listeners))

test_sample_icecast()
