from flask import Flask, render_template, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
from db_functions import update_or_create_user
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
import sentry_sdk

# Load environment variables from .env
load_dotenv()

# Construct the database URL
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

database_url = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}"
print(database_url)

### Part 2 - initial sqlalchemy-engine to connect to db:

engine = create_engine(database_url,
                         connect_args={'ssl': {'ssl-mode': 'preferred'}},
                         )

## Test connection

inspector = inspect(engine)
inspector.get_table_names()

## OAuth
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

##SDK Sentry
sentry_sdk.init(
    dsn="",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

sentry_sdk.init(
    dsn="https://76cc562e9f73c47a55644f0175136426@o4506392591204352.ingest.sentry.io/4506392595005440",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

app = Flask(__name__)


app.secret_key = os.urandom(12)
oauth = OAuth(app)

# Configure the database URI using PyMySQL
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy instance
db = SQLAlchemy(app)

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

@app.route('/')
def index():
    return render_template('googleoauth.html')

#testing for Sentry SDK
@app.route('/error')
def creating_error():
    try:
        1/0
    except Exception as e:
        raise Exception (f'Something went wrong: {e}')

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

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token, nonce=session['nonce'])
    session['user'] = user
    update_or_create_user(user)
    print(" Google User ", user)
    return redirect('/home')

@app.route('/home/')
def dashboard():
    user = session.get('user')
    if user:
        return render_template('home.html', user=user)
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/mindlamp_data')
def mindlamp_route():
    mindlamp_data = lampdata.query.all()
    return render_template('index.html', lampdata=mindlamp_data)

from flask import Flask, render_template, request


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



if __name__ == '__main__':
    app.run(
        debug=True,
        port=8000
    )

