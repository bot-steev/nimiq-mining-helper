# nimiq-mining-helper

## Requirements

- [Python 3](https://www.python.org/download/releases/3.0/)
- [Discord.py](https://github.com/Rapptz/discord.py)
- [PyPi](https://pypi.org/)
- [libCloud](https://libcloud.apache.org/)
- [PyCrypto](https://pypi.org/project/pycrypto/)
- [Discord Developer App][1]
- [Owner of a server in the Discord Application](https://discordapp.com)
- GCE Service Account as described in Telegram.

## Installation Instructions for Ubuntu 16.04 LTS
### Step 1
Create a snapshot of a 16-core server with all of its startup scripts and stuff.

### Step 2
Nuke the 16-core instance and create a pre-emtible 14-core as well as a dedicated 1-core with the snapshot from Step 1.

### Step 3
SSH into the 14-core and ensure your startup scripts worked properly, then SSH into the 1-core (from now on reffered to as the hosting server) and disable all the startup scripts.

### Step 4
Your 1-core should already have python3 configured due to the miner installation, to check use:
```
whereis python3
```
And verify that you have a path to `/usr/bin/python3` or `/usr/bin/python3.5`

### Step 5
Next we install [PyPi](https://pypi.org/),
```
sudo apt-get install python3-pip
```

Followed by the [Discord.py](https://github.com/Rapptz/discord.py) package:
```
pip3 install discord.py
```

Next the [libCloud](https://libcloud.apache.org/) package:
```
pip3 install apache-libcloud
```

Finally we get the [PyCrypto](https://pypi.org/project/pycrypto/) package:
```
pip3 install pycrypto
```

### Step 6
Next we get the latest version of the Nimiq Mining Helper:
```
git clone https://github.com/bot-steev/nimiq-mining-helper.git
```

### Step 7
Go into the directory that you just downloaded:
```
cd nimiq-mining-helper/
```

### Step 8
Make a new directory named src:
```
mkdir src
```

### Step 9 
Move the database template into the src folder and rename it with the following command:
```
mv miner_info_db_template.sqlite /src/miner_info_db.sqlite
```

### Step 10
Go into the src folder:
```
cd src
```

### Step 11
Create a new file called key.txt:
```
touch key.txt
```

### Step 12
Follow the [Discord Developer App][1] link and create a new App called Niminq Mining Helper

### Step 13
After the app has been created successfully scroll down and enable the `Bot Account` section. When the bot account has been made, next to Token, click `click to reveal` and copy this token.

### Step 14
Go back to your server and open the key.txt file and paste the key:
```
nano key.txt
ctrl + V
ctrl + X
shitf + Y
Enter
```
### Step 15
Now change back to the main directory and start up the bot:
```
cd ..
python3 nimiq_v01_BETA.py
```

Should the bot start correctly, a block of text will appear in the terminal screen, of which a part will look like the following:
```
Use this link to invite nimiq-mining-helper:
https://discordapp.com
```

Follow this link to be taken to a screen where it will ask you to which server you would like to add the bot. Select your one from the drop-down menu and continue.

That Concludes the section for getting the bot up and hosted on your own instance, the section below will describe setting up the Database for the bot actually be able to check your servers.

## Bot Database Setup

Please see the table below for the bot commands available at this time:
```
| Command                                  | Description                                                |
|------------------------------------------|------------------------------------------------------------|
| !accountinfo                             | Lists all Service Accounts from the service_account Table. |
| !addaccount [account'] [JSON FilePath^]  | Add a new Service Account to the service_account Table.    |
| !deleteaccount [account']                | Delete a Service Account from the service_account Table.   |
| !projectinfo                             | Lists all Projects from the project_info Table.            |
| !addproject [projectID*] [projectAlias*] | Add a new Project to the project_info Table.               |
| !deleteproject [projectID*]              | Delete a Project from the project_info Table.              |
| !cleardb                                 | Delete everything from both Tables.                        |
| !check                                   | Start Hartbeat check that will run every 2 minutes.        |
```
### Table Key Notes

```
N.B. - > Do not include the [] brackets !!!
'account - Your service account email address from the Cloud Console.
^JSON FilePath - Please ensure that the file path you put in the db matches exactly.
*ProjectID - Copy it exactly as displayed on your Google Cloud Console.
*ProjectAlias - An easy to remember name for your project, use _ or - but no spaces.
```

Below is an example setup:

![ExampleImage](https://i.imgur.com/KC7rxUC.png)

## The Grand Finale

Now you can switch to your discord app and in your channel of choice start the heartbeat:
```
!check
```

I think that just about covers it, but if you have any questions feel free to DM me on discord at `steev0#0420`.

Tips are appreciated :

![NIM](https://i.imgur.com/W3ztF49.png) `NIM: NQ49 HTNJ L51H SVQ5 6QCD 6LY1 1L8P XGEE LBCF`
 
### P.S.

In order for the bot to keep running when you close the SSH window follow below:

Once the bot has been tested and working, cancel the process in your SSH session
```
ctrl+c
```

Then restart the bot using the following command:
```
nohup python3 nimiq_v01_BETA.py.py &
```

[1]: https://discordapp.com/developers/applications/me