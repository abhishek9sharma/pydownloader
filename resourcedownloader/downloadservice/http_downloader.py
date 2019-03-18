from resourcedownloader.downloadservice.resource_downloader import BaseDownloader
import os
import  requests


#TODO:     # Check for size compute failure in connect method line 20
#TODO:     # connection timeout configurable line 17 Also find and optimum value
#TODO:     # Network error such as wifi Temp Dir and Cleanup a possible way
#TODO : Remove commented Code

class HTTPDownloader(BaseDownloader):
    
    def __init__(self, resourceurl, path_download_dir):
        super().__init__(resourceurl, path_download_dir)
        self.response = None

    def connect(self):
        try:

            self.response = requests.get(self.resourceurl, stream=True, timeout=60)
            self.response.raise_for_status()
            self.size_of_file_to_download = int(self.response.headers.get('content-length', ))
            self.connectionactive = True
            if self.size_of_file_to_download == 0:
                # Not sure if this is actually required except for tracking progress
                raise Exception( " Not Able to determine length of the content to be downloaded for url {0}", self.resourceurl)
            
        except:
            raise



    def disconnect(self):
        try:
            if self.response:
                self.response.close()
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

    def download_resource(self, resourceidx, config_path ='Config/config.ini'):
        try:
            super().download_resource(resourceidx, config_path)
            self.connect()
            with open(self.path_downloaded_file, 'wb') as f:
                    for current_chunk in self.response.iter_content(chunk_size = self.chunksize):
                        if current_chunk:
                            self.size_of_file_downloaded += f.write(current_chunk)

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




  
    
    


