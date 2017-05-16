# Welcome to balance_sheeter!
This is the ReadMe file for BalanceSheet. This will help you in Getting Started with the project.

## Installation
balance_sheeter is built using Python, Django and postgresql so you will need to have python, django and postgresql setup in your system.

#### Clone the repo

    git clone git@github.com:himani2707/balance_sheeter.git
    
    cd balance_sheeter
    
#### Set up postgresql

Follow the installation instructions mentioned [here](https://wiki.postgresql.org/wiki/Detailed_installation_guides).
    
    createuser Himani --createdb
    
    createdb django_test --owner Himani

    Alternatively you can edit the settings file located at (balance_sheeter/config/settings.py) and change your database settings accordingly.
    
NOTE: If you get `FATAL: Peer authentication failed for user "<username>"
` follow the solution [here](http://stackoverflow.com/a/18664239/6582734).

#### Install the dependencies

    pip install -r requirements.txt
    
#### Install JDK
 
    Java version 1.8.0_131

#### Run the migrations

    python manage.py migrate

#### Start the server

    python manage.py runserver

    
## Running The Project

    Once you are done with all the settings and configurations, please run python manage.py runserver and this will run a local django server on your
    machine. Open your browser and navigate to 127.0.0.1:8000/monsoon/home or http://localhost:8000/monsoon/home and you be seeing the home screen where
    you can post queries.


## API details

##### Request type: GET URL: http://localhost:8000/monsoon/home
    Home page

##### Request type: POST URL: http://localhost:8000/monsoon/save-and-return
    POST params: variable name (as in the balance sheet), year, balance-sheet.pdf

##### Request type: GET URL: http://localhost:8000/monsoon/results
    Returns value corresponding to the query and a link to download csv file

##### Request type: GET URL: http://localhost:8000/monsoon/results
    Downloads the csv file
