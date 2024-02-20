from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import socket
import sys

app = Flask(__name__)
app.secret_key = 'decoy'

port = 5002


class Client:
    def __init__(self, ip):
        self.content = None
        self.ip = ip
        self.port = port

    def send_file(self, file):
        self.content = file.read()
        return self.content

    def connect(self, selected_file, filename, email):
        try:
            s = socket.socket()
            s.connect((self.ip, self.port))
            print("Connected to server")

            s.recv(1024)

            content = self.send_file(selected_file)
            s.send(content)
            print("File content sent")

            s.recv(2048)

            s.send(filename.encode("utf-8"))
            print("Filename sent")

            s.recv(1024)

            s.send(email.encode("utf-8"))
            print("Email sent")

            s.recv(1024)

            s.close()

        except Exception as e:
            print("[ERROR] Oops something went wrong, check below error message")
            print("[ERROR MESSAGE] ", e)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    ip = request.form['ip']
    filename = request.form['filename']
    email = request.form['email']
    selected_file = request.files['option']

    client = Client(ip)
    client.connect(selected_file, filename, email)

    print("Successfully Shared.")

    message = "File Shared Successfully."

    return render_template('index.html', msg=message)


if __name__ == '__main__':
    app.run(debug=True, port=4887)
