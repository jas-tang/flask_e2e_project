# flask_e2e_project
This is a repository for the Final Assignment (Product / Web Service) for HHA504/507

For this project, the intention was to build an application that displays data from a datasource. I used data from my mindlamp project, see more [here](https://github.com/jas-tang/AHI_mindLAMP). 

We used Github for version control. We used Flask-Python to build the application for both front and and backend with various routes. We also used MySQL, with is databse on Azure. We used SQL Alchemy to connect to the database. We used .env to hide our credentials. We used tailwind and css to customize our HTML files. We used Google OAuth for security and storing user log in information onto a database. We used Sentry.io as a logger and debugging tool. We used Docker to contain our application. 

## Demo
https://github.com/jas-tang/flask_e2e_project/assets/141374136/d9ca50cd-7f8b-4c62-91ce-bb9037f71711

## Quickstart
To run locally, insert credentials onto environment. Run app.py within the app folder.

To run with docker, use docker-compose up --build

## Imports
```python
from flask import Flask, render_template, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
import sentry_sdk
from db_functions import update_or_create_user
```

## Environment
DB_USERNAME=
DB_PASSWORD=
DB_HOST=
DB_NAME=
GOOGLE_CLIENT_ID = 
GOOGLE_CLIENT_SECRET = 

## The Datasource

My data source comes from a sql server on azure. It is on an Azure database for MySQL flexible server. Following the instructions on this github [repository](https://github.com/jas-tang/mysql_cloudmanaged_databases), I was able to set up my server. 

This is what my server looked like.
![](https://github.com/jas-tang/mysql_cloudmanaged_databases/blob/main/images/azure3.png)

I launched mysqlworkbench to import my data, which was in a CSV format. Using the importing wizard, I was able to transfer my data onto mySQLworkbench. 

![](https://github.com/jas-tang/flask_e2e_project/blob/main/docs/01.JPG)

The data is properly sitting within the server.
![](https://github.com/jas-tang/flask_e2e_project/blob/main/docs/02.JPG)

## Connecting to the data source
In my app.py file, we have to construct the database URL. 

```
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
```
Make sure that your environment file has the proper credentials. We used dotenv and gitignore here to hide our credentials. 

Then, we used pymysql to create the connection 
```python
database_url = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}"
print(database_url)
```
```python
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

## SQLAlchemy
Using sqlalchemy, we can test if there connection to our server works.
```python
engine = create_engine(database_url,
                         connect_args={'ssl': {'ssl-mode': 'preferred'}},
                         )
```
```python
inspector = inspect(engine)
inspector.get_table_names()
```
We properly created the connection. 
![](https://github.com/jas-tang/flask_e2e_project/blob/main/docs/03.jpg)

## Base application
We initialize the database. 
```python
db = SQLAlchemy(app)
```
Then, we have to create a class for our model. This would help the data fit into a mold. 
```python
class lampdata(db.Model):
    __tablename__ = 'lampdata'
    my_row_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.String(10000), nullable=False)
    userNAME = db.Column(db.String(10000), nullable=False)
    ActivityName = db.Column(db.String(10000), nullable=False)
    ActivityDate = db.Column(db.Date, nullable=False) 
    item = db.Column(db.String(10000), nullable=False)
    value = db.Column(db.String(10000), nullable=False)
    type = db.Column(db.String(10000), nullable=False)
```
As a side note, at first, it was only displaying unique User IDs, which left me perplexed. I then swapped the primary key to my_row_id to fix the issue. 

By routing this in an html file, we will be able to see the data. 
```python
@app.route('/mindlamp_data')
def mindlamp_route():
        mindlamp_data = lampdata.query.all()
        return render_template('index.html', lampdata=mindlamp_data)
```

## The HTML
This is my base html that I used for my application. It used tailwind and CDN. 
```HTML
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>mindLAMP AHI</title>
    
    <!-- Tailwind CSS via CDN -->
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>

<body class="bg-gray-200">

    <header class="bg-red-600 text-white p-4">
        <h1 class="text-4xl">mindLAMP Data AHI</h1>
        <nav>
            <ul class="flex space-x-4">
                <li><a href="/home/" class="hover:underline">Home</a></li>
                <li><a href="{{ url_for('mindlamp_route') }}" class="hover:underline">Data</a></li>
            </ul>
        </nav>
    </header>

    <main class="p-4">

        {% block content %}{% endblock %}

    </main>

    <footer class="bg-red-600 text-white p-4 mt-6">
        <p>Check <a href="https://github.com/jas-tang/flask_e2e_project">Github</a> for more information</p>
    </footer>

    <style>
        a:link {
          color: green;
          background-color: transparent;
          text-decoration: none;
        }
        a:visited {
          color: pink;
          background-color: transparent;
          text-decoration: none;
        }
        a:hover {
          color: red;
          background-color: transparent;
          text-decoration: underline;
        }
        a:active {
          color: yellow;
          background-color: transparent;
          text-decoration: underline;
        }
        </style>

</body>

</html>
```
I created a home landing page, as well as the index, which showed the data. Lastly, there is an HTML file for the google oauthentication landing page. 

## Google OAuth
Going this this [site](https://console.cloud.google.com/apis/credentials/consent), we are able to create a consent screen. 
![](https://github.com/jas-tang/flask_e2e_project/blob/main/docs/oauth.JPG)
![](https://github.com/jas-tang/flask_e2e_project/blob/main/docs/oauth2.JPG)

We then have to go to credentials, and manage the credentials. We inputed our flask app's designated port. 
```
Authorized JavaScript Origins = https://8000-cs-xxxxxxxxx-default.cs-us-east1-vpcf.cloudshell.dev
Authorized redirect URIs: https://8000-cs-xxxxxxxx-default.cs-us-east1-vpcf.cloudshell.dev/google/auth/
```

Going back to the app.py, we include some extra code.
```python
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

app.secret_key = os.urandom(12)
oauth = OAuth(app)
```

This code generates a token and redirects the user to the correct URI. 
```python
    # Redirect to google_auth function
    ###note, if running locally on a non-google shell, do not need to override redirect_uri
    ### and can just use url_for as below
    redirect_uri = url_for('google_auth', _external=True)
    print('REDIRECT URL: ', redirect_uri)
    session['nonce'] = generate_token()
    ##, note: if running in google shell, need to override redirect_uri 
    ## to the external web address of the shell, e.g.,
    redirect_uri = 'https://8000-cs-51349017989-default.cs-us-east1-vpcf.cloudshell.dev/google/auth/'
    return oauth.google.authorize_redirect(redirect_uri, nonce=session['nonce'])
```

We then create this function. This function registers the login information to a database. 
```python
@app.route('/google/')
def google():
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
```

Using sqlite3, we can create a database file and store the login credentials within it. This is a separate file called db_functions.py. In our python app.py file, we import update_or_create_user from this file. 
```python
import sqlite3
import os

# Initialize the database
DATABASE = 'users.db'

# Specifying the path
DB_FOLDER = '/home/jason_tang/flask_e2e_project/db'
DATABASE = os.path.join(DB_FOLDER, 'users.db')

def get_db():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            profile TEXT
            permissions TEXT DEFAULT 'basic'
        )
    ''')
    db.commit()
    return db

def update_or_create_user(user_info):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (email, name, profile) VALUES (?, ?, ?)
            ON CONFLICT(email) DO UPDATE SET name = excluded.name, profile = excluded.profile
        ''', (user_info['email'], user_info['name'], user_info['picture']))
        db.commit()
        print("User added to database: ", user_info['email'])
    except Exception as e:
        print(e)
        db.rollback()
```
This code initializes and gets values from the users in a db file. This is a separate file called db_review.py. 
```python
import sqlite3
import pandas as pd

# Initialize the database
DATABASE = '/home/jason_tang/flask_e2e_project/db/users.db'

# search for user in database
db = sqlite3.connect(DATABASE)
cursor = db.cursor()

# get list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

# get values from users table
df = pd.read_sql_query("SELECT * FROM users", db)
df
```

Now, for our landing page, we are making it route to the googleoauth page.
```python
@app.route('/')
def index():
    return render_template('googleoauth.html')
```
The landing page has a sign in button, as well as an image of the mindlamp logo and google logo.

After logging in, the user will be able to properly see the application. Their information is displayed on the app, and they have an option to logout.
```python
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')
```

## Sentry SDK
Using [Sentry IO](https://sentry.io/welcome/?utm_source=google&utm_medium=cpc&utm_id=%7B19655969969%7D&utm_campaign=Google_Search_Brand_NORM_Alpha&utm_content=g&utm_term=sentry.io&gad_source=1&gclid=Cj0KCQiAsvWrBhC0ARIsAO4E6f_qZTOaCt2aw8PMGMX-yNjQnQH4rnt4f92h8BIBmCbMawzdI_xOy0gaAs7UEALw_wcB), we are able to look at our logs. 

From the Sentry IO site, create an account, and then create a python project. It will then give you information to git install, as well as import. They will also provide code to paste into yours.
```python
##SDK Sentry
sentry_sdk.init(
    dsn="",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)
```
```python
sentry_sdk.init(
    dsn="insert your dsn here"
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)
```

Now, we can edit our code to try and except. 
```python
@app.route('/mindlamp_data')
def mindlamp_route():
    try: 
        mindlamp_data = lampdata.query.all()
        return render_template('index.html', lampdata=mindlamp_data)
    except Exception as e:
        raise Exception (f'Something went wrong: {e}')
```
If an issue were to occur, we would see the issue on Sentry IO. 
![](https://github.com/jas-tang/flask_e2e_project/blob/main/docs/sentrysdk.JPG)
![](https://github.com/jas-tang/flask_e2e_project/blob/main/docs/sentrysdk2.JPG)

## Additional Filter Function
This code created a filter button to go through my data.
This was done by querying all the lamp data, and then storing it in a variable. This would display all the data. 
The next function would filter by user ids. 
```python
@app.route('/filter', methods=['GET', 'POST'])
def filter_data():
    filter_user_ids = request.form.getlist('filter_user_id')

    
    if not filter_user_ids or '' in filter_user_ids:
        # If "All" is selected or no specific user is selected, retrieve all data
        filtered_data = lampdata.query.all()
    else:
        # Perform filtering based on the selected user IDs
        # Use the `in_` clause to filter for multiple user IDs
        filtered_data = lampdata.query.filter(lampdata.userID.in_(filter_user_ids)).all()

    return render_template('index.html', filtered_data=filtered_data)
```

## Docker
Create a docker file that contains the following.
```
FROM python:3.8-alpine
WORKDIR /app
COPY . /app
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    && apk add libffi-dev
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app/app.py"]
```
Something to note is the last line CMD ["python", "app/app.py"]. Since my app.py is placed in a a folder called app, we had to specify the function. 

Please include the following in your requirements.txt file.


After that, build the image.
```
Flask
authlib
Flask-SQLAlchemy
sentry-sdk
python-dotenv==0.19.0
requests==2.26.0
pymysql==1.0.2
```

As a side note, my db_functions.py is in the same folder as my app.py because it imports a function from it. I could not figure out a way to bypass that as I wanted to db_functions.py in the folder called db. I tried the following code to mild success.
```python
import sys
sys.path.append('/home/jason_tang/flask_e2e_project/db')
```
This allowed my app to function properly locally, but I could not create a docker image of it. I reverted the code, and went to simply placing the db_functions.py within the same level as my app.py. 

Now, we can build the image
```
docker build -t "name of image" .
```
To launch the image into a container, do the following.
```
docker run -d -p 8000:8000 "name of image"
```
The docker container should be functioning and running on port 8000. 

![](https://github.com/jas-tang/flask_e2e_project/blob/main/docs/docker%20container%20success.JPG)

Then I created the docker-compose.yaml file.
```
version: '3'
services:
  mindlamp_db:
    build: ./flask_e2e_project
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app
```
To compose the app, we can use 
```
docker-compose up --build
```

## Azure Deployment
Install Azure CLI by pasting the following script into the shell
```
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

Test if the install worked correct with the following code
```
az
```

Give permission to the shell with a Microsoft account
```
az login --use-device-code
```

Locate all subscription IDs within the shell
```
az account list --output table
```

Change the subscription approrpiate name. For my case, it was Azure for Students.

```
az account set --subscription (insert the subscription ID here)
```

Create a new resource group within the Azure Web Portal. It is located in the Resource Group tab. Ensure that the new group has its subscription set to the working subscription name. For my case, it was Azure for Students. 

Create the web app and connect it to Microsoft Azure with the following code.
```
az webapp up --resource-group (insert group name) --name (insert your app name) --runtime <(Insert language)> --sku <(insert service plan)>
az webapp up --resource-group Jason504 --name jastang504-flask --runtime <Python> --sku <b1>
```

The application should now be deployed. Access your application via Microsoft Azure's App Services tab. 

In the case that you need to redeploy the app, use the following code
```
az webapp up
```

Here is how you delete the app
```
az webapp delete --name (insert app name) --resource-group (insert resource group)
```

My attempt at deploying on azure failed because I realized that my app.py was reliant on multiple files. When I was deploying my app.py, it was only deploying app.py, but not the rest of the requirements. 
I was able to deploy an app, but it did not function.
![](https://github.com/jas-tang/flask_e2e_project/blob/main/docs/azure%20web%20app.JPG)
