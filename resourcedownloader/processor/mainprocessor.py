# import  sys
# print(sys.path)
from queue import Queue,Empty
from threading import  Thread
from resourcedownloader.processor.downloadprocessor import  DownloadProcessor
from resourcedownloader.processor.resource import Resource
import  os
import  time
from tqdm import  tqdm


#TODO:     # comsoidation based on Q or List?
#TODO:     # Write a Log Somewhere
#TODO:     # deletes from downloader or forced from her
#TODO:     # errors for 0 inputs
#TODO:     # No of threads configurable
#TODO:     # Network error such as wifi Temp Dir and Cleanup a possible way
#TODO:     #Detailed Logging at each faiure
#TODO:     # Main Process tqdm bar


class DownloadsProcessor:

    def __init__(self, resourceurlslist, path_download_dir):
        self.resourceurls = resourceurlslist
        self.path_download_dir = os.path.join(path_download_dir)
        
        if len(self.resourceurls)==0:
            print( " No urls specified. Please provide resource links need to be downloade")
            return

        if self.path_download_dir=='' or self.path_download_dir is None:
            print( " Download directory is not specified or is invalid. Please check ")
            return

        self.jobqueue = Queue()
        self.resultqueue = Queue()
        self.results = {'Failed' : [] ,'Completed': [], 'Unresolved':[] }
        self.resources = {}

        self.runnningdownloads = []
        self.mainprocessprogress = None

        for idx,resourceurl in enumerate(self.resourceurls):
            resourceobj = Resource(idx, resourceurl)
            if resourceobj.protocolresolved:
                statusvalue = "Resolved Protocol Ready for Download"
                self.jobqueue.put(idx)
                resourceobj.set_status(statusvalue)    
            else:
                statusvalue = "Unresolved : Undefined Protocol"
                self.resultqueue.put((idx, statusvalue))
                self.results['Unresolved'].append(idx)
                resourceobj.set_status(statusvalue)
                           
            self.resources[idx] = resourceobj      
       
        self.threadsize = 2

    def delete_failed_downloads(self):
        #check if fetch from Queue thr resource idx
        for resourceidx in self.results['Failed']:
            resourceobj = self.resources[resourceidx]
            if 'Failed' in resourceobj.get_status():
                if resourceobj.downloadfilepath:
                    self.delete_failed_download(resourceobj)
        #decide how to delete resource/downloader/forcefully from here

    def delete_failed_download(self, resourceobj):
        if resourceobj.protocl_downloader:
            currdownloader = resourceobj.protocol_downloader
            if currdownloader:
                currdownloader.abort_download()
        try:
            if  os.path.exists(resourceobj.downloadfilepath):
                os.remove(resourceobj.downloadfilepath) 
        except:
            print (' Error occured while removiing file {0}', resourceobj.downloadfilepath)


    def monitor_progress(self):
        """Monitors the progress of Resources waiting download in queue"""
        try:
            while True:
                if self.jobqueue.unfinished_tasks == 0:
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
                    #check if failed downloads can be deleted from here

                time.sleep(1)
            self.delete_failed_downloads()
        except:
            self.delete_failed_downloads()





    def process_resources(self):
        try:
            #Start Monitor
            progress_monitor = Thread(target=self.monitor_progress)
            progress_monitor.start()

            # Start Downloads
            if self.threadsize>len(self.resourceurls):
                noofthreads = len(self.resourceurls)
            else:
                noofthreads = self.threadsize

            for threadidx in range(noofthreads):
                jobprocessor = DownloadProcessor(threadidx, self.jobqueue, self.resultqueue, self.resources, self.path_download_dir,self.runnningdownloads, self.results)
                jobprocessor.start()

            self.jobqueue.join()
            progress_monitor.join()
        except:
            pass
        finally:
            self.delete_failed_downloads()
            print(" Completed current iteration for Downloading Resources")


