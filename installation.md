# Installation

This document explains how to deploy the postcodes application to Ubuntu Server

#### Create a folder for the project:

```bash
mkdir postcodes
cd postcodes
```

#### Setup a python virtual environment (venv) with python 3 (version >= 3.6.9)

```
virtualenv venv
source venv/bin/activate
```

#### Install app's dependencies with this virtualenv:

```
pip install dash==1.13.3
pip install gunicorn
pip install pandas
```

#### Copy the files `9722_UBDC_logo.png`, `health_boards.csv` and `pcodes_app.py` to the newly created folder.

#### Run the app with a Production Server

I chose gunicorn. Gunicorn is a WSGI HTTP Server for UNIX. For example, to run the application with 4 worker processes (`-w 4`) binding to localhost port 4000 (`-b 127.0.0.1:4000`):

```bash
gunicorn -w 4 -b 127.0.0.1:4000 pcodes_app:server
```
