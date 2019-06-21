from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/getByDistance')
def getByDistance():
    odpowiedz1 = {
        "nazwa": "PWR",
        "miasto": "wroclaw"
        # itd...
    }

    odpowiedz2 = {
        "nazwa": "Inna uczelnia",
        "miasto": "nie wroclaw"
        # itd...
    }

    odleglosc = request.args.get("odleglosc")

    print(odleglosc)

    if odleglosc == str(5):
        return json.dumps(odpowiedz1)
    else:
        return json.dumps(odpowiedz2)
        

if __name__ == '__main__':
    app.run()