from resourcedownloader.downloadservice.resource_downloader import BaseDownloader
import pysftp
import  os

import  logging
logging.getLogger("paramiko").setLevel(logging.WARNING)



class SFTPDownloader(BaseDownloader):
    
    def __init__(self, resourceurl, path_download_dir, config_path = None):

        """ Returns downloader object for SFTP resoucrce """

        super().__init__(resourceurl, path_download_dir,  config_path)
        self.pysftpref = pysftp
        self.sftpconnector = None
        self.remotepath = None


    def connect(self):

        """ This method extracts connection information from the url and tries to create a SFTP Connection """

        try:
            # Establish Connection
            host = self.parsed_url.hostname
            port = self.parsed_url.port
  
            if port is None:
                self.set_port_from_config()
                port = self.port
            username = self.parsed_url.username
            password = self.parsed_url.password
                       
            self.sftpconnector = self.pysftpref.Connection(host, username = username, password = password, port = port)
            self.sftpconnector.timeout = self.timeout
            
            # Compute size of file
            self.remotepath = self.org_file_name
            if self.remotedir:
                self.sftpconnector.cwd(self.remotedir)
                self.remotepath = os.path.join(self.remotedir , self.remotepath)
            self.connectionactive = True
            
            
            # raise exception if file size cannot be determined as unreliable download
            self.size_of_file_to_download = self.sftpconnector.stat(self.remotepath).st_size
            
            if self.size_of_file_to_download == 0:
                raise Exception( " Aborting, as not able to determine length of the content to be downloaded for url {0}", self.resourceurl)

        except:
            raise

    def disconnect(self):

        """ This method tries to stop all connections which were created while trying to download an SFTP resource """

        try:
            self.sftpconnector.close()
            self.connectionactive = False
        except:
            raise

    def abortdownload(self):
        
        """ This method tries to stop any active SFTP connections created and delete the  downloaded SFTP resource """

        try:
            self.disconnect()
        except:
            raise
        finally:
            self.delete_file()

    def set_port_from_config(self):

        """ Sets the default port to be used for downloading SFTP file """    

        try:
            if self.configparser:
                ports = self.configparser['ports']
                port = ports.get(self.protocol, 22)
                self.port = int(port)
            else:
                self.port = 22
        except:
            self.port = 22 
            # default set to continue process


    def download_resource(self, resourceidx):

        """ 
            This method tries to download a SFTP resource attached with the class.
            In case of partial download tries to delete the file downloaded 
        """

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
            raise

    



