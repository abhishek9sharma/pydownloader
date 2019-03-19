from resourcedownloader.downloadservice.resource_downloader import BaseDownloader
import os
import requests

import logging

logging.getLogger("requests").setLevel(logging.WARNING)


class HTTPDownloader(BaseDownloader):

    def __init__(self, resourceurl, path_download_dir, config_path=None):

        """ Returns downloader object for HTTP resoucrce """

        super().__init__(resourceurl, path_download_dir, config_path)
        self.response = None

    def connect(self):

        """ This method extracts connection information from the url and tries to create a HTTP Connection """

        try:
            # connect
            self.response = requests.get(self.resourceurl, stream=True, timeout=self.timeout)
            self.response.raise_for_status()
            self.connectionactive = True

            # compute size
            self.size_of_file_to_download = int(self.response.headers.get('content-length', ))
            if self.size_of_file_to_download == 0:
                raise Exception(" Not Able to determine length of the content to be downloaded for url {0}",
                                self.resourceurl)

        except:
            raise

    def disconnect(self):

        """ This method tries to stop all connections which were created while trying to download an HTTP resource """

        try:
            if self.response:
                self.response.close()
                self.connectionactive = False
        except:
            raise

    def abortdownload(self):

        """ This method tries to stop any active HTTP connections and delete the  downloaded FTP resource """

        try:
            self.disconnect()
        except:
            raise
        finally:
            self.delete_file()

    def download_resource(self, resourceidx):

        """ 
            This method tries to download a HTTP resource attached with the class.
            In case of partial download tries to delete the download file downloaded 
        """

        try:
            super().download_resource(resourceidx)
            self.connect()
            with open(self.path_downloaded_file, 'wb') as f:
                for current_chunk in self.response.iter_content(chunk_size=self.chunksize):
                    if current_chunk:
                        self.size_of_file_downloaded += f.write(current_chunk)

            try:
                self.disconnect()
            except:
                # delete only if download incomplete
                if self.size_of_file_to_download == self.size_of_file_downloaded:
                    pass
                else:
                    raise
        except:
            self.abortdownload()
            raise
