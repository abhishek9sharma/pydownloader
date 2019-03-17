from threading import  Thread
from queue import  Queue,Empty
from resourcedownloader.processor.resource import Resource


#TODO:     #attempt delete after exception Line 49
#TODO:     ##Result Queue May Be Delete or convert to failed queue
#TODO:     ##Exception format line 46
#TODO:     ##finnaly may be remove if runningdownloads is not required


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
                curr_resource.protocol_downloader.download_resource(str(resourceidx))
                curr_resource.set_downloadfilepath(curr_resource.protocol_downloader.get_download_path())
                self.runnningdownloads.remove(resourceidx)

                # check addtions to resultqueue and results
                statusval = 'Download Completed'
                curr_resource.set_status(statusval)
                self.resultqueue.put((resourceidx, statusval))
                self.results['Completed'].append(resourceidx)

                self.jobqueue.task_done()
            #checl if below is right format
            except Exception as e:

                # check addtions to resultqueue and results
                statusval = 'Failed while downloading'
                self.resources[resourceidx].set_status(statusval)
                self.resources[resourceidx].exceptions_if_failed.appened(e)
                self.resultqueue.put((resourceidx, statusval))
                self.results['Failed'].append(resourceidx)
                #may be attempt a delete here
                self.jobqueue.task_done()
            finally:
                if resourceidx not in self.resources:
                    pass
                else:
                    if resourceidx in self.runnningdownloads:
                        self.runnningdownloads.remove(resourceidx)



