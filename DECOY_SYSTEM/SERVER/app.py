import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
import numpy as np

app = Flask(__name__)
app.secret_key = 'decoysystem'


@app.route("/home")
def home():
    return render_template("index.html")


@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        pwd = request.form["password"]
        r1 = pd.read_excel('user.xlsx')
        for index, row in r1.iterrows():
            if row["email"] == str(email) and row["password"] == str(pwd):

                return redirect(url_for('home'))
        else:
            msg = 'Invalid Login Try Again'
            return render_template('login.html', msg=msg)
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['Email']
        password = request.form['Password']
        col_list = ["name", "email", "password"]
        r1 = pd.read_excel('user.xlsx', usecols=col_list)
        new_row = {'name': name, 'email': email, 'password': password}
        #r1 = r1.append(new_row, ignore_index=True)
        r1 = pd.concat([r1, pd.DataFrame([new_row])], ignore_index=True)
        r1.to_excel('user.xlsx', index=False)
        print("Records created successfully")
        # msg = 'Entered Mail ID Already Existed'
        msg = 'Registration Successfull !! U Can login Here !!!'
        return render_template('login.html', msg=msg)
    return render_template('register.html')


@app.route('/password', methods=['POST', 'GET'])
def password():
    if request.method == 'POST':
        email = request.form['a_email']
        current_pass = request.form['c_password']
        new_pass = request.form['verify']
        verify_pass = request.form['r_verify']

        if not email or not current_pass or not new_pass or not verify_pass:
            msg = 'Please fill in all fields'
            return render_template('password.html', msg=msg)

        r1 = pd.read_excel('user.xlsx')

        for index, row in r1.iterrows():
            if row["password"] == str(current_pass):
                if new_pass == verify_pass:
                    # Hash and store the new password securely in a real-world application
                    r1.loc[index, "password"] = str(verify_pass)
                    r1.to_excel("user.xlsx", index=False)
                    msg = 'Password changed successfully'
                    return render_template('password.html', msg=msg)
                else:
                    msg = 'Re-entered password does not match'
                    return render_template('password.html', msg=msg)

        msg = 'Incorrect email or password'
        return render_template('password.html', msg=msg)

    return render_template('password.html')


def read_excel(file):
    df = pd.read_excel(file)
    cols = list(df.columns)
    df1 = np.asarray(df)
    length = len(df1)
    df2 = []
    count = length
    for i in range(length):
        df2.append(df1[count - 1])
        count -= 1
    print("df2: ", df2)
    return cols, df2


@app.route("/clear_data", methods=['GET', 'POST'])
def clear_data():
    df1 = pd.read_excel('ip_log.xlsx')
    df1.drop(df1.index, inplace=True)
    df1.to_excel('ip_log.xlsx', index=False)
    return redirect(url_for('home'))


@app.route("/all_ip", methods=['GET', 'POST'])
def all_ip():
    data = read_excel('ip_log.xlsx')
    title = "List of All Clients"
    return render_template("index.html", title=title, cols=data[0], values=data[1])


if __name__ == "__main__":
    app.run(debug=True, port=4998)
