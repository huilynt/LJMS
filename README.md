# Learning Journey Planning System
https://github.com/huilynt/LJMS

By G3T3

## Installation

### Frontend (ReactJS)
In the root folder,


```
npm install # For first time installation of packages
npm start # Run the project
```

### Backend (Flask)
Please start your DB first. We use WAMP with MySQL.

Place LMS RawData folder in "C:/wamp64/tmp" folder
* E.g. "C:/wamp64/tmp/RawData/courses.csv"

Import these files into your DB in order:
1. LJPS_Tables.sql
2. LJPS_Data.sql

```
pip install -r requirements.txt # For first time installation of modules
cd api
flask run
```
