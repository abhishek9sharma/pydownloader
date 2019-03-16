from  resourcedownloader.downloadservice.download_factory import DownloadProtocolFactory
from tqdm import  tqdm
import os

class Resource(object):

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
   
    def set_status(self, statusvalue):
        self.status = statusvalue

    def set_downloadfilepath(self, path):
        self.downloadfilepath =  path

    def plot_progress(self):
        if self.protocolresolved and self.protocol_downloader:
            description, downloaded, totalsize = self.protocol_downloader.get_download_progress()            
            if self.download_progress is None:
                #description = self.protocol_downloader._downloaded_file_name
                downloadsize = self.protocol_downloader._chunksize
                downloadunit = self.protocol_downloader._chunkunit
                self.download_progress = tqdm(total=totalsize, desc=description,  unit_divisor=downloadsize,
                                                     unit_scale=True, unit=downloadunit, disable = False)
            curr_advancement = downloaded - self.download_progress.n
            self.download_progress.update(curr_advancement)
        else:
            return

