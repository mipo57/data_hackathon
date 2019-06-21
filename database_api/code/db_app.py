from flask import Flask, request
from db_queries import DataHandler


app = Flask(__name__)

'''
@app.route('/database_api/<place>')
def get_place(place):
    dh = DataHandler()
    return dh.select_schools_by_place(place)
'''


@app.route('/database_api/getByDistance')
def get_by_distance():
    distance = request.args.get("dist")
    latitudeN = request.args.get("latN")
    longitudeE = request.args.get("lonE")
    dh = DataHandler()
    return dh.select_schools_by_distance(float(latitudeN), float(longitudeE), float(distance))


@app.route('/database_api/getSchools')
def get_schools():
    sorted = request.args.get("sorted")
    sort_by = request.args.get("sortby")
    city = request.args.get("city")

    where_cause = ''
    sort_cause = ''

    if sorted is 1:
        sort_cause = 'ORDER BY '


    return where_cause + sort_cause + "DUPA" + sorted



@app.route('/database_api/getSimilarSchools')
def get_similar_schools():
    city = request.args.get("city")
    rspo = request.args.get("rspo")
    dh = DataHandler()
    return dh.get_similar_schools(str(city), int(rspo))


@app.route('/database_api/getByStudTeach')
def get_by_stud_teach():
    rspo = request.args.get("rspo")
    distance = request.args.get("dist")
    dh = DataHandler()
    return dh.select_school_by_stud_teach_coeff(rspo, float(distance))


@app.route('/database_api/getFullInfo')
def select_school_by_rspo():
    rspo = request.args.get("rspo")
    dh = DataHandler()
    return dh.select_school_by_rspo(rspo)


if __name__ == '__main__':
    app.run("0.0.0.0")


"""
EXAMPLE OF USE
http://127.0.0.1:5000/database_api/getByDistance?dist=5&latN=51.504455&lonE=18.125713
http://127.0.0.1:5000/database_api/Kalisz
"""