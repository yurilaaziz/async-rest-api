# Description
A human asynchronous framework based on celery.

*Note*:

This project starts to be a quick project built as an example for Asynchronous REST API with celery.
This purpose of this project is to explain how to step by step design a cloud-native application.
Mediums posts will follow.



# Get started 

## Install 
```
git clone http://github.com/yurilaaziz/barberousse.git

```

## Run the celery worker 
````commandline
celery -A barberousse.worker worker -l debug -Q tasks -n tasks
 
````

## Run the gateway
```
python entry.py

```
## Run the gateway using gunicorn 
```
gunicorn barberousse:app

```

