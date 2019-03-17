from resourcedownloader.downloadservice.resource_downloader import BaseDownloader
import pysftp
import  os
class SFTPDownloader(BaseDownloader):
    
    def __init__(self, resourceurl, path_download_dir):
        super().__init__(resourceurl, path_download_dir)
        #cnopts = pysftp.CnOpts()
        #cnopts.hostkeys = None
        self.sftpconnector = None
        self.remotepath = None


    def connect(self):

        try:

            host = self.parsed_url.hostname
            port = self.parsed_url.port
            if port is None:
                port = 22
            username = self.parsed_url.username
            password = self.parsed_url.password


            self.sftpconnector = pysftp.Connection(host, username = username, password = password, port = port)
            if self.sftpconnector is None:
                raise Exception( "Failed to create connection for url {0}", self.resourceurl)

            self.remotepath = self.org_file_name
            if self.remotedir:
                self.sftpconnector.cwd(self.remotedir)
                self.remotepath = os.path.join(self.remotedir , self.remotepath)


            if not(self.remotepath):
                self.remotepath = self.org_file_name

            self.size_of_file_to_download = self.sftpconnector.stat(self.remotepath).st_size
            if self.size_of_file_to_download == 0:
                #Not sure if this is actually required except for tracking progress
                raise Exception( " Not Able to determine length of the content to be downloaded for url {0}", self.resourceurl)

        except Exception as e:
                print(e, " aborting download for {0} due to exception while making sftp connection", self.resourceurl)
                self.abortdownload()
                # Add code for handling the case where header does not case content length or any other exception that may occur while setting up
                # connection

    def disconnect(self):
        try:
            self.sftpconnector.close()
        except:
            print("Exception while closing the SFTP connection for URL {0}", self.resourceurl)

    def abortdownload(self):
        try:
            self.disconnect()
            self.delete_file()
        except:
            pass

    def update_progress(self, bytestransferred, bytesleft):
        self.size_of_file_downloaded = bytestransferred

    def download_resource(self):
        try:
            super().download_resource()
            #self.set_download_file_path()
            self.connect()
            #with open(self.path_downloaded_file, 'wb') as f:
            self.sftpconnector.get(self.remotepath, self.path_downloaded_file, self.update_progress)
            self.disconnect()
        except Exception as e:
            print(e, " aborting download for {0} due to some exception while downloading", self.resourceurl)
            self.abortdownload()

    



