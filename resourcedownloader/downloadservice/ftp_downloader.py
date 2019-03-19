from resourcedownloader.downloadservice.resource_downloader import BaseDownloader
import os
from ftplib import FTP
from configparser import ConfigParser

import logging

logging.getLogger("ftplib").setLevel(logging.WARNING)


class FTPDownloader(BaseDownloader):

    def __init__(self, resourceurl, path_download_dir, config_path=None):

        """ Returns downloader object for FTP resoucrce """

        super().__init__(resourceurl, path_download_dir, config_path)
        self.ftpconnector = FTP()
        self.remotepath = None

    def set_port_from_config(self):

        """ Sets the default port to be used for downloading FTP file """

        try:
            if self.configparser:
                ports = self.configparser['ports']
                port = ports.get(self.protocol, 21)
                self.port = int(port)
            else:
                self.port = 21
        except:
            self.port = 21
            # default set to continue process

    def connect(self):

        """ This method extracts connection information from the url and tries to create a FTP Connection """

        try:
            # Establish Connection
            host = self.parsed_url.hostname
            port = self.parsed_url.port

            if port is None:
                self.set_port_from_config()
                port = self.port

            username = self.parsed_url.username
            password = self.parsed_url.password
            self.ftpconnector.connect(host=host, port=port, timeout=self.timeout)
            self.ftpconnector.login(user=username, passwd=password)
            self.connectionactive = True

            # Compute size of file
            self.remotepath = self.org_file_name
            if self.remotedir:
                self.ftpconnector.cwd(self.remotedir)
                self.remotepath = os.path.join(self.remotedir, self.remotepath)
            self.size_of_file_to_download = self.ftpconnector.size(self.remotepath)

            # raise exception if file size cannot be determined as unreliable download
            if self.size_of_file_to_download == 0:
                raise ValueError(
                    " Aborting, as not able to determine length of the content to be downloaded for url {0}",
                    self.resourceurl)

        except:
            raise

    def disconnect(self):

        """ This method tries to stop all connections which were created while trying to download an FFTP resource """

        if self.ftpconnector.sock:
            try:
                self.ftpconnector.quit()
                self.connectionactive = False
            except:
                self.ftpconnector.close()
                self.connectionactive = False

    def abortdownload(self):

        """ This method tries to stop any active FTP connections and delete the downloaded FTP resource """

        try:
            self.disconnect()
        except:
            raise
        finally:
            self.delete_file()

    def download_resource(self, resourceidx):

        """ 
            This method tries to download a FTP resource attached with the class.
            In case of partial download tries to delete the file downloaded 
        """

        try:
            super().download_resource(resourceidx)
            self.connect()
            with open(self.path_downloaded_file, 'wb') as f:
                def download_chunk(chunk):
                    self.size_of_file_downloaded += f.write(chunk)

                self.ftpconnector.retrbinary('RETR ' + self.org_file_name, download_chunk, blocksize=self.chunksize)

            try:
                self.disconnect()
            except:
                if self.size_of_file_to_download == self.size_of_file_downloaded:
                    pass
                else:
                    raise
        except:
            self.abortdownload()
            raise
