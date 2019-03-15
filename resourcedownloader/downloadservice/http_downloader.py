from resourcedownloader.downloadservice.resource_downloader import BaseDownloader
import os
import  requests

class HTTPDownloader(BaseDownloader):
    
    def __init__(self, resourceurl, path_download_dir):
        super().__init__(resourceurl, path_download_dir)
        self._response = None
        self._chunksize = 1024

    def connect(self):
        try:
            self._response = requests.get(self._resourceurl, stream=True)
            self._response.raise_for_status()
            self._size_of_file_to_download= self._response.headers['content_length']
        except :
            pass

    def disconnect(self):
        if self._response:
            self._response.close()

    def abortdownload(self):
        try:
            self.delete_file()
            self.disconnect()
        except:
            pass



    def download_resource(self):
        try:
            self.set_download_file_path()
            self.connect()
            #with requests.get(url= self._resourceurl, stream = True) as response:
            with open(self._path_downloaded_file, 'wb') as f:
                for current_chunk in self._response.iter_content(chunk_size = self._chunksize):
                    if current_chunk:
                        self._size_of_file_downloaded +=len(current_chunk)
                        f.write(current_chunk)
            self.disconnect()
        except Exception as e:
            print(e, " abort download ")
            self.abortdownload()



  
    
    



