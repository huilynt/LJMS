# Learning Journey Planning System
https://github.com/huilynt/LJMS

By G3T3

## Installation

## Access to database

Our MySQL databases are managed by phpMyAdmin. In order to create and populate the databases:

    1. Place LMS RawData folder in "C:/wamp64/tmp" folder
        * E.g. "C:/wamp64/tmp/RawData/courses.csv"

    2. Launch WAMP/MAMP server and access phpMyAdmin through this URL http://localhost/phpmyadmin/

      1. Login credentials for Windows users

         Username: root<br>
         No password required<br>

      2. Login credentials for MacOS users

         Username: root<br>
         Password: root<br>

        3. Import these files into your DB in this order:
            1. LJMS_Tables.sql
            2. LJMS_Data.sql

## Frontend (ReactJS)
In the root folder,

```
npm install # For first time installation of packages
npm start # Run the project
```

## Backend (Flask)
Please start your DB first. We use WAMP with MySQL.

```
pip install -r requirements.txt # For first time installation of modules
cd api
flask run
```