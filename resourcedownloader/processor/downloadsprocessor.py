# import  sys
# print(sys.path)
from  resourcedownloader.downloadservice.download_factory import DownloadProtocolFactory
class DownloadsProcessor(object):

    def __init__(self, resourceurislist, path_download_dir):
        self._resourceuris = resourceurislist
        self._path_download_dir = path_download_dir

    def process_resources(self):
        for uri in self._resourceuris:
            determinehandler = DownloadProtocolFactory.get_protocol(uri)
            print(determinehandler)
            



