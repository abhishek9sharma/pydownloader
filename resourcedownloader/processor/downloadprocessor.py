from threading import  Thread
from queue import  Queue,Empty
from resourcedownloader.processor.resource import Resource


class DownloadProcessor(Thread):
    def __init__(self, jobqueue, resultqueue, resources, pathtodownload, runningdownloads, results):
        Thread.__init__(self)
        self.jobqueue = jobqueue
        self.resultqueue = resultqueue
        self.resources= resources
        self.pathtodownload = pathtodownload
        self.runnningdownloads = runningdownloads
        self.results = results

    def run(self):
         while True:
            try:
                resourceidx = self.jobqueue.get_nowait()
            except Empty:            
                break
            
            try:               
                curr_resource = self.resources[resourceidx]                
                protocoldownloaderclass = curr_resource.protocolclass
                curr_resource.protocol_downloader = protocoldownloaderclass(curr_resource.resourceurl, self.pathtodownload)                 
                self.runnningdownloads.append(resourceidx) # should use some other data structure as compared to list
                
                statusval = 'Download Started'
                curr_resource.set_status(statusval)
                curr_resource.protocol_downloader.download_resource()
                curr_resource.set_downloadfilepath(curr_resource.protocol_downloader.get_download_path())
                self.runnningdownloads.remove(resourceidx)

                statusval = 'Download Completed'
                self.resultqueue.put((resourceidx, statusval))
                self.results['Completed'].append(resourceidx)

                curr_resource.set_status(statusval)
                self.jobqueue.task_done()
            except:
                statusval = 'Failed while downloading'
                if resourceidx not in self.resources:
                    print(" No resource object found with index {0}", resourceidx)
                else:
                    self.resources[resourceidx].set_status(statusval)
                    self.resultqueue.put((resourceidx, statusval))
                    self.results['Completed'].append(resourceidx)

                self.jobqueue.task_done()
            finally:
                if resourceidx not in self.resources:
                    pass
                else:
                    if resourceidx in self.runnningdownloads:
                        self.runnningdownloads.remove(resourceidx)



