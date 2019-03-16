from threading import  Thread
from queue import  Queue,Empty
from  resourcedownloader.downloadservice.download_factory import DownloadProtocolFactory
from tqdm import  tqdm

class DownloadWorker(Thread):
    def __init__(self, queue, started_downloads, completed_downloads):
        Thread.__init__(self)
        self.queue = queue
        self.download_progress = None
        self.started_downloads = started_downloads
        self.completed_downloads = completed_downloads
        self.download_processor = None

    def run(self):
         while True:
             try:
                 resourceurl, downloaddir = self.queue.get_nowait()
                 #print('thread for url', resourceurl)
                 protocol_downloader = self.get_downloader(resourceurl)
                 if protocol_downloader:
                     self.download_processor = protocol_downloader(resourceurl, downloaddir)
                     self.started_downloads.append(self.download_processor)
                     self.download_processor.download_resource()
                 else:
                     pass
                     #add to finished status with a failed status
                 self.completed_downloads.append(self.download_processor)
                 self.queue.task_done()
             except Empty:
                break

    # #
    # # def get_progress(self):
    # #     if self.download_processor:
    # #         if self.downloadprogress is None:
    # #             description, downloaded, totalsize = self.downloadprocessor.get_download_progress()
    # #             downloadsize = self.download_processor._chunksize
    # #             downloadunit = self.download_processor._chunkunit
    # #             self.download_progress = tqdm(desc= description, total = totalsize, unit_divisor= downloadsize , unit_scale= True, unit =downloadunit)
    # #         curradvance = downloaded -self.download_progress.n
    #         self.download_progress.update(curradvance)



    def get_downloader(self, resourceurl):
         try:
             return DownloadProtocolFactory.get_protocol(resourceurl)
         except:
             return None

