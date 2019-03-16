from threading import  Thread
from queue import  Queue,Empty
from  resourcedownloader.downloadservice.download_factory import DownloadProtocolFactory

class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
         while True:
             try:
                 resourceurl, downloaddir = self.queue.get_nowait()
                 protocol_downloader = self.get_downloader(resourceurl)
                 if protocol_downloader:
                     download_processor = protocol_downloader(resourceurl, downloaddir)
                     print('Starting download for url ', resourceurl)
                     download_processor.download_resource()
                 else:
                     pass
                 print('Finished download for url ', resourceurl)

                 self.queue.task_done()
             except Empty:
                break



    def get_downloader(self, resourceurl):
         try:
             return DownloadProtocolFactory.get_protocol(resourceurl)
         except:
             return None
