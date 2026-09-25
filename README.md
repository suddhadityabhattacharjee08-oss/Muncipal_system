# Public Service Management System

A simple Python and MySQL based Public Service Management System for a college computer project.

## Modules
- Municipal System
- Medical System
- Financial System

## Requirements
- Python 3
- MySQL Server
- mysql-connector-python

## Setup

1. Install the Python dependency:
   `pip install -r requirements.txt`

2. Open MySQL Workbench or the MySQL command line.

3. Run `database_setup.sql`.

4. Open `main.py` and change `MYSQL_PASSWORD` if your MySQL root account has a password.

5. Run:
   `python main.py`

## Notes
The project uses three databases so each module keeps its tables separate. The program uses parameterized SQL queries for user-entered values.

Author: Suddhaditya Bhattacharjee
