from flask import Flask, redirect, url_for, render_template, request
import db_methods as db

app = Flask(__name__, template_folder='templates')


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/stock/search', methods=['GET'])
def input_side():
    return render_template('input_side.html')


@app.route('/stock/insert', methods=['POST'])
def get_input():
    if request.method == 'POST':
        stonk_name = request.form['stonk_name']
        print(stonk_name)
        db.db_write(stonk_name)
    return render_template('await_analysis.html')


if __name__ == '__main__':
    app.run(debug=True)
