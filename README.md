
# To Run this project follow these steps
## Overview

This project is a Library Management System (LMS) built with Django. It allows users to manage book inventories, issue books, and handle user registrations and logins.

## Prerequisites

Python 3.8 or higher

Django 4.x

PostgreSQL (or another database if configured)

pip (Python package manager)


if you want to use virtual environment  if not skip {
-
virtual Environment Setup Guide
Virtual environments allow you to create isolated Python environments for your projects, ensuring that dependencies are managed separately for each project.

## 1. Installation

* ## Windows

#### Install Python:

Ensure Python is installed and added to your system PATH. Download from python.org if needed.

#### i. Install Virtualenv:
Open Command Prompt or PowerShell and run :

```bash
 pip install virtualenv
```

#### ii. Create a Virtual Environment : 
```
python -m venv venv
```

### Activate the Virtual Environment:

Command Prompt : 
```
venv\Scripts\activate
```

PowerShell : 
```
venv\Scripts\Activate.ps1
```



* ## macOS and Linux
  


Python should be pre-installed. Verify with :
```   
python3 --version
```   
Install Virtualenv :

 ````
 pip install virtualenv
 ````


Create a Virtual Environment:

Using venv:

```
python3 -m venv venv
```

Using virtualenv :
```   
virtualenv venv
```
### 2. Activate the Virtual Environment : 

```
source venv/bin/activate
```
}
-




# Setup and Installation
```
1. Clone the Repository :

     git clone https://github.com/yourusername/your-repository-name.git
      cd your-repository-name

2. Install Dependencies

     pip install -r requirements.txt



3. Configure Settings
     update the settings.py file with your database and other configuration settings.

     For MySQL, update the DATABASES section in settings.py:

     DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '3306',
          }
      }
   


 4. Apply Migrations
      python manage.py makemigrations
      python manage.py migrate



5. Create a Superuser
      python manage.py createsuperuser



6. Collect Static Files
     python manage.py collectstatic


7. Run the Development Server
      python manage.py runserver
      
```

