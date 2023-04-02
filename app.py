
from flask import Flask,redirect,url_for,render_template,request
import sqlite3 
app=Flask(__name__)

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/')
def main():
    print("------abc-----")
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_check():
    username = request.form['username']
    password = request.form['password']
    mydb = sqlite3.connect("cia2")
    mycursor = mydb.cursor()
    mycursor.execute("select * from login")
    data = mycursor.fetchall()
    username_list=[]
    password_list=[]

    for i in data:
        username_list.append(i[0])
        password_list.append(i[-1])

    if username not in username_list:
        return render_template('login.html',msg="Invalid username or password")
    else:
        if password not in password_list:
            return render_template('login.html',msg="Invalid username or password")
        else:
            return render_template("index.html")


@app.route('/success/<int:score>')
def success(score):
    res=""
    if score>=50:
        res="PASS"
    else:
        res='FAIL'
    exp={'score':score,'res':res}
    return render_template('result.html',result=exp)


@app.route('/fail/<int:score>')
def fail(score):
    return "The Person has failed and the marks is "+ str(score)

### Result checker
@app.route('/results/<int:marks>')
def results(marks):
    result=""
    if marks<50:
        result='fail'
    else:
        result='success'
    return redirect(url_for(result,score=marks))

### Result checker submit html page
@app.route('/submit',methods=['POST','GET'])
def submit():
    total_score=0
    if request.method=='POST':
        science=float(request.form['science'])
        maths=float(request.form['maths'])
        c=float(request.form['c'])
        data_science=float(request.form['datascience'])
        total_score=(science+maths+c+data_science)/4
    res=""
    return redirect(url_for('success',score=total_score))

    



if __name__=='__main__':
    app.run(debug=True)