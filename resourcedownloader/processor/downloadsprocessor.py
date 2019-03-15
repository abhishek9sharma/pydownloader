# import  sys
# print(sys.path)
from queue import Queue
from threading import  Thread
from resourcedownloader.processor.downloadworker import  DownloadWorker
import  os

class DownloadsProcessor(object):

    def __init__(self, resourceurlslist, path_download_dir):
        self._resourceurls = resourceurlslist
        self._path_download_dir = os.path.join(path_download_dir)
        self._threadsize = 2
        self.work_queue = Queue()

    def process_resources(self):
        try:
            for resource in self._resourceurls:
                self.work_queue.put((resource, self._path_download_dir))

            for i in range(self._threadsize):
                workerprocess = DownloadWorker(self.work_queue)
                workerprocess.start()

            self.work_queue.join()
        except:
            pass


        # for url in self._resourceurls:
        #     downloadertype= DownloadProtocolFactory.get_protocol(url)
        #     downloader = downloadertype(url, self._path_download_dir)
            #downloader.download_resource()


