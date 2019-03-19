# Description
A package (set of scripts) to download files using various network protocols.

## Steps to run
### All commands may require sudo/admin privileges
1. *Python 3* should be installed on the system (the code has been verified on *Python 3.6.3*)
2. Using command line, navigate to the folder *pydownloader*(make sure this folder contains the file *README.md* and folder *resourcedownloader*)

3. Install/Configure a virtual environment as follows from the command line (this step may be skipped but it may cause dependency issues on the system) (If already configured go to Step 4)
    
    a. Installation 
        
        -- Windows  : pip install --user virtualenv
        -- Linux    : python3 -m pip install --user virtualenv
        
    b. Configuration (*testassignment* is the environment name)
        
        i. Create
            -- Windows  : python -m virtualenv testassignment
            -- Linux    : python3 -m virtualenv testassignment 
        
        ii.  Activate 
            -- Windows  : .\testassignment\Scripts\activate
            -- Linux    :  source testassignment/bin/activate 
        
    c. Install dependencies      
          
        -- Windows  : pip install -r requirements.txt
        -- Linux    : pip install -r requirements.txt 
    
 4. **Ignore this step if coming from Step 3** else continue to *Activate virtual environment* (*testassignment* is the environment name)
        
        -- Windows  : .\testassignment\Scripts\activate
        -- Linux    :  source testassignment/bin/activate 
        
5. Create a file *resourceurls.txt* in *pydownloader* folder, which should contain the links which are to be downloaded. Currently, *http, https, ftp, sftp* protocols are supported. Each link should be in different lines. Example shown below
    ```
    http://speedtest.tele2.net/1MB.zip
    ftp://speedtest.tele2.net/10MB.zip
    sftp://demo-user:demo-user@demo.wftpserver.com:2222/download/manual_en.pdf
    https://www.python.org/static/community_logos/python-logo-master-v3-TM.png
    ```

6. From command prompt, run the following command
    
        -- Windows : python run.py -u resourceurls.txt -d <destfolderpath>
        -- Linux   : python3 run.py -u resourceurls.txt -d <destfolderpath>
		
		where destfolderpath is the path of destination folder where files are to be downloaded 

7. The execution trace logs are generated in the Folder below
        
        -- pydownloader/resourcedownloader/Logs 

8. In order to execute the testcases run the following command from command prompt. Before this please make sure to *activate* the *virtual environments* as         shown in *Step 3* or *Step 4*
    
        -- Windows  : pytest
        -- Linux    : pytest

