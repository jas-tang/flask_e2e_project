from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import or_


### Part 2 - initial sqlalchemy-engine to connect to db:

engine = create_engine("mysql+pymysql://jason504:Thisismypassword2000*@jason-azure.mysql.database.azure.com/mindlamp",
                         connect_args={'ssl': {'ssl-mode': 'preferred'}},
                         )

## Test connection

inspector = inspect(engine)
inspector.get_table_names()


app = Flask(__name__)

# Configure the database URI using PyMySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://jason504:Thisismypassword2000*@jason-azure.mysql.database.azure.com/mindlamp'
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
    return render_template('home.html')

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

