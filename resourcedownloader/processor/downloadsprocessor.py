# import  sys
# print(sys.path)
from queue import Queue
from threading import  Thread
from resourcedownloader.processor.downloadworker import  DownloadWorker
import  os
import  time

class DownloadsProcessor(object):

    def __init__(self, resourceurlslist, path_download_dir):
        self._resourceurls = resourceurlslist
        self._orgjobs = len(self._resourceurls)
        self._path_download_dir = os.path.join(path_download_dir)
        self._progress = 0
        self._threadsize = 2
        self.work_queue = Queue()
        for resource in self._resourceurls:
                self.work_queue.put((resource, self._path_download_dir))


    def monitor_progress(self):
        """Monitors the progress of Resources waiting download in queue"""
        try:
            while(True):
                jobs_pending = self.work_queue.unfinished_tasks
                #jobs_pending = 3
                if jobs_pending ==0:
                    #remove partial files if any
                    break
                #print(self._orgjobs - jobs_pending, " jobs processed")
                #print(jobs_pending, " jobs left")
                time.sleep(2)

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
                workerprocess = DownloadWorker(self.work_queue)
                workerprocess.start()

            self.work_queue.join()
            progress_monitor.join()
            # Check if some failed files need removal
        except:
            print(" Some Exception Occured")
            # Check if some failed filed need removal




        # for url in self._resourceurls:
        #     downloadertype= DownloadProtocolFactory.get_protocol(url)
        #     downloader = downloadertype(url, self._path_download_dir)
            #downloader.download_resource()


