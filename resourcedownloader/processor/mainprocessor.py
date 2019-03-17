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
        
        if len(self._resourceurls)==0:
            print( " No urls specified. Please provide resource links need to be downloade")
            return

        if self._path_download_dir=='' or self._path_download_dir is None:
            print( " Download directory is not specified or is invalid. Please check ")
            return

        self.jobqueue = Queue()
        self.resultqueue = Queue()
        self.results = {'Failed' : [] ,'Completed': [], 'Unresolved':[] }
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
                statusvalue = "Unresolved : Undefined Protocol"
                self.resultqueue.put((idx, statusvalue))
                self.results['Unresolved'].append(idx)
                resourceobj.set_status(statusvalue)
                           
            self.resources[idx] = resourceobj      
         
        self._threadsize = 6

    def delete_failed_downloads(self):
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
            #print(" Completed Downloading Resources")
        except:
            print('Some execption occured in monitor process')
        finally:
            print('Deleting all failed downloads')
            self.delete_failed_downloads()
            #Consoolidation: Remove files for failed downloade if still present




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


