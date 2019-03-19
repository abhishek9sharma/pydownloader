import sys
from resourcedownloader.processor.mainprocessor import DownloadsProcessor
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url_file', required =True, type = argparse.FileType('r', encoding='UTF-8'), default=sys.stdin,
                        help='File containing urls')
    parser.add_argument('-d', '--download_folder', required=True,
                        help='Directory containing downloaded filesdr ')

    args = parser.parse_args()
    return args

#urls = [
 #       'ftp://speedtest:speedtest@ftp.otenet.gr/test1Mb.db',
  #      'http://speedtest.ftp.otenet.gr/files/test1Mb.db',
  #      'sftp://demo-user:demo-user@demo.wftpserver.com:2222/download/manual_en.pdf'
        #'ftp://speedtest:speedtest@ftp.otenet.gr/test1Mb.db',
        #'http://speedtest.ftp.otenet.gr/files/test100k.db',
        #'http://speedtest.ftp.otenet.gr/files/test10Mb.db',
        #'sftp://demo:password@test.rebex.net:22/readme.txt'
 #       ]

#download_dir = 'F:\AgodaTest\\'

def main(): 
   args = parse_args()
   url_file = args.url_file
   url_list = [u.strip() for u in url_file.readlines()]
   #with open(url_file, 'r') as f:
   #        urllist.append(str(f.readline()).strip())

   download_dir = args.download_folder
   if not os.path.isdir(download_dir):
        raise argparse.ArgumentTypeError("{0} is not a directory".format(download_dir))
   downloadmodule = DownloadsProcessor(url_list, download_dir)
   downloadmodule.download_resources()

if __name__ == '__main__':
        try:
                main()
        except Exception as e:
                print(e)
