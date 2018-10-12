from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import pandas as pd

UPLOAD_FOLDER = '/home/amar/mydir/'
static_folder = '/home/amar/PycharmProjects/nark/static/'
templates_folder = '/home/amar/PycharmProjects/nark/templates/'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:amaramar@localhost:5432/postgres"
app.config['SECRET_KEY'] = "amaramar"

def allowed_file(title):
    f = title.split('.')[-1]
    if f in ALLOWED_EXTENSIONS:
        return True
    else:
        return False

headstr = ""
head = []
newheadlst = []
filename = ""
newsize = ''
df = pd.DataFrame()

@app.route('/', methods=['GET','POST'])
def index():
    return render_template("index.html")


@app.route('/map', methods=['POST', 'GET'])
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
    global size
    global newheadlst
    global df
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

        newheadlst = [A1,B1,C1,D1,E1]
        newheadstr = "{},{},{},{},{}".format(A1,B1,C1,D1,E1)

        csvfile = open(UPLOAD_FOLDER+filename, 'r')
        newcsv = open(UPLOAD_FOLDER+'new'+filename, 'w')
        d = csvfile.read()
        s = d.replace(headstr, newheadstr)
        del d
        newcsv.write(s)
        del s
        csvfile.close()
        newcsv.close()
        df = pd.read_csv(UPLOAD_FOLDER + 'new' + filename)
        size = df.shape[0]
        del df

        return render_template("filtering.html", size=size)

'''

@app.route('/filter', methods=['POST'])
def filter():
    if request.method == 'POST':
        df = pd.read_csv(UPLOAD_FOLDER + 'new' + filename)

        age = int(request.form['age'])
        if "m" or "f" in request.form['gender']:
            gender = str(request.form['gender'])
        else:
            gender = "na"
        doi = str(request.form['doi'])
        if "y" or "n" in request.form['married']:
            married = str(request.form['married'])
        else:
            married = "na"
        loan = float(request.form['loan'])
        # return "{} {} {} {} {}".format(age,gender,doi,married,loan)
        #
        # df = pd.read_csv(UPLOAD_FOLDER + 'new' + filename)
        params = [age,gender,doi,married,loan]
        return"{}".format(params)

        # df1 = df.loc[lambda df: df.Age < age]
        # df2 = df1.loc[lambda df1: df.Gender == gender]
        # print(df2)
        # jj = df2.shape[0]
        # return "{}".format(df2)
        # add = UPLOAD_FOLDER+'new'+filename
        # return render_template("filteringnew.html", size = jj)
'''

@app.route('/templates', methods=['POST'])
def filter():
    if request.method == 'POST':
        global newsize
        df = pd.read_csv(UPLOAD_FOLDER + 'new' + filename)

        age = int(request.form['age'])
        if "m" or "f" in request.form['gender']:
            gender = str(request.form['gender'])
        else:
            gender = "na"
        doi = str(request.form['doi'])
        if "y" or "n" in request.form['married']:
            married = str(request.form['married'])
        else:
            married = "na"
        loan = float(request.form['loan'])

        if age == 0:
            df1 = df
        else:
            df1 = df.loc[lambda df: df.Age < age]

        if gender == "na":
            df2 = df1
        else:
            df2 = df1.loc[lambda df1: df.Gender == gender]

        # if doi == '':
            # df3 = df2
        # else:
            # df3 = df2.loc[lambda df2: df.Date_of_Issue == doi]

        if married == "na":
            df4 = df2
        else:
            df4 = df2.loc[lambda df2: df.Married == married]

        if loan == 0:
            df5 = df4
        else:
            df5 = df4.loc[lambda df4: df.Loan_Amount < loan]

        newsize = df5.shape[0]
        df6 = df5
        df5.to_csv(static_folder+'short'+filename, index=False)
        df6.to_csv(templates_folder+'short'+filename, index=False)
        df6.to_html('templates/newpool.html')
        # jj = templates_folder+'newpool'+filename
        return render_template("filteringnew.html", size=newsize)

@app.route('/viewpool')
def viewpool():
    return render_template("newpool.html")

if __name__ == "__main_":
    app.run()
    # app.run(host='0.0.0.0')
