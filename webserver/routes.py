from flask import Flask, render_template
import json



app = Flask(__name__)

@app.route('/drinks')
def drinks():
    drinks = json.load(open('./drinks.json'))
    return render_template('drinks.html', drinks=drinks)


if __name__ == '__main__':
    app.run(debug=True)