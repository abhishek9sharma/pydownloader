# import  sys
# print(sys.path)
from queue import Queue,Empty
from threading import  Thread
from resourcedownloader.processor.downloadprocessor import  DownloadProcessor
from resourcedownloader.processor.resource import Resource
import  os
import  time
from tqdm import  tqdm


class DownloadsProcessor(object):

    def __init__(self, resourceurlslist, path_download_dir):
        self._resourceurls = resourceurlslist
        self._path_download_dir = os.path.join(path_download_dir)

        self.jobqueue = Queue()
        self.resultqueue = Queue()
        self.results = {'Failed' : [] ,'Completed': []}
        self.resources = {}

        self.runnningdownloads = []
        self.mainprocessprogress = None

        for idx,resourceurl in enumerate(self._resourceurls):
            resourceobj = Resource(idx, resourceurl)
            if resourceobj.protocolresolved:
                statusvalue = "Resolved Protocol Ready for Download"
                self.jobqueue.put(idx)
                resourceobj.set_status(statusvalue)    
            else:
                statusvalue = "Failed : Undefined Protocol"
                self.resultqueue.put((idx, statusvalue))
                self.results['Failed'].append(idx)

                resourceobj.set_status(statusvalue)           
            self.resources[idx] = resourceobj      
         
        self._threadsize = 2


    def monitor_progress(self):
        """Monitors the progress of Resources waiting download in queue"""
        try:
            while True:
                if self.jobqueue.unfinished_tasks == 0:
                    # Add Code to remove dirty files
                    break

                #Track Main Processor
                # if self.mainprocessprogress is None:
                #     desc = " Total Progress over all jobs "
                #     self.mainprocessprogress = tqdm(desc=desc, total=len(self.resources), unit_scale=True, disable= False)
                #
                # progress = len(self.resources) - self.jobqueue.unfinished_tasks
                # #progress = len(self.resultqueue)
                # self.mainprocessprogress.update(progress)

                for k,resourceobj in self.resources.items():
                      resourceobj.plot_progress()


                time.sleep(1)
            #Check if some failed filed need removal
            print(" Completed Downloading Resources")
        except:
            pass
            # Add Code to remove dirty files

    def process_resources(self):
        try:
            progress_monitor = Thread(target=self.monitor_progress)
            progress_monitor.start()

            
            for threadidx in range(self._threadsize):
                jobprocessor = DownloadProcessor(self.jobqueue, self.resultqueue, self.resources, self._path_download_dir,self.runnningdownloads, self.results)
                #jobprocessor = Thread(target= self.worker)
                jobprocessor.start()

            self.jobqueue.join()

            #while len(self.runnningdownloads)>0:
            #    pass
            progress_monitor.join()
        except:
            pass
            # Add Code to remove dirty files


