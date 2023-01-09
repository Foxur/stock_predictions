from flask import Flask, redirect, url_for, render_template, request
import db_methods as db
import stock_data.processing.stock_prediction as sp
from datetime import date, timedelta

app = Flask(__name__, template_folder='templates')


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/stock/search', methods=['GET'])
def input_side():
    return render_template('input_side.html')


@app.route('/stock/analysis', methods=['POST'])
def get_input():
    if request.method == 'POST':
        stonk_name = request.form['stonk_name']
        if db.check_exist(stonk_name):
        # get Last creation Date
            if db.check_last_creation(stonk_name):
        #Fasle == create new Model | True load predictions
                predictions = sp.load_predictions(stonk_name)
            else:
                predictions = sp.get_new_predictions(stonk_name)
                db.update_timestamp(stonk_name)

        else:
            predictions = sp.get_new_predictions(stonk_name)
            db.db_write(stonk_name)
    time = []
    for i in range(0, len(predictions)):
        time.append(date.today() + timedelta(days=i))

    return render_template('await_analysis.html', length= range(0, len(predictions)), predictions=predictions, time=time)


if __name__ == '__main__':
    app.run(debug=True)
