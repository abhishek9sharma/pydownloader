from threading import  Thread
from queue import  Queue,Empty
from resourcedownloader.processor.resource import Resource
import  os
from pathlib import Path
import logging
from _datetime import  datetime

#TODO : Remove commented Code

#logging.basicConfig(level = logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
#logging.getLogger().setLevel(logging.INFO)


class DownloadProcessor(Thread):
    
    #def __init__(self, threadidx, jobqueue, failedqueue, resources, pathtodownload, runningdownloads, results):
    def __init__(self, threadidx, jobqueue, failedqueue, resources, pathtodownload, config_path = None):
        Thread.__init__(self)
        self.pathtodownload = pathtodownload
        self.threadtempid = str(threadidx)
        self.logger = self.set_logger()
        self.jobqueue = jobqueue
        self.failedqueue = failedqueue
        self.resources= resources
        self.config_path =  self.set_config_path(config_path)
        #self.runnningdownloads = runningdownloads
        #self.results = results

    def get_currtime_str(self):
        timestampformat = '%Y%m%d__%H%M%S'
        currtime_str = str(datetime.now().strftime(timestampformat))
        return  currtime_str

    def set_logger(self):
        uniqfilename = os.path.join(str(Path(__file__).parents[1]),'Logs', self.get_currtime_str()+ '_'+ self.threadtempid+'_' +'thread_joblog.log')
        #uniqfilename = str(self.get_currtime_str()+ '_'+ self.threadtempid +'_' + 'joblog.log')

        logger = logging.getLogger(str(uniqfilename))
        logger.setLevel(logging.INFO)
        logfilepath = os.path.join(self.pathtodownload, uniqfilename +'.log' )

        handler = logging.FileHandler(logfilepath)
        logformat = logging.Formatter('%(asctime)s:%(message)s')
        handler.setFormatter(logformat)
        logger.propagate = False
        logger.addHandler(handler)

        return  logger


    def set_config_path(self, config_path):
        try:
            if config_path is None:
                return os.path.join(str(Path(__file__).parents[1]),'config','config.ini')
            else:
                return  os.path.join(os.path.dirname(config_path) , os.path.basename(config_path))
        except:
            return  None
    

    def run(self):
         while True:
            try:
               #resourceidx = self.jobqueue.get_nowait()
                resourceidx = self.jobqueue.get_nowait()
            except Empty:
                break
            except:
                raise

            try:
                curr_resource = self.resources[resourceidx]                
                statusval = 'Resource Index Extracted in Download Thread :'
                curr_resource.update_status(statusval)
                
                protocoldownloaderclass = curr_resource.protocolclass
                curr_resource.protocol_downloader = protocoldownloaderclass(curr_resource.resourceurl, self.pathtodownload, self.config_path)
                #self.runnningdownloads.append(resourceidx) # should use some other data structure as compared to list
                statusval = 'Downloader Object Attached in Thread :'
                curr_resource.update_status(statusval)
                
                file_idx = self.threadtempid + '_'+ str(resourceidx)
                statusval = 'Calling Download Method of Downloader :'
                curr_resource.update_status(statusval)                
                curr_resource.protocol_downloader.download_resource(file_idx)
                curr_resource.set_downloadfilepath(curr_resource.protocol_downloader.get_download_path())
                #self.results['Completed'].append(resourceidx)
                #self.runnningdownloads.remove(resourceidx)
                statusval = 'Download Completed :'
                curr_resource.update_status(statusval)
                self.logger.info( statusval + " for url:{0} and is present at {1}".format(curr_resource.resourceurl, curr_resource.downloadfilepath))
                          
            #checl if below is right format
            except Exception as e:
                # check addtions to failedqueue and results
                statusval = 'Download Failed    :'
                curr_resource = self.resources[resourceidx]               
                curr_resource.update_status(statusval)
                self.failedqueue.put((resourceidx, statusval))
                curr_resource.exceptions_if_failed.append(e)
                loginfo = statusval + " is the  status for url:{0}\n".format(curr_resource.resourceurl)
                excpinfo = " ".join(['\t\t\t\t\t     Failed with exception' + str(e) +'\n' for e in curr_resource.exceptions_if_failed])
                self.logger.info( loginfo + excpinfo)
                #self.results['Failed'].append(resourceidx)
                #may be attempt a delete here may be not as waste of time
                #self.jobqueue.task_done()
            # finally:
            #     if resourceidx not in self.resources:
            #         pass
            #     else:
            #         if resourceidx in self.runnningdownloads:
            #             self.runnningdownloads.remove(resourceidx)
            self.jobqueue.task_done()
