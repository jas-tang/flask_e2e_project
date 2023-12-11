from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


### Part 2 - initial sqlalchemy-engine to connect to db:

engine = create_engine("mysql+pymysql://jason504:Thisismypassword2000*@jason-azure.mysql.database.azure.com/mindlamp",
                         connect_args={'ssl': {'ssl-mode': 'preferred'}},
                         )

## Test connection

inspector = inspect(engine)
inspector.get_table_names()


app = Flask(__name__)

# Configure the database URI using PyMySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://jason:jason2023@172.174.249.223:3306/mindlamp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy instance
db = SQLAlchemy(app, session_options={'autoflush': False})

class LAMPdata(db.Model):
    userID = db.Column(db.String(50), primary_key=True)
    userNAME = db.Column(db.String(50), nullable=False)
    ActivityName = db.Column(db.String(50), nullable=False)
    ActivityDate = db.Column(db.String(50), nullable=False)
    item = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/mindlamp_data')
def mindlamp():
    lampdata = LAMPdata.query.all()
    return render_template('index.html', lampdata=lampdata)

if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )
