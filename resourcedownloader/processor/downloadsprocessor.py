# import  sys
# print(sys.path)
from queue import Queue
from threading import  Thread
from resourcedownloader.processor.downloadworker import  DownloadWorker
import  os
import  time
from tqdm import  tqdm


def Resource:
    def __init__(self, resourceurl):
        self.resourceurl = resourceurl
        self.




class DownloadsProcessor(object):

    def __init__(self, resourceurlslist, path_download_dir):
        self._resourceurls = resourceurlslist
        self._path_download_dir = os.path.join(path_download_dir)
        for resource in self._resourceurls:
                self.job_queue.put((resource, self._path_download_dir))


        self.job_queue = Queue()
        self._threadsize = 2

        self.runnning = []
        self.started_downloads =[]
        self.completed_downloads = []

        self._progressalljobs = 0


    def ResolveProtocol(self):
        pass

    def monitor_progress(self):
        """Monitors the progress of Resources waiting download in queue"""
        try:
            while True:
                #print(len(self.runnning_threads))
                for download in self.started_downloads:
                    print(download)
                    if download.download_processor:
                        #print(download.download_processor.get_download_progress())
                        downloader = download.download_processor
                        if downloader.downloadprogress is None:

                            description, downloaded, totalsize = downloader.downloadprocessor.get_download_progress()
                            downloadsize = downloader.download_processor._chunksize
                            downloadunit = downloader.download_processor._chunkunit
                            download_progress = tqdm(desc=description, total=totalsize, unit_divisor=downloadsize,
                                                          unit_scale=True, unit=downloadunit)
                        curradvance = downloaded - self.download_progress.n
                        download_progress.update(curradvance)

                #for worker in self.runnning_threads:
                #    print(worker.download_processor)
                    #if worker.download_processor:
                    #    print(worker.get_download_progress())
                        # downloadprocessor = worker.download_processor
                        # description, downloaded, total, percentage = downloadprocessor.get_download_progress()
                        # progresspercentage = 0
                        # if total>0:
                        #     progresspercentage = float(downloaded/total)
                        # print(description,  '% complete')
                        #time.sleep(1)


            #Check if some failed filed need removal
            print(" Completed Downloading Resources")
        except:
            pass

    def process_resources(self):
        """Processes the Resources that need to be downloaded"""
        try:

            progress_monitor = Thread(target=self.monitor_progress)
            progress_monitor.start()

            for i in range(self._threadsize):
                workerprocess = DownloadWorker(self.job_queue, self.started_downloads, self.completed_downloads)
                #self.runnning.append(workerprocess)
                workerprocess.start()


            self.job_queue.join()
            progress_monitor.join()
            # Check if some failed files need removal
        except:
            print(" Some Exception Occured")
            # Check if some failed filed need removal




        # for url in self._resourceurls:
        #     downloadertype= DownloadProtocolFactory.get_protocol(url)
        #     downloader = downloadertype(url, self._path_download_dir)
            #downloader.download_resource()


