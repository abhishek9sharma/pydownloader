from resourcedownloader.downloadservice.resource_downloader import BaseDownloader
import pysftp
import  os


#TODO:     # Check for size compute failure in connect method line 20
#TODO: handle timeout
#TODO : Remove commented Code


class SFTPDownloader(BaseDownloader):
    
    def __init__(self, resourceurl, path_download_dir, config_path = None):
        super().__init__(resourceurl, path_download_dir,  config_path)
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
            #port = None

            if port is None:
                self.set_port_from_config()
                port = self.port
            username = self.parsed_url.username
            password = self.parsed_url.password
            self.sftpconnector = self.pysftpref.Connection(host, username = username, password = password, port = port)
            self.remotepath = self.org_file_name
            if self.remotedir:
                self.sftpconnector.cwd(self.remotedir)
                self.remotepath = os.path.join(self.remotedir , self.remotepath)
            self.connectionactive = True
            
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
            self.connectionactive = False
        except:
            raise

    def abortdownload(self):
        try:
            self.disconnect()
        except:
            raise
        finally:
            self.delete_file()

    def set_port_from_config(self):
        try:
            if self.configparser:
                ports = self.configparser['ports']
                port = ports.get(self.protocol, 22)
                self.port = int(port)
            else:
                self.port = 22
        except:
            self.port = 22 # default set to continue process


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

    



