# DivictusInterface
#### The Interface was programmed to be used by the Minecraft Network *Divictus Gaming* but was a pro bono project and as such is opensource.
```
The Interface allows the staff of the Minecraft Network to: 
- Monitor server status
- Players online / All players who have BEEN online
- Player profile - when and where last seen, mute histories, ban histories, report histories
- Player chat logs
- Server chat logs
- Live chat for each server.
- Notes about players - allows the staff to leave notes about the players which other staff members can see
- Reports - allows players to report others which alerts the online staff and adds the report to their profile
- Privacy permissions - hiding private player messages from staff in the logs unless they are permitted to see them.
- AND MORE
```
It is made to be used on networks but it could also be used on a single server.


![Index Page if logged in](https://i.imgur.com/1kUBxVB.png)

![Player Page](https://i.imgur.com/Wm41Xol.png)

![Ban History](https://i.imgur.com/AyGT32i.png)

![Reports Page](https://i.imgur.com/9w7XLFd.png)

![Chat logs Page](https://i.imgur.com/LLc4ScL.png)

The Interface works with Litebans.

You must create a file called secret.py in the same directory as the settings.py file.

In it you must add your django Secret Key and the config for the Litebans database.
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
Where you can generate your own secret key to use for encrypting passwords and etc. using
```
python -c "import secrets; print(secrets.token_urlsafe())"
```

As the settings are currently the interface would use sqlite.

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

The interface requires two redis instances (could technically use only one with 2 databases - but currently configured for two)

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

One of the redis instances is used by the django channels while the other is used by my ticket system which allows only one websocket to be opened per server.

There needs to exist a superuser account that should be able to access /admin/.

STAFF MEMBERS SHOULD NOT BE ABLE TO ACCESS /admin/ ONLY THE INTERFACE MANAGER SHOULD BE ABLE TO DO THAT.

Create a superuser using:


```
python manage.py createsuperuser
```

The superuser is used to create accounts for other staff members from the admin page which looks like that

![Admin page](https://i.imgur.com/CSQJ2XM.png)

For each staff member there should exists one user and one **player**.
The **player** is connected to the user. The user is used for login.

Now you should create these permissions in the permissions section:

![Permissions: mute, ban, readprivmessages, administrator](https://i.imgur.com/4Kea3Jn.png)

KEEP THE NAMES OF THE PERMISSIONS AS THAT

Then you can create some roles like Admin, Helper, etc.

The Permission **readprivmessages** allows staff members to read private in-game messages in live chat and chat logs.


From the panel the administrator can create/generate a  new server client instance.

It is recommended you DO NOT create a Player instance for the superuser account.

The Interface works with Defender -> it blocks IPs and Accounts after 5 wrong login attempts.


## THE INTERFACE USES A MINECRAFT PLUGIN TO CONNECT TO ALL THE SERVERS IN THE NETWORK
The repo to the plugin is [Interface Plugin](https://github.com/ysanatomic/divictus-interface-plugin "Interface Plugin").

There you can find more information about in-game commands and plugin configs.



