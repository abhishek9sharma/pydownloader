from resourcedownloader.downloadservice.download_factory import DownloadProtocolFactory
from tqdm import tqdm
import os
from pathlib import Path
import sys
from resourcedownloader.utils.utilfunctions import *
from datetime import datetime


class Resource:

    def __init__(self, idx, resourceurl, config_path=None):

        """construtor for url that needs to be downloaded"""

        self.resourceidx = idx
        self.resourceurl = resourceurl
        self.config_path = set_config_path(config_path)
        self.exceptions_if_failed = []
        try:
            self.protocolclass = DownloadProtocolFactory.get_protocol(self.resourceurl, self.config_path)
        except Exception as e:
            self.protocolclass = None
            self.exceptions_if_failed.append(e)

        self.protocolresolved = True if self.protocolclass else False
        self.protocol_downloader = None
        self.status = "Failed : Undefined Protocol" if not (self.protocolresolved) else ""
        self.download_progress = None
        self.downloadfilepath = None
        self.progress_bar = None

    def set_status(self, statusvalue):
        """ Sets progress status of resource """
        self.status = str(statusvalue)

    def update_status(self, statusvalue):

        """ Updates current progress status of resource """

        currstatus = str(self.get_status())
        if currstatus == '':
            self.set_status(str(statusvalue))
        else:
            newstatus = currstatus + ':' + str(statusvalue).replace(':', '')
            self.set_status(newstatus)

    def get_status(self):

        """ Gets current progress status of resource """

        return self.status

    def set_downloadfilepath(self, path):

        """ Sets download path of current resource """

        self.downloadfilepath = path

    def get_progress_simple(self):
        
        """ Returns simple progress of current resource using tqdm library """
        try:
            if self.protocolresolved and self.protocol_downloader and self.protocol_downloader.downloaded_file_name:
                description, downloaded, totalsize, curr_percentage_progress = self.protocol_downloader.get_download_progress()
                return "{0} percent of resource {1} has been downloaded at {1}".format(curr_percentage_progress, self.resourceurl, description)
            else:
                return "No information about resource  {0}".format(self.resourceurl)
        except:
            return "No information about resource  {0}".format(self.resourceurl)

    def get_current_state(self):        
        status = self.get_status()
        if 'Download Completed' in status:
            return 'Download was Successful'
        elif 'Failed' in status:
            return 'Download Failed'
        elif status=='Resolved Protocol Ready for Download':
            return 'Queued'
        else:
            return 'Downloading'

    def plot_progress(self, lastcall = False):
        
        """plots progress of current resource using tqdm library """

        try:
            #if lastcall:
            #    if self.progress_bar:
            #        self.progress_bar.close()

            if self.protocolresolved and self.protocol_downloader and self.protocol_downloader.downloaded_file_name:
                description, downloaded, totalsize, curr_percentage_progress = self.protocol_downloader.get_download_progress()
                if totalsize == 0:
                    description += 'Cannot track progress as size of file not determined'

                if self.download_progress is None:
                    self.download_progress = tqdm(total=100, desc=description, disable=False, file=sys.stdout)

                if self.download_progress.n == 100:
                    #self.progress_bar.close()
                    pass
                else:
                    currprogress = curr_percentage_progress - self.download_progress.n
                    self.download_progress.update(currprogress)
                    #time.sleep(1)
                    
            else:
                return
        except:
            pass  # this should be implemented
