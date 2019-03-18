from configparser import ConfigParser

config = ConfigParser()
config['protocol_selector'] ={
    'http':'HTTPDownloader',
    'https': 'HTTPDownloader',
    'ftp': 'FTPDownloader',
    'sftp': 'SFTPDownloader'
}

config['ports']={
'http' :'0',
'ftp':'0',
'sftp':'22',
}

config['chunksizes']={
'http:' :'1024',
'ftp':'1024',
'sftp':'1024',
}


config['threading']={
'noofthreads' :'3'
}

#config['timestampformat']={'format':'%Y%m%d__%H%M%S'}

with open('./config.ini','w') as configfile:
    config.write(configfile)