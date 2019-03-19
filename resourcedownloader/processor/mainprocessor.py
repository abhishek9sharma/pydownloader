# import  sys
# print(sys.path)
from resourcedownloader.processor.downloadprocessor import DownloadProcessor
from resourcedownloader.processor.resource import Resource
from queue import Queue, Empty
from threading import Thread, Semaphore
import threading
import os
import errno
import time
from tqdm import tqdm
from configparser import ConfigParser
from pathlib import Path
import sys
import logging
from datetime import datetime
from resourcedownloader.utils.utilfunctions import *



class DownloadsProcessor:

    def __init__(self, resourceurlslist, path_download_dir, config_path=None):

        """ Constructor for creating a list of resources which need to be downloaded """

        if len(resourceurlslist) == 0 or resourceurlslist is None:
            raise ValueError('No urls are present in the file specified')

        if path_download_dir == '' or path_download_dir is None:
            raise ValueError(" Download directory is not specified or is invalid. Please check ")

        self.resourceurls = resourceurlslist
        self.path_download_dir = os.path.join(path_download_dir)
        self.config_path = set_config_path(config_path)

        self.configparser = None
        self.logger = set_logger('_main_joblog.log')
        self.progress_info_mode = 1

        self.jobqueue = Queue()
        self.failedqueue = Queue()
        self.resources = {}
        self.mainprocessprogress = None
      
        for idx, resourceurl in enumerate(self.resourceurls):
            resourceobj = Resource(idx, resourceurl, config_path)
            if resourceobj.protocolresolved:
                statusvalue = "Resolved Protocol Ready for Download"
                self.jobqueue.put(idx)
                resourceobj.update_status(statusvalue)
                self.logger.info(statusvalue + " is the latest status for url:{0}\n".format(resourceobj.resourceurl))

            else:
                statusvalue = "Protocol could not be resolved no further processing"
                resourceobj.update_status(statusvalue)
                loginfo = statusvalue + " is the  latest status for url:{0}\n".format(resourceobj.resourceurl)
                excpinfo = " ".join(['\t\t\t\t\t     Failed with exception' + str(e) + '\n' for e in
                                     resourceobj.exceptions_if_failed])
                self.logger.info(loginfo + excpinfo)

            self.resources[idx] = resourceobj

        self.threadsize = 2
        self.logger.info("resource objects initiated")

    def load_config(self):

        """ Tries to load configuration based on the config path """

        try:
            self.configparser = ConfigParser()
            configdata = self.configparser.read(self.config_path)
            if configdata and len(configdata) > 0:
                pass
            else:
                self.configparser = None
        except:
            self.configparser = None

    def set_no_of_threads(self):

        """ Tries to set number of threads based on configuration passed or sets them to default values """

        try:
            if self.configparser:
                thread_config = self.configparser['threading']
                threadsize = thread_config.get('noofthreads', 2)
                self.threadsize = int(threadsize)
            else:
                self.threadsize = 2
        except:
            self.threadsize = 2  # set to default so as to keep the process runnning

    def check_failed_downloads_deletion(self):

        """ Checks for downloads which have failed, if their files have not been deleted attempts to forcefully remove them """

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

        """ Tries to delete a file for a resource if not already deleted """
        try:
            if resourceobj.protocol_downloader:
                try:
                    currdownloader = resourceobj.protocol_downloader
                    delete_failed = not (currdownloader.delete_successful)

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

        """Plots the progress about how many jobs processed in tqdm format """

        if self.mainprocessprogress is None:
            desc = " Jobs Completed "
            self.mainprocessprogress = tqdm(desc=desc, total=len(self.resources), disable=False, file=sys.stdout)

        if self.mainprocessprogress.n == len(self.resources):
             pass
        else:
            progress = len(self.resources) - self.jobqueue.unfinished_tasks - self.mainprocessprogress.n
            self.mainprocessprogress.update(progress)
        
    def plot_progress_individual(self, lastcall = False):

        """Plots the progress of individual jobs processed in tqdm format """

        for k, resourceobj in self.resources.items():
            resourceobj.plot_progress(lastcall)

    def get_progress_counts(self, final = False):

        """ Prints job counts based on their current state """

        failed = 0
        downloaded = 0
        downloading = 0
        total = len(self.resources)
        left = self.jobqueue.unfinished_tasks
        
        for k, resourceobj in self.resources.items():
            state = resourceobj.get_current_state()
            if state in ['Download was Successful']:
                 downloaded+=1
            elif state in ['Download Failed']:
                #print(resourceobj.res)
                failed += 1
            elif state in ['Queued', 'Downloading']:
                downloading += 1
        #opstring = "Total Jobs: {0} Running : {1} Downloaded : {2} Failed : {3}".format(total, downloading, downloaded, failed)
        opstring = "Total Jobs:"+ str(total) +" Running:"+ str(downloading) +" Downloaded:" + str(downloaded)+ " Failed :" + str(failed)
        if final:
            print(opstring)
            time.sleep(1)
        else:
            sys.stdout.write(opstring + '\r')
            sys.stdout.flush() 
     

    def monitor_progress(self):

        """Monitors the progress of Resources waiting download in queue and also clears downloads in failed queue"""

        try:

            while True:                
                if self.progress_info_mode == 1:
                    self.get_progress_counts()
                else:
                    self.plot_progress_individual()
                    # Track Main Processor
                    #self.plot_progress_total()
                    # time.sleep(1)
                     #time.sleep(1)
                
                if self.jobqueue.unfinished_tasks == 0:
                    #All jobs should be running by now
                    if self.progress_info_mode == 1:
                        self.get_progress_counts(True)  
                    else:
                        self.plot_progress_individual(True)
                        #self.plot_progress_total()
                        #time.sleep(2)                        
                    break

                self.check_failed_downloads_deletion()
            self.check_failed_downloads_deletion()            
            self.logger.info(" Completed final  round of failed downloads removal inside monitor")
        except:
            self.check_failed_downloads_deletion()
            self.logger.info(" Completed  round of failed downloads removal inside monitor exception")
            raise

    def download_resources(self):

        """ Creates threads for downloading resource files based on resource objects """

        try:
            self.logger.info(" Download Modules Initiated ")
            self.load_config()
            if self.configparser:
                self.set_no_of_threads()

            # Start Monitor
            progress_monitor = Thread(target=self.monitor_progress)
            progress_monitor.start()
            self.logger.info(" Monitoring Thread Initiated ")

            # Start Downloads
            if self.threadsize > len(self.resourceurls):
                noofthreads = len(self.resourceurls)
            else:
                noofthreads = self.threadsize

            for threadidx in range(noofthreads):
                jobprocessor = DownloadProcessor(threadidx, self.jobqueue, self.failedqueue, self.resources,
                                                 self.path_download_dir, self.config_path)
                jobprocessor.start()

            self.logger.info(" Job Proceesing Threads Initiated ")

            self.jobqueue.join()
            self.logger.info(" Trying to Close  Job Proceesing Threads ")
            self.failedqueue.join()
            self.logger.info(" Completed round of failed downloads removal after job thread closing")

            progress_monitor.join()
            self.logger.info(" Trying to Close  Monitor Threads ")

            #tqdm.write (' Finished Processing Jobs Please check logs folder for detailed info')
            for ridx, resourceobj in self.resources.items():
                    print("\t\tFor resource {0} status was {1}".format(resourceobj.resourceurl, resourceobj.get_current_state()))
                    time.sleep(0.1)            
            print(' Finished Processing Jobs \n Please check logs folder for detailed info')

        except:
            self.check_failed_downloads_deletion()
            self.logger.info(" Completed round failed downloads removal inside download module exception")
        finally:
              self.check_failed_downloads_deletion()
              self.logger.info(" Completed last round of failed downloads removal ")
             