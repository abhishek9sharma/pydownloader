from resourcedownloader.downloadservice.resource_downloader import BaseDownloader
import pysftp
import  os


#TODO:     # Check for size compute failure in connect method line 20
#TODO:     #port configurable



class SFTPDownloader(BaseDownloader):
    
    def __init__(self, resourceurl, path_download_dir):
        super().__init__(resourceurl, path_download_dir)
        #cnopts = pysftp.CnOpts()
        #cnopts.hostkeys = None
        self.pysftpref = pysftp
        self.sftpconnector = None
        self.remotepath = None


    def connect(self):
        try:
            # Establish Connection
            host = self.parsed_url.hostname
            port = self.parsed_url.port
            if port is None:
                port = 22
            username = self.parsed_url.username
            password = self.parsed_url.password
            self.sftpconnector = self.pysftpref.Connection(host, username = username, password = password, port = port)
            self.remotepath = self.org_file_name
            if self.remotedir:
                self.sftpconnector.cwd(self.remotedir)
                self.remotepath = os.path.join(self.remotedir , self.remotepath)

            # Compute size of file
            if not(self.remotepath):
                self.remotepath = self.org_file_name

            # raise exception if file size cannot be determined
            self.size_of_file_to_download = self.sftpconnector.stat(self.remotepath).st_size
            if self.size_of_file_to_download == 0:
                #Not sure if this is actually required except for tracking progress
                raise Exception( " Not Able to determine length of the content to be downloaded for url {0}", self.resourceurl)

        except:
            raise

    def disconnect(self):
        try:
            self.sftpconnector.close()
        except:
            raise

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

            def update_progress(bytestransferred, bytesleft):
                self.size_of_file_downloaded = bytestransferred

            self.sftpconnector.get(self.remotepath, self.path_downloaded_file, update_progress)

            try:
                self.disconnect()
            except:
                if self.size_of_file_to_download==self.size_of_file_downloaded:
                    pass
                else:
                    raise
        except:
            self.abortdownload()

    



