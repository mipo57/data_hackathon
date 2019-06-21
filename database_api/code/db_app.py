from flask import Flask, request
from data_handler import DataHandler


app = Flask(__name__)


@app.route('/database_api/<place>')
def get_place(place):
    dh = DataHandler()
    return dh.select_schools_by_place(place)



@app.route('/database_api/getByDistance')
def get_by_distance():
    distance = request.args.get("dist")
    latitudeN = request.args.get("latN")
    longitudeE = request.args.get("lonE")
    dh = DataHandler()
    return dh.select_schools_by_distance(float(latitudeN), float(longitudeE), float(distance))


@app.route('/database_api/get_schools')
def get_schools():
    print(request.args)
    sorted = request.args.get("sorted",default=1)
    sortby = request.args.get("sortby",default='matura')
    city = request.args.get("city",default='*')
    for_disabled = request.args.get("for_disabled",default=0)
    limit = request.args.get("limit", default=30)
    local = request.args.get("local", default=0)
    distance = request.args.get("distance",default = 5)
    type = request.args.get("type",default='liceum')
    dh = DataHandler()
    return dh.get_schools(int(sorted), str(sortby), str(city), int(for_disabled),
                          int(limit), int(local), int(distance), str(type))



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