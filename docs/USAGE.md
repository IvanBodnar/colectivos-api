
##### Run command general form:
`
$ docker-compose run app sh -c "<command>"
`

### **Steps**

#### Start a virtualenv on project root and install the dependencies (optional):
`$ python3.7 -m venv venv`  
`$ source venv/bin/activate`
`$ pip install -r requirements.txt`

#### Start django project
`
$ docker-compose run app sh -c "django-admin.py startproject <project name> ."
`

#### Add postgres configuration data to settings.py  
```python
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST', None),
        'NAME': os.environ.get('POSTGRES_DB', None),
        'USER': os.environ.get('POSTGRES_USER', None),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', None),
    }
}
```

#### Set environment variables on container

- Put the env variables on vars.env file
SECRET_KEY=\<SECRET KEY> (no quotes)

```bash
# app
SECRET_KEY=c&wnyx1t^@mo&+356&&b&^^*g381m$1!1zceupbe%b14u5rjl9
DB_HOST=db

# db
POSTGRES_DB=app
POSTGRES_USER=user
POSTGRES_PASSWORD=pass
```
A database and user with the specified password will be created on the postgres container.
- Run docker-compose up  
`
$ docker-compose up
`
- Alternatively, the image can be built first, and then the container can be run
with the env file passed:  
`
$ doc run -itd --env-file ./vars.env 80d
`

#### Start django app
`
$ docker-compose run app sh -c "python manage.py startapp <app name>"
`