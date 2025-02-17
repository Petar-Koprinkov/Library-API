# 🏛️ Library API

### A DjangoRest Web Application that allows you to manage a library. Users can register, log in, log out, get all books, create book, get a current book, edit it and delete it.


## General Requirements
- **Python**: Version 3.11.1 or higher  
- **PostgreSQL**: Database
- **pip**: For installing dependencies  
- **Browser**: Developed and tested using Microsoft Edge, Internet Explorer and Chrome. A Chromium-based browser is recommended but others probably work as well.
- **GIT**: Alternatively you can just download the source code.
- **Python Virtual Environment**: Optional, but recommended
---

## Setup Instructions

### Step 1: Clone the project
```bash
git clone https://github.com/Petar-Koprinkov/Library-API
```
And navigate to the root directory (`manage.py` level)
 ```bash
cd Library-API
```

### Step 2: Install Dependencies


Run the following command to install required Python libraries:
```bash
pip install -r requirements.txt
```

### Step 3: Database Migration
Run the following command to apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Run the app
Use this command to run the app:
```bash
python manage.py runserver
```

### Step 4: Run the tests
Use this command to run the app:
```bash
python manage.py test
```


---

## You can access the application with all its functionalities LOCALLY at http://localhost:8000/
