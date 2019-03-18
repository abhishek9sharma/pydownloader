# import  sys
# print(sys.path)
from queue import Queue,Empty
from threading import  Thread, Semaphore
from resourcedownloader.processor.downloadprocessor import  DownloadProcessor
from resourcedownloader.processor.resource import Resource
import  os
import  errno
import  time
from tqdm import  tqdm
from configparser import  ConfigParser
from pathlib import  Path


#TODO:     # Q used Needs to B Tested # Network error such as wifi Temp Dir and Cleanup a possible way
#TODO:     # Write a Log Somewhere
#TODO:     # errors for 0 inputs
#TODO :     #remove commented code
#TODO:     #Detailed Logging at each faiure
#TODO:     # Main Process Check if to keep or remove


class DownloadsProcessor:

    def __init__(self, resourceurlslist, path_download_dir, config_path = None):
        self.resourceurls = resourceurlslist
        self.path_download_dir = os.path.join(path_download_dir)
        self.config_path = self.set_config_path(config_path)
        self.configparser = None
        

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
            resourceobj = Resource(idx, resourceurl, config_path)
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

    def set_config_path(self, config_path):
        try:
            if config_path is None:
                return os.path.join(str(Path(__file__).parents[1]),'config','config.ini')
            else:
                return  os.path.join(os.path.dirname(config_path) , os.path.basename(config_path))
        except:
            return  None

    def load_config(self):
        try:
            self.configparser = ConfigParser()
            configdata =self.configparser.read(self.config_path)
            if configdata and len(configdata)>0:
                pass
            else:
                self.configparser = None
        except:
            self.configparser = None


    def set_no_of_threads(self):
        try:
            if self.configparser:
                thread_config = self.configparser['threading']
                threadsize = thread_config.get('noofthreads', 2)
                self.threadsize = int(threadsize)
            else:
                self.threadsize = 2
        except:
            self.threadsize = 2 # set to default so as to keep the process runnning



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
    
    def plot_progress_total(self):
        if self.mainprocessprogress is None:
            desc = " Jobs Completed "
            self.mainprocessprogress = tqdm(desc=desc, total=len(self.resources), disable= False)
        
        if self.mainprocessprogress.n==len(self.resources):
            pass
        else:
            progress = len(self.resources) - self.jobqueue.unfinished_tasks - self.mainprocessprogress.n
            self.mainprocessprogress.update(progress)             

    def plot_progress_individual(self):
        lock = Semaphore(value=1)
        lock.acquire() 
        for k,resourceobj in self.resources.items():                          
            resourceobj.plot_progress()     
        #time.sleep(0.1)           
        lock.release()

    def monitor_progress(self):
        """Monitors the progress of Resources waiting download in queue and also clears downloads in failed queue"""
        try:
            lock = Semaphore(value=1)
            while True:
                
                self.plot_progress_individual()

                #Track Main Processor                    
                # lock.acquire()                
                # self.plot_progress_total()
                # time.sleep(1)  
                # lock.release()

                if self.jobqueue.unfinished_tasks == 0:
                    #self.plot_progress_individual()
                    time.sleep(5)
                    break              
                #self.check_failed_downloads_deletion() 
               
                                            
            self.check_failed_downloads_deletion()
        except:
            self.check_failed_downloads_deletion()
            raise


    def download_resources(self):
        try:
            self.load_config()
            if self.configparser:
                self.set_no_of_threads()

            #Start Monitor
            progress_monitor = Thread(target=self.monitor_progress)
            progress_monitor.start()

            # Start Downloads
            if self.threadsize > len(self.resourceurls):
                noofthreads = len(self.resourceurls)
            else:
                noofthreads = self.threadsize

            for threadidx in range(noofthreads):
                #jobprocessor = DownloadProcessor(threadidx, self.jobqueue, self.failedqueue, self.resources, self.path_download_dir,self.runnningdownloads, self.results)
                jobprocessor = DownloadProcessor(threadidx, self.jobqueue, self.failedqueue, self.resources, self.path_download_dir, self.config_path)
                jobprocessor.start()

            self.jobqueue.join()
            self.failedqueue.join()
            progress_monitor.join()
            #time.sleep(20)
            #print(' Finished Processing Jobs')
        finally:
            # self.jobqueue.join()
            # progress_monitor.join()
            self.check_failed_downloads_deletion()           
            time.sleep(10)
            print(" Completed current iteration for Processing (Downloading) Resources")


