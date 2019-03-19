# import  sys
# print(sys.path)
from resourcedownloader.processor.downloadprocessor import  DownloadProcessor
from resourcedownloader.processor.resource import Resource
from queue import Queue,Empty
from threading import  Thread, Semaphore
import  os
import  errno
import  time
from tqdm import  tqdm
from configparser import  ConfigParser
from pathlib import  Path
import sys
import logging
from  datetime import  datetime



#TODO:     # Main Progress Bar
#TODO :     #remove commented code
#TODO :    #Temp Dir and Cleanup a possible way


class DownloadsProcessor:

    def __init__(self, resourceurlslist, path_download_dir, config_path = None):

        if len(resourceurlslist) == 0 or resourceurlslist is None:
            raise ValueError('No urls are present in the file specified')

        if path_download_dir == '' or path_download_dir is None:
            raise ValueError(" Download directory is not specified or is invalid. Please check ")

        self.resourceurls = resourceurlslist
        self.path_download_dir = os.path.join(path_download_dir)
        self.config_path = self.set_config_path(config_path)
        self.configparser = None
        self.logger = self.set_logger()
        self.progress_info_mode = 1



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
                resourceobj.update_status(statusvalue)
                loginfo = statusvalue + " is the  status for url:{0}\n".format(resourceobj.resourceurl)
                excpinfo = " ".join(['\t\t\t\t\t     Failed with exception' + str(e) + '\n' for e in
                                     resourceobj.exceptions_if_failed])
                self.logger.info(loginfo + excpinfo)

                           
            self.resources[idx] = resourceobj      
       
        self.threadsize = 2
        self.logger.info("resource objects initiated")

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

    def get_currtime_str(self):
        timestampformat = '%Y%m%d__%H%M%S'
        currtime_str = str(datetime.now().strftime(timestampformat))
        return  currtime_str

    def set_logger(self):
        uniqfilename = os.path.join(str(Path(__file__).parents[1]),'Logs', self.get_currtime_str()+ '_main_joblog.log')
        #uniqfilename = str(self.get_currtime_str()+ '_'+ self.threadtempid +'_' + 'joblog.log')

        logger = logging.getLogger(str(uniqfilename))
        logger.setLevel(logging.INFO)
        logfilepath = uniqfilename

        handler = logging.FileHandler(logfilepath)
        logformat = logging.Formatter('%(asctime)s:%(message)s')
        handler.setFormatter(logformat)
        logger.propagate = False
        logger.addHandler(handler)

        return  logger


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

            while True:
                if self.progress_info_mode ==1:
                    total = len(self.resources)
                    left = self.jobqueue.unfinished_tasks
                    finished = total - left
                    #self.basic_progress_bar(finished,total, status='Progress')
                    #time.sleep(0.5)  # emulating long-playing job
                    opstring = "Total Jobs: {0}  Jobs Finished : {1} Jobs Left : {2}".format(total, finished, left)
                    sys.stdout.write(opstring + '\r')
                    sys.stdout.flush()
                    #print(
                    #time.sleep(0.5)
                    #self.clear_screen()

                else:
                    self.plot_progress_individual()

                    #Track Main Processor
                    #lock = Semaphore(value=1)
                    # lock.acquire()
                    # self.plot_progress_total()
                    # time.sleep(1)
                    # lock.release()

                if self.jobqueue.unfinished_tasks == 0:
                    if self.progress_info_mode == 1:
                        opstring = "Total Jobs: {0}  Jobs Finished : {1} Jobs Left : {2}".format(total, finished, left)
                        print(opstring)
                    else:
                        self.plot_progress_individual()
                        #time.sleep(5)
                        self.failedqueue.join()
                    break              
                self.check_failed_downloads_deletion()
                self.logger.info(" Completed a round of failed downloads removal inside monitor")
                                            
            self.check_failed_downloads_deletion()
            self.logger.info(" Completed final  round of failed downloads removal inside monitor")
        except:
            self.check_failed_downloads_deletion()
            self.logger.info(" Completed  round of failed downloads removal inside monitor exception")
            raise

    # def basic_progress_bar(self,count, total, status=''):
    #     bar_len = 60
    #     filled_len = int(round(bar_len * count / float(total)))
    #
    #     percents = round(100.0 * count / float(total), 1)
    #     bar = '=' * filled_len + '-' * (bar_len - filled_len)
    #
    #     sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    #     sys.stdout.flush()

    def download_resources(self):
        try:
            self.logger.info(" Download Modules Initiated ")
            self.load_config()
            if self.configparser:
                self.set_no_of_threads()



            #Start Monitor
            progress_monitor = Thread(target=self.monitor_progress)
            progress_monitor.start()
            self.logger.info(" Monitoring Thread Initiated ")

            # Start Downloads
            if self.threadsize > len(self.resourceurls):
                noofthreads = len(self.resourceurls)
            else:
                noofthreads = self.threadsize

            for threadidx in range(noofthreads):
                #jobprocessor = DownloadProcessor(threadidx, self.jobqueue, self.failedqueue, self.resources, self.path_download_dir,self.runnningdownloads, self.results)
                jobprocessor = DownloadProcessor(threadidx, self.jobqueue, self.failedqueue, self.resources, self.path_download_dir, self.config_path)
                jobprocessor.start()

            self.logger.info(" Job Proceesing Threads Initiated ")

            self.jobqueue.join()
            self.logger.info(" Trying to Closing  Job Proceesing Threads ")


            self.failedqueue.join()
            self.logger.info(" Completed round of failed downloads removal after job thread closing")

            progress_monitor.join()
            self.logger.info(" Trying to Closing  Monitor Threads ")
            #time.sleep(20)
            #print(' Finished Processing Jobs')
        except:
            self.check_failed_downloads_deletion()
            self.logger.info(" Completed round failed downloads removal inside download module exception")
        finally:
            # self.jobqueue.join()
            # progress_monitor.join()
            self.check_failed_downloads_deletion()
            self.logger.info(" Completed last round of failed downloads removal ")
            #time.sleep(10)
            print(" Completed current iteration for Processing (Downloading) Resources")
            self.logger.info(" Completed current iteration for Processing (Downloading) Resources")


