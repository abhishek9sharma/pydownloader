from resourcedownloader.downloadservice.resource_downloader import BaseDownloader
import os
import  requests

class HTTPDownloader(BaseDownloader):
    
    def __init__(self, resourceurl, path_download_dir):
        super().__init__(resourceurl, path_download_dir)
        self.response = None

    def connect(self):
        try:
            self.response = requests.get(self.resourceurl, stream=True)
            self.response.raise_for_status()
            self.size_of_file_to_download = int(self.response.headers.get('content-length', 0))
            if self.size_of_file_to_download == 0:
                # Not sure if this is actually required except for tracking progress
                raise Exception( " Not Able to determine length of the content to be downloaded for url {0}", self.resourceurl)
        except:
            raise



    def disconnect(self):
        if self.response:
            self.response.close()

    def abortdownload(self):
        try:
            self.disconnect()
            self.delete_file()
        except:
            pass

    def download_resource(self):
        try:
            super().download_resource()
            self.connect()
            with open(self.path_downloaded_file, 'wb') as f:
                    for current_chunk in self.response.iter_content(chunk_size = self.chunksize):
                        if current_chunk:
                            self.size_of_file_downloaded += f.write(current_chunk)

            self.disconnect()
        except Exception as e:
            #print(e, " aborting download for {0} due to some exception while downloading", self.resourceurl)
            self.abortdownload()
            raise




  
    
    


