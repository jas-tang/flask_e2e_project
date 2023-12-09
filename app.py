from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database URI using PyMySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://jason:jason2023@172.174.249.223:3306/mindlamp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy instance
db = SQLAlchemy(app)

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
    lampdata = LAMPdata.query.all()
    return render_template('index.html', lampdata=lampdata)

if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )
