# DivictusInterface
#### The Interface was programmed to be used by Divictus Gaming but was a pro bono project and as such is open-source.

```
The Interface allows the staff of the Minecraft Network to:
- Monitor server status
- Players online/ All players who have BEEN online
- Player profile - when and where last seen, mute histories, ban histories, report histories
- Player chat logs
- Server chat logs
- Live chat for each server
- Notes about players - allows the staff to leave notes about the players which other staff members can see
- Reports - allows players to report others which alerts the online staff and adds the report to their profile
- Privacy permissions - hiding private player messages from staff in the logs unless they are permitted to see them
- AND MORE
```

![Index Page if logged in](https://i.imgur.com/1kUBxVB.png)

![Player Page](https://i.imgur.com/Wm41Xol.png)

![Ban History](https://i.imgur.com/AyGT32i.png)

![Reports Page](https://i.imgur.com/9w7XLFd.png)

![Chat logs Page](https://i.imgur.com/LLc4ScL.png)

### Configuration

The Interface works with Litebans.

You must create a file called secret.py in the same directory as the settings.py file.


In it, you must add your Django Secret Key and the config for the Litebans database.
```
SECRET_KEY = 'yoursecretkey'

litebansconfig = {
  'user': 'user',
  'password': 'pass',
  'host': '127.0.0.1',
  'port': 3306,
  'database': 'litebans',
  'raise_on_warnings': True
}
```
Where you can generate your own secret key to use for encrypting passwords, etc. using
```
python -c "import secrets; print(secrets.token_urlsafe())"
```

As the settings are currently the interface would use SQLite.

If you want to use MySQL replace 
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
with 
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PASSWORD',
        'HOST': 'localhost', 
        'PORT': '3306',
    }
}
```

The interface requires two Redis instances (could technically use only one with 2 databases - but currently configured for two)

One of them has to be running on port 6379 and the other one on port 6380.

It is really easy to spin them in docker containers for under a minute using
```
sudo docker run --name redisforinterfacetickets -p 6380:6379 -d redis
sudo docker run --name redisforinterfacechannels -p 6379:6379 -d redis
```

And later you can start them again using
```
sudo docker start redisforinterfacetickets 
sudo docker start redisforinterfacechannels 
```

One of the Redis instances is used by the Django channels while the other is used by my ticket system which allows only one WebSocket to be opened per server.

### Install all the required packages
The interface has been tested on python versions 3.6 and 3.9.

Before using it you have to install all required packages. You can do that using
```
pip3 install -r requirments.txt
```
Then if you want to run the server in development mode you can do
```
python3 manage.py runserver
```

### Interface Configuration

There needs to exist a superuser account that should be able to access /admin/.

STAFF MEMBERS SHOULD NOT BE ABLE TO ACCESS /admin/ ONLY THE INTERFACE MANAGER SHOULD BE ABLE TO DO THAT.

Create a superuser using:


```
python manage.py createsuperuser
```

The superuser is used to create accounts for other staff members from the admin page which looks like that

![Admin page](https://i.imgur.com/CSQJ2XM.png)

For each staff member, there should exist one user and one **player**.
The **player** is connected to the user. The user is used for login.

Now you should create these permissions in the permissions section:

![Permissions: mute, ban, readprivmessages, administrator](https://i.imgur.com/4Kea3Jn.png)

KEEP THE NAMES OF THE PERMISSIONS AS THAT

Then you can create some roles like Admin, Helper, etc.

The Permission **readprivmessages** allows staff members to read private in-game messages in live chat and chat logs.


From the panel, the administrator can create/generate a new server-client instance.

It is recommended you DO NOT create a Player instance for the superuser account.

#### The Interface works with Defender
It blocks IPs and Accounts after 5 wrong login attempts.

You can change in `settings.py` after how many wrong attempts IPs and Accounts should be blocked
```
DEFENDER_LOGIN_FAILURE_LIMIT = 5
```
If the interface is behind a reverse proxy you should change `DEFENDER_BEHIND_REVERSE_PROXY`
```
DEFENDER_BEHIND_REVERSE_PROXY = True
```
If you want to lockout only IP addresses and not usernames do
```
DEFENDER_DISABLE_USERNAME_LOCKOUT = True
```

#### PRODUCTION
You shouldn't make the interface available to the internet as it is currently set up.
You should disable debug mode and config it with **Nginx** and **daphne**.

Disable debug mode in `DivictusInterface/settings.py`
```
DEBUG = False
```
Starting the interface up with daphne is as easy as 
```
daphne DivictusInterface.asgi:application
```
Django however does NOT server static files by default. That is why I have added whitenoise to the project with handles that so you don't need to configure and use Nginx.

**This should be all you need to do to use the interface in production.**



## THE INTERFACE USES A MINECRAFT PLUGIN TO CONNECT TO ALL THE SERVERS IN THE NETWORK
The repo to the plugin is [Interface Plugin](https://github.com/ysanatomic/divictus-interface-plugin "Interface Plugin").

There you can find more information about in-game commands and plugin configs.



