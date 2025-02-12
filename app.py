from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('log-in.html')
@app.route('/admin/beheer')
def beheer():
    return render_template('beheerder-beheer.html')
@app.route('/admin/nieuw')
def admin_nieuw():
    return render_template('nieuwe-admin.html')

if __name__ == "__main__":
    app.run(debug=True)