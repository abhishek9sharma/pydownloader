from resourcedownloader.downloadservice.resource_downloader import BaseDownloader
import  os
from ftplib import  FTP
class FTPDownloader(BaseDownloader):
    
    def __init__(self, resourceurl, path_download_dir):
        super().__init__(resourceurl, path_download_dir)
        self._ftpconnector = FTP()

    def connect(self):

        try:

            host = self._parsed_url.hostname
            port = self._parsed_url.port
            if port is None:
                port =0
            username = self._parsed_url.username
            password = self._parsed_url.password
            self._ftpconnector.connect(host= host, port= port)
            self._ftpconnector.login( user = username, passwd= password)
            remotepath = self._org_file_name

            if self._remotedir:
                self._ftpconnector.cwd(self._remotedir)
                remotepath = self._remotedir + remotepath


        except Exception as e:
            print(e, " aborting download for {0} due to exception while making ftp connection", self._resourceurl)
            self.abortdownload()

        try:
            self._size_of_file_to_download = self._ftpconnector.size(remotepath)
            if self._size_of_file_to_download == 0:
                #Not sure if this is actually required except for tracking progress
                raise Exception( " Not Able to determine length of the content to be downloaded for url {0}", self._resourceurl)
        except Exception as e:
            raise e
            #Add code for handling the case where header does not case content length or any other exception that may occur while setting up
            # connection

    def disconnect(self):
        if self._ftpconnector.sock:
            try:
                self._ftpconnector.quit()
            except:
                self._ftpconnector.close()

    def abortdownload(self):
        try:
            self.disconnect()
            self.delete_file()
        except:
            pass




    def download_resource(self):
        try:
            super().download_resource()
            #self.set_download_file_path()
            self.connect()
            with open(self._path_downloaded_file, 'wb') as f:
                def download_chunk(chunk):
                    self._size_of_file_downloaded += f.write(chunk)
                self._ftpconnector.retrbinary('RETR ' + self._org_file_name, download_chunk, blocksize=self._chunksize)
            self.disconnect()
        except Exception as e:
            print(e, " aborting download for {0} due to some exception while downloading", self._resourceurl)
            self.abortdownload()
