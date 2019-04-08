# Setup Guide

## Setting Up the WebApp: cruzmail/~

### Resetting Database Migrations

Remove any previous migrations (files in /migrations/ besides _init__.py):
```
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
```

Drop the database:
```
$ sudo mysql -u root -p < cruzmail_db.sql
```

Create new migrations:
```
python manage.py makemigrations
python manage.py migrate
```

### Testing the WebApp
```
python3 manage.py runserver <server-ip>:<port>
```



## Setting Up the Database: db_build.sql

### Prerequisites
* UNIX based server environment

### Installing the MySQL Environment

Install the MySQL server using the package installer:
```
$ sudo apt-get update
$ sudo apt-get install mysql-server
$ sudo mysql_secure_installation
```

Allow remote access:
```
$ sudo ufw allow mysql
```

Start the MySQL service and enable it to launch at reboot:
```
$ sudo systemctl start mysql
$ sudo systemctl enable mysql
```

Start the MySQL shell:
```
$ sudo mysql -u root -p
```

### Creating the Database

Download cruzmail_db.sql. Change directory to its location and run:
```
$ sudo mysql -u root -p < cruzmail_db.sql
```