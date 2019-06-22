import pymssql
import json
from math import sin, cos, sqrt, atan2, radians


class DataHandler:

    def __init__(self, server='localhost:1433', user='sa', password='P@ssw0rd', database='BetterEducation'): # zmienić na localhost
        self._conn = pymssql.connect(server=server, user=user, password=password, database=database)

    def _query_db(self, sql_query):
        cursor = self._conn.cursor()
        cursor.execute(sql_query)
        jsonable_data = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        return jsonable_data

    def select_schools_by_place(self, place):
        query_skeleton = 'SELECT * FROM szkolyAdresy WHERE Miejscowosc = '
        place = '\'' + place + '\''
        result = self._query_db(query_skeleton + place)
        return json.dumps(result)

    @staticmethod
    def _get_distance(lat1, lon1, lat2, lon2):
        earth_radius = 6373.0

        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return round(earth_radius * c, 3)

    def select_schools_by_distance(self, latidudeN, longitudeE, distance):
        query_skeleton = 'SELECT * FROM szkolyAdresy'
        outer_places = self._query_db(query_skeleton)

        result = list()
        for record in outer_places:
            record_distance = self._get_distance(float(record['LatitudeN']), float(record['LongitudeE']),
                                                 float(latidudeN), float(longitudeE))
            # print('{:7} {:7} {:7}\n'.format(record['RSPO'], center_place[0]['RSPO'], record_distance))
            if record_distance < distance:
                result.append(record)

        return json.dumps(result)

    def get_similar_schools_by_stc(self, rspo, distance):
        query_skeleton = 'SELECT szkolyPlacowki.RSPO, CASE WHEN LEtatatowNauczycieli = 0 THEN 0 ELSE LUczniow /' \
                         ' LEtatatowNauczycieli END \'StosunekUczNaucz\', LongitudeE, LatitudeN FROM szkolyPlacowki' \
                         ' INNER JOIN szkolyAdresy sA on szkolyPlacowki.RSPO = sA.RSPO WHERE szkolyPlacowki.RSPO '
        other_schools = self._query_db(query_skeleton + ' <> ' + rspo)
        my_school = self._query_db(query_skeleton + ' = ' + rspo)


        better_1 = my_school[0]
        better_2 = my_school[0]

        worse_1 = my_school[0]
        worse_2 = my_school[0]

        better_1_val = 1000  # magic start value -> synthetic, unreal big exam result
        better_2_val = 1000  # magic start value -> synthetic, unreal big exam result

        worse_1_val = -1000  # magic start value -> synthetic, unreal low exam result
        worse_2_val = -1000  # magic start value -> synthetic, unreal low exam result

        for record in other_schools:
            record_distance = self._get_distance(float(record['LatitudeN']), float(record['LongitudeE']),
                                                 float(my_school[0]['LatitudeN']), float(my_school[0]['LongitudeE']))
            if record_distance <= distance:
                if float(record['StosunekUczNaucz']) > float(my_school[0]['StosunekUczNaucz']):
                    if float(record['StosunekUczNaucz']) < better_2_val:
                        if record['StosunekUczNaucz'] < better_1_val:
                            better_2 = better_1
                            better_2_val = float(better_1['StosunekUczNaucz'])
                            better_1 = record
                            better_1_val = float(record['StosunekUczNaucz'])
                        else:
                            better_2 = record
                            better_2_val = float(record['StosunekUczNaucz'])
                else:
                    if float(record['StosunekUczNaucz']) > worse_2_val:
                        if float(record['StosunekUczNaucz']) > worse_1_val:
                            worse_2 = worse_1
                            worse_2_val = float(worse_1['StosunekUczNaucz'])
                            worse_1 = record
                            worse_1_val = float(record['StosunekUczNaucz'])
                        else:
                            worse_2 = record
                            worse_2_val = float(record['StosunekUczNaucz'])

        return json.dumps([worse_1, worse_2, my_school, better_2, better_1])

    def select_school_by_rspo(self, rspo):
        query_skeleton = 'SELECT * FROM szkolyAdresy INNER JOIN szkolyPlacowki sP on szkolyAdresy.RSPO = sP.RSPO WHERE'\
                         ' szkolyAdresy.RSPO = '
        my_school = self._query_db(query_skeleton + ' ' + rspo)

        query_skeleton = 'SELECT NazwaPrz, PoziomPrz, TypPrz, SrWynik, LZdajacych, Rok FROM wynikiMatur INNER JOIN '\
                         'przedmioty p on wynikiMatur.IDPrz = p.IDPrz WHERE RSPO = '
        my_info = self._query_db(query_skeleton + rspo)

        return json.dumps([my_school, my_info])

    def get_similar_schools_by_test(self, rspo, distance):
        query_skeleton = 'SELECT AVG(SrWynik) \'Sr\', wynikiMatur.RSPO, Nazwa, LongitudeE, LatitudeN FROM wynikiMatur ' \
                         'INNER JOIN szkolyAdresy sA on wynikiMatur.RSPO = sA.RSPO ' \
                         'INNER JOIN szkolyPlacowki sP on sA.RSPO = sP.RSPO WHERE wynikiMatur.RSPO <> {} ' \
                         'GROUP BY wynikiMatur.RSPO, LongitudeE, LatitudeN, Nazwa'.format(rspo)
        other_schools = self._query_db(query_skeleton)

        query_skeleton = 'SELECT AVG(SrWynik) \'Sr\', wynikiMatur.RSPO, Nazwa, LongitudeE, LatitudeN FROM wynikiMatur ' \
                         'INNER JOIN szkolyAdresy sA on wynikiMatur.RSPO = sA.RSPO ' \
                         'INNER JOIN szkolyPlacowki sP on sA.RSPO = sP.RSPO WHERE wynikiMatur.RSPO = {} ' \
                         'GROUP BY wynikiMatur.RSPO, LongitudeE, LatitudeN, Nazwa'.format(rspo)

        my_school = self._query_db(query_skeleton)

        if len(my_school) == 0:
            query_skeleton = 'SELECT 0 \'Sr\', sA.RSPO, Nazwa, LongitudeE, LatitudeN FROM szkolyAdresy sA INNER JOIN ' \
                             'szkolyPlacowki sP on sA.RSPO = sP.RSPO WHERE sA.RSPO = {}'.format(rspo)

            my_school = self._query_db(query_skeleton)
            my_school[0]['Sr'] = str((int(rspo) % 8) * 10)

        better_1 = my_school[0]
        better_2 = my_school[0]

        worse_1 = my_school[0]
        worse_2 = my_school[0]

        better_1_val = 1000  # magic start value -> synthetic, unreal big exam result
        better_2_val = 1000  # magic start value -> synthetic, unreal big exam result

        worse_1_val = -1000  # magic start value -> synthetic, unreal low exam result
        worse_2_val = -1000  # magic start value -> synthetic, unreal low exam result

        for record in other_schools:
            record_distance = self._get_distance(float(record['LatitudeN']), float(record['LongitudeE']),
                                                 float(my_school[0]['LatitudeN']), float(my_school[0]['LongitudeE']))
            if record_distance <= distance:
                if float(record['Sr']) > float(my_school[0]['Sr']):
                    if float(record['Sr']) < better_2_val:
                        if record['Sr'] < better_1_val:
                            better_2 = better_1
                            better_2_val = float(better_1['Sr'])
                            better_1 = record
                            better_1_val = float(record['Sr'])
                        else:
                            better_2 = record
                            better_2_val = float(record['Sr'])
                else:
                    if float(record['Sr']) > worse_2_val:
                        if float(record['Sr']) > worse_1_val:
                            worse_2 = worse_1
                            worse_2_val = float(worse_1['Sr'])
                            worse_1 = record
                            worse_1_val = float(record['Sr'])
                        else:
                            worse_2 = record
                            worse_2_val = float(record['Sr'])

        return json.dumps([worse_1, worse_2, my_school, better_2, better_1])


'''
# EXAMPLE OF USAGE
dh = DataHandler()
a = dh.select_schools_by_place('Hrubieszów')
b = dh.select_schools_by_distance(51.504455, 18.125713, 5) # wsp. Grabów n Prosną

print(a)
print(b)
'''
