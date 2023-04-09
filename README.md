### Setup
    Download the files from repository

    Change the directory to the folder where you downloaded files

    Create Python virtual environment
    python3.10 -m venv venv
    For installing required packages, execute the following command in terminal:

    pip install -r plugins.txt

    After successful installation execute the following commands:
    
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

### Docker

    docker build -t sport-league .
    docker run -it -p 8080:8000 -e DJANGO_SUPERUSER_USERNAME=admin  -e DJANGO_SUPERUSER_PASSWORD=admin123123  -e DJANGO_SUPERUSER_EMAIL=admin@admin.com  sport-league

### Django Admin 
    http://127.0.0.1:8000/admin
    email: admin@admin.com
    password: admin123123
    
    Ranking List View
    http://127.0.0.1:8000/team/
    
    Sample CSV Data
    http://127.0.0.1:8000/static/sample.csv

    List View
    http://127.0.0.1:8000/team/ranking-list/

    Ranking Add View
    http://127.0.0.1:8000/team/add-ranking/
    

### Login and Registration API

    Login:
    http://127.0.0.1:8000/account/login-api/

    POST request: 
        {
        "email":"admin@admin.com",
        "password":"admin123123"
        }
    
    Registration:
    http://127.0.0.1:8000/account/register/

    POST Request:
        {
        "username":"emarn6",
        "email":"emarn6@admin.com",
        "password":"admin123"
        }
