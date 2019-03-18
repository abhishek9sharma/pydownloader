from  resourcedownloader.downloadservice.download_factory import DownloadProtocolFactory
from tqdm import  tqdm
import os

#TODO: Remove Code from PlotProgress
#TODO : Remove commented Code

class Resource:

    def __init__(self, idx, resourceurl):
        """construtor for url that needs to be downloaded"""
        self.resourceidx = idx
        self.resourceurl = resourceurl
        self.protocolclass = DownloadProtocolFactory.get_protocol(self.resourceurl)
        self.protocolresolved = True if self.protocolclass else False
        self.protocol_downloader = None
        self.status = "Failed : Undefined Protocol" if not(self.protocolresolved) else ""
        self.download_progress = None
        self.downloadfilepath = None
        self.progress_bar = None
        self.exceptions_if_failed = []
   
    def set_status(self, statusvalue):
        self.status = str(statusvalue)
  
    def update_status(self, statusvalue):
        currstatus = str(self.get_status())
        if currstatus =='':
            self.set_status(str(statusvalue))
        else:
            newstatus = currstatus + ':' + str(statusvalue).replace(':','')
            self.set_status(newstatus)

    
    def get_status(self):
        return self.status

    def set_downloadfilepath(self, path):
        self.downloadfilepath =  path

    def plot_progress(self):
        if self.protocolresolved and self.protocol_downloader:
            description, downloaded, totalsize, curr_percentage_progress = self.protocol_downloader.get_download_progress()
            if totalsize==0:
                description += 'Cannot track progress as size of file not determined'
                #print('Cannot track progress of {0} as total size determined is {1} ', description, totalsize)

            #print(curr_percentage_progress)
            #print(curr_percentage_progress)
            #urr_percentage_progress = int(100* float(downloaded/totalsize))
            #print(description, curr_percentage_progress)
            if self.download_progress is None:
                #description = self.protocol_downloader.downloaded_file_name
                self.download_progress = tqdm(total=100, desc=description, disable=False)
            currprogress = curr_percentage_progress - self.download_progress.n
            self.download_progress.update(currprogress)

            # if self.download_progress is None:
            #     downloadsize = self.protocol_downloader.chunksize
            #     downloadunit = self.protocol_downloader.chunkunit
            #     self.download_progress = tqdm(total=totalsize, desc=description,  unit_divisor=downloadsize,
            #                                  unit_scale=True, unit= downloadunit, disable = False)
            # curr_advancement = downloaded - self.download_progress.n
            # self.download_progress.update(curr_advancement)
        else:
            return


