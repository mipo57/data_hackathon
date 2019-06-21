from flask import Flask, request
from db_queries import DataHandler


app = Flask(__name__)


@app.route('/database_api/<place>')
def get_place(place):
    dh = DataHandler()
    return dh.select_schools_by_place(place)


@app.route('/database_api/get_by_distance')
def get_by_distance():
    distance = request.args.get("dist")
    latitudeN = request.args.get("latN")
    longitudeE = request.args.get("lonE")
    dh = DataHandler()
    return dh.select_schools_by_distance(float(latitudeN), float(longitudeE), float(distance))


if __name__ == '__main__':
    app.run("0.0.0.0")


"""
EXAMPLE OF USE
http://127.0.0.1:5000/get_by_distance?dist=5&latN=51.504455&lonE=18.125713
http://127.0.0.1:5000/Kalisz
"""