from flask import Flask, render_template, redirect, url_for, request, session
import db_methods as db
import stock_data.processing.stock_prediction as sp
import stock_data.processing.get_stock_data as gd
from datetime import date, timedelta

app = Flask(__name__, template_folder='templates')

# Initial loading of symbols
companys_symbols, symbols = gd.get_symbols()


@app.route('/', methods=['GET'])
def home_page():
    latest_creations = db.get_latest_creations()
    return render_template('home.html', data=latest_creations)


@app.route('/stock/search', methods=['GET'])
def input_side():
    return render_template('input_side.html', data=companys_symbols)


@app.route('/stock/analysis', methods=['POST'])
def get_input():
    if request.method == 'POST':
        stonk_name = request.form['stonk_name']
        if stonk_name in symbols:
            print('Found')
            if db.check_exist(stonk_name):
                # get Last creation Date
                if db.check_last_creation(stonk_name):
                    # Fasle == create new Model | True load predictions
                    predictions = sp.load_predictions(stonk_name)
                else:
                    sp.get_new_predictions(stonk_name)
                    predictions = sp.get_new_predictions(stonk_name)
                    db.update_timestamp(stonk_name)

            else:
                sp.get_new_predictions(stonk_name)
                predictions = sp.load_predictions(stonk_name)
                db.db_write(stonk_name)
            time2 = []
            for i in range(0, len(predictions)):
                time2.append(date.today() + timedelta(days=i))
            return render_template('await_analysis.html', length=range(0, len(predictions)), predictions=predictions,
                                   time=time2,
                                   name=stonk_name, stonk_name=stonk_name + '.png')
        else:
            return redirect(url_for('input_side'))


if __name__ == '__main__':
    app.run(debug=True)
