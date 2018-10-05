from flask import Flask, render_template, request, jsonify, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = '/home/amar/mydir/'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:amaramar@localhost:5432/postgres"
app.config['SECRET_KEY'] = "amaramar"

# db = SQLAlchemy(app)
# db.init_app(app)

'''
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Contents(db.Model):
    __tablename__ = "example"
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    name = db.Column(db.String(length=50))
    married = db.Column(db.Boolean)
    date = db.Column(db.DATE)
'''
def allowed_file(title):
    f = title.split('.')[-1]
    if f in ALLOWED_EXTENSIONS:
        return True
    else:
        return False

headstr=""
head=[]
filename=""

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('test1.html')


@app.route('/map', methods=['POST'])
def mapping():
    global filename
    global headstr
    global head
    if request.method == "POST":
        file = request.files['inputfile']
        title = file.filename
        if allowed_file(title) == True:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with open(UPLOAD_FOLDER+filename) as csvfile:
                headstr = csvfile.readline().rstrip()
                csvfile.seek(0)
                head = csvfile.readline().rstrip().split(',')
                return render_template('mapping.html', head=head)
                
        else:
            return render_template("again.html")


        # stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
        # csv_input = csv.reader(stream)

@app.route('/headers', methods=['POST'])
def headers():


    if request.method == 'POST':
        newhead = {
            request.form['A']:"Age",
            request.form['B']:"Gender",
            request.form['C']:"Date_of_Issue",
            request.form['D']:"Married",
            request.form['E']:"Loan_Amount"
        }

        A1 = newhead[head[0]]
        B1 = newhead[head[1]]
        C1 = newhead[head[2]]
        D1 = newhead[head[3]]
        E1 = newhead[head[4]]
        newheadstr =  "{},{},{},{},{}".format(A1,B1,C1,D1,E1)

        csvfile = open(UPLOAD_FOLDER+filename, 'r')
        newcsv = open(UPLOAD_FOLDER+'new'+filename, 'w')
        d = csvfile.read()
        s = d.replace(headstr, newheadstr)
        del d
        newcsv.write(s)
        del s
        csvfile.close()
        newcsv.close()
        return render_template("filtering.html")

if __name__ == "__main_":
    app.run(debug=True)
