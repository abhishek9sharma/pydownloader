from resourcedownloader.downloadservice.resource_downloader import BaseDownloader
import  os
from ftplib import  FTP


#TODO:     # Check for size compute failure in connect method line 20
#TODO:    #port configurable
#TODO: handle timeout
#TODO : Remove commented Code

class FTPDownloader(BaseDownloader):
    
    def __init__(self, resourceurl, path_download_dir):
        super().__init__(resourceurl, path_download_dir)
        self.ftpconnector = FTP()
        self.remotepath = None

    def connect(self):

        try:

            #Establish Connection
            host = self.parsed_url.hostname
            port = self.parsed_url.port
            if port is None:
                port =0
            username = self.parsed_url.username
            password = self.parsed_url.password
            self.ftpconnector.connect(host= host, port= port)
            self.ftpconnector.login( user = username, passwd= password)
            self.connectionactive = True
            
            #Compute size of file
            self.remotepath = self.org_file_name
            if self.remotedir:
                self.ftpconnector.cwd(self.remotedir)
                self.remotepath = os.path.join(self.remotedir , self.remotepath)
            if not(self.remotepath):
                self.remotepath = self.org_file_name
            self.size_of_file_to_download = self.ftpconnector.size(self.remotepath)
            #raise exception if file size cannot be determined
            if self.size_of_file_to_download == 0:
                #Not sure if this is actually required except for tracking progress
                raise ValueError( " Not Able to determine length of the content to be downloaded for url {0}", self.resourceurl)

        except:
            raise

    def disconnect(self):
        if self.ftpconnector.sock:
            try:
                self.ftpconnector.quit()
                self.connectionactive = False
            except:
                self.ftpconnector.close()
                self.connectionactive = False
    
    def abortdownload(self):
        try:
            self.disconnect()
        except:
            raise
        finally:
            self.delete_file()

    def download_resource(self, resourceidx):
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
                if self.size_of_file_to_download==self.size_of_file_downloaded:
                    pass
                else:
                    raise
        except:
            self.abortdownload()
