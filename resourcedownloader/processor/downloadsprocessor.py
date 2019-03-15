# import  sys
# print(sys.path)
from  resourcedownloader.downloadservice.download_factory import DownloadProtocolFactory

class DownloadsProcessor(object):

    def __init__(self, resourceurlslist, path_download_dir):
        self._resourceurls = resourceurlslist
        self._path_download_dir = path_download_dir

    def process_resources(self):
        for url in self._resourceurls:
            downloadertype= DownloadProtocolFactory.get_protocol(url)
            downloader = downloadertype(url, self._path_download_dir)
            downloader.download_resource()


