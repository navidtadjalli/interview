# Achare Interview Project

This repository contains codes to achare interview project.

I wrote this project using Django and DjangoRestFramework.
I used sqlite3 as database.

## How to Run Manually

 - First create a virtualenv and activate it

```
python -m venv venv
source venv/bin/activate
```

- Install requirements
```
pip install -r requirements.txt
```

- Migrate migration files
```
python manage.py migrate
```

- Create super-user
```
python manage.py createsuperuser
```
enter phone number and password

now you can run the project with the following command
```
python manage.py runserver 0.0.0.0:8000
```
`0.0.0.0` because project get visible through network 

## How to Run with Docker
Build docker image
```
docker build -t achare_project .
```

Run docker image with following command
```
docker run -p 8000:8000 -t achare_project
```

## Excuses
I did not write test cases for CustomerManager because I just copied it from the original manager and just removed username from it.

I did not write test cases for parts of code that I was sure were copied from else where in the project and were fully tested in the original place. 