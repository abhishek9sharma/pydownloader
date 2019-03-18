# import  sys
# print(sys.path)
from queue import Queue,Empty
from threading import  Thread
from resourcedownloader.processor.downloadprocessor import  DownloadProcessor
from resourcedownloader.processor.resource import Resource
import  os
import  errno
import  time
from tqdm import  tqdm


#TODO:     # Q used Needs to B Tested # Network error such as wifi Temp Dir and Cleanup a possible way
#TODO:     # Write a Log Somewhere
#TODO:     # errors for 0 inputs
#TODO:     # No of threads configurable
#TODO :     #remove commented code
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
        self.failedqueue = Queue()
        #self.results = {'Failed' : [] ,'Completed': [], 'Unresolved':[] }
        #self.runnningdownloads = []
        self.resources = {}

        
        self.mainprocessprogress = None

        for idx,resourceurl in enumerate(self.resourceurls):
            resourceobj = Resource(idx, resourceurl)
            if resourceobj.protocolresolved:
                statusvalue = "Resolved Protocol Ready for Download"
                self.jobqueue.put(idx)
                resourceobj.update_status(statusvalue)    
            else:
                statusvalue = "Protocol could not be resolved no further processing"
                #self.failedqueue.put((idx, statusvalue))
                #self.results['Unresolved'].append(idx)
                resourceobj.update_status(statusvalue)
                           
            self.resources[idx] = resourceobj      
       
        self.threadsize = 2

    def check_failed_downloads_deletion(self):
        #check if fetch from Queue thr resource idx
        #for resourceidx in self.results['Failed']:
        try:
            failed_resourceidx, status = self.failedqueue.get_nowait()
            resourceobj = self.resources[failed_resourceidx]
            if 'Failed' in resourceobj.get_status():
                try:
                    if resourceobj.downloadfilepath:
                        self.delete_failed_download(resourceobj)
                    resourceobj.update_status('Deletion Verified')
                except:
                    resourceobj.update_status('Deletion Could not be Verified')
            self.failedqueue.task_done()

        except:
            pass


    def delete_failed_download(self, resourceobj):
        try:
            if resourceobj.protocol_downloader:
                try:
                    currdownloader = resourceobj.protocol_downloader
                    delete_failed = not(currdownloader.delete_successful)
                    
                    if delete_failed and currdownloader.connectionactive:
                        currdownloader.abort_download()
                    elif delete_failed:
                        currdownloader.delete_file()
                    elif currdownloader.connectionactive:
                        currdownloader.disconnect()
                    else:
                        pass
                except:
                     os.remove(resourceobj.downloadfilepath) 
            else:
                os.remove(resourceobj.downloadfilepath) 
        except OSError as osexcp:
                if osexcp.errno == errno.ENOENT:
                    pass
        except:
           raise
 

    def monitor_progress(self):
        """Monitors the progress of Resources waiting download in queue and also clears downloads in failed queue"""
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
                # #progress = len(self.failedqueue)
                # self.mainprocessprogress.update(progress)

                for k,resourceobj in self.resources.items():
                    resourceobj.plot_progress()                
                self.check_failed_downloads_deletion()                
                time.sleep(1)
            
            self.check_failed_downloads_deletion()
        except:
            self.check_failed_downloads_deletion()
            raise


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
                #jobprocessor = DownloadProcessor(threadidx, self.jobqueue, self.failedqueue, self.resources, self.path_download_dir,self.runnningdownloads, self.results)
                jobprocessor = DownloadProcessor(threadidx, self.jobqueue, self.failedqueue, self.resources, self.path_download_dir)
                jobprocessor.start()

            self.jobqueue.join()
            progress_monitor.join()
        finally:
            # self.jobqueue.join()
            # progress_monitor.join()
            self.check_failed_downloads_deletion()            
            self.failedqueue.join()
            time.sleep(5)
            print(" \nCompleted current iteration for Downloading Resources")


