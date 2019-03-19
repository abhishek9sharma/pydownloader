from threading import Thread
from queue import Queue, Empty
from resourcedownloader.processor.resource import Resource
import os
from pathlib import Path
import logging
from datetime import datetime
from resourcedownloader.utils.utilfunctions import *


class DownloadProcessor(Thread):

    def __init__(self, threadidx, jobqueue, failedqueue, resources, pathtodownload, config_path=None):

        """ Constructor for a thread object which proceses the resources to be downloaded """

        Thread.__init__(self)
        self.pathtodownload = pathtodownload
        self.threadtempid = str(threadidx)
        self.logger = set_logger(self.threadtempid + '_' + 'thread_joblog.log')

        self.jobqueue = jobqueue
        self.failedqueue = failedqueue
        self.resources = resources
        self.config_path = set_config_path(config_path)

    def run(self):

        """Extracts a resource from the job queue and  tries to download it"""

        while True:
            try:
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
                curr_resource.protocol_downloader = protocoldownloaderclass(curr_resource.resourceurl,
                                                                            self.pathtodownload, self.config_path)

                statusval = 'Downloader Object Attached in Thread :'
                curr_resource.update_status(statusval)

                file_idx = self.threadtempid + '_' + str(resourceidx)
                statusval = 'Calling Download Method of Downloader :'

                curr_resource.update_status(statusval)
                curr_resource.protocol_downloader.download_resource(file_idx)
                curr_resource.set_downloadfilepath(curr_resource.protocol_downloader.get_download_path())
                statusval = 'Download Completed :'

                curr_resource.update_status(statusval)
                self.logger.info(statusval + " for url:{0} and is present at {1}".format(curr_resource.resourceurl,
                                                                                         curr_resource.downloadfilepath))

            except Exception as e:
                statusval = 'Download Failed    :'
                curr_resource = self.resources[resourceidx]
                curr_resource.update_status(statusval)
                self.failedqueue.put((resourceidx, statusval))
                curr_resource.exceptions_if_failed.append(e)
                loginfo = statusval + " is the  status for url:{0}\n".format(curr_resource.resourceurl)
                excpinfo = " ".join(['\t\t\t\t\t     Failed with exception' + str(e) + '\n' for e in
                                     curr_resource.exceptions_if_failed])
                self.logger.info(loginfo + excpinfo)

            self.jobqueue.task_done()
