from resourcedownloader.downloadservice.resource_downloader import BaseDownloader
import  os
from ftplib import  FTP
class FTPDownloader(BaseDownloader):
    
    def __init__(self, resourceurl, path_download_dir):
        super().__init__(resourceurl, path_download_dir)
        self.ftpconnector = FTP()
        self.remotepath = None

    def connect(self):

        try:

            host = self.parsed_url.hostname
            port = self.parsed_url.port
            if port is None:
                port =0
            username = self.parsed_url.username
            password = self.parsed_url.password
            self.ftpconnector.connect(host= host, port= port)
            self.ftpconnector.login( user = username, passwd= password)
            self.remotepath = self.org_file_name

            if self.remotedir:
                self.ftpconnector.cwd(self.remotedir)
                self.remotepath = os.path.join(self.remotedir , self.remotepath)

            if not(self.remotepath):
                self.remotepath = self.org_file_name

            self.size_of_file_to_download = self.ftpconnector.size(self.remotepath)
            if self.size_of_file_to_download == 0:
                #Not sure if this is actually required except for tracking progress
                raise Exception( " Not Able to determine length of the content to be downloaded for url {0}", self.resourceurl)

        except Exception as e:
                print(e, " aborting download for {0} due to exception while making ftp connection", self.resourceurl)
                self.abortdownload()

    def disconnect(self):
        if self.ftpconnector.sock:
            try:
                self.ftpconnector.quit()
            except:
                self.ftpconnector.close()

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
            with open(self.path_downloaded_file, 'wb') as f:
                def download_chunk(chunk):
                    self.size_of_file_downloaded += f.write(chunk)
                self.ftpconnector.retrbinary('RETR ' + self.org_file_name, download_chunk, blocksize=self.chunksize)
            self.disconnect()
        except Exception as e:
            print(e, " aborting download for {0} due to some exception while downloading", self.resourceurl)
            self.abortdownload()
