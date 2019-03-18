from threading import  Thread
from queue import  Queue,Empty
from resourcedownloader.processor.resource import Resource
import  os
from pathlib import Path

#TODO:     ##Exception format line 56
#TODO:     ##what if failure while adding to faile queue
#TODO : Remove commented Code

class DownloadProcessor(Thread):
    
    #def __init__(self, threadidx, jobqueue, failedqueue, resources, pathtodownload, runningdownloads, results):
    def __init__(self, threadidx, jobqueue, failedqueue, resources, pathtodownload, config_path = None):
        Thread.__init__(self)
        self.threadtempid = str(threadidx)
        self.jobqueue = jobqueue
        self.failedqueue = failedqueue
        self.resources= resources
        self.pathtodownload = pathtodownload
        self.config_path =  self.set_config_path(config_path)
        #self.runnningdownloads = runningdownloads
        #self.results = results

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
                
            #checl if below is right format
            except Exception as e:
                # check addtions to failedqueue and results
                statusval = 'Failed while downloading :'
                curr_resource = self.resources[resourceidx]               
                curr_resource.update_status(statusval)
                self.failedqueue.put((resourceidx, statusval))
                curr_resource.exceptions_if_failed.append(e)
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
