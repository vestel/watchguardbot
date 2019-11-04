## WatchGuardBot

# Installation & launching

You might need to install latest Python 3.x version. 
If you are using Ubuntu or Mint, use [DeadSnakes PPA](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa) for that.

    $ sudo add-apt-repository ppa:deadsnakes/ppa
	$ sudo apt update
	$ sudo apt install python3.7 python3.7-dev python3-virtualenv
	
Checkout this repository code:

	$ git clone <URL> ~/Projects/watchguardbot
	
After that create virtual execution runtime in your favourite folder
	
	$ virtualenv --python=`which python3.7` ~/Projects/watchbotenv

Activate it by running 

	$ source ~/Projects/watchbotenv/bin/activate
	(watchbotenv) $ cd ~/Projects/watchguardbot
	
Install project dependences:

	(watchbotenv) $ pip install -r requirements.txt
	
Rename and edit sample settings file:

	(watchbotenv) $ cp dabot/settings.py.example dabot/settings.py
	
Launch bot:

	(watchbotenv) $ cd dabot
	(watchbotenv) $ python source.py
	
