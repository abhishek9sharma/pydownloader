A set of scripts to download files using various protocols.

## Steps to run
### All command may require sudo/admin privileges
1. *Python 3* should be installed on the system (the code has been verified on *Python 3.6.3*)
2. Using command line, navigate to the folder *pydownloader*(make sure this folder contains the file *README.md* and folder *resourcedownloader*)

3. Install/Configure a virtual environment as follows from the command line (this step may be skipped but it may cause dependency issues on the system) (If already configured go to Step 4)
    
    a. Installation 
        
        -- Windows  : pip install --user virtualenv
        -- Linux    : python3 -m pip install --user virtualenv
        
    b. Configuration (*testassignment* is the environment name)
        
        i. Create
            -- Windows  : python -m virtualenv testassignment
            -- Linux    : python3 -m virtualenv env 
        
        ii.  Activate 
            -- Windows  : .\testassignment\Scripts\activate
            -- Linux    :  source testassignment/bin/activate 
        
    c. Install dependencies      
          
        -- Windows  : pip install -r requirements.txt
        -- Linux    : pip install -r requirements.txt 
    
 4. Activate environment (*testassignment* is the environment name)
        
        -- Windows  : .\testassignment\Scripts\activate
        -- Linux    :  source testassignment/bin/activate 
        
5. Create a file *resourceurls.txt* in *pydownloader* folder, which should contain the links which are to be downloaded. Currently, *http, ftp, sftp* protocols are supported. Each link should be in different lines. Example shown below
    ```
    ftp://speedtest:speedtest@ftp.otenet.gr/test1Mb.db
    http://speedtest.ftp.otenet.gr/files/test1Mb.db
    sftp://demo-user:demo-user@demo.wftpserver.com:2222/download/manual_en.pdf
    ```

6. From command prompt, run the following command
    
        -- Windows : python run.py -u resourceurls.txt -d <destfolderpath>
        -- Linux   : python3 run.py -u resourceurls.txt -d <destfolderpath>
		
		where destfolderpath is the path of destination folder where files are to be downloaded 
