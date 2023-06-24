TODO:

 - Complete `AttemptMiddleware` for IP checking

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