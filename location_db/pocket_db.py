import sqlite3
from geopy.distance import vincenty as get_distance
import json


class PocketDB:
    def __init__(self):
        """
        DB initializer, connecting to DB
        :return: self
        """
        self._db = sqlite3.connect('/home/shakedl/PockeTour/location_db/database.db')
        self._cursor = self._db.cursor()

    def __enter__(self):
        """
        DB 'with' initializer
        :return: self
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        DB 'with' destructor
        kills the DB connection
        :return: None
        """
        self._db.close()

    def get_descriptors(self, current_gps):
        """
        gets the descriptors of sites located near the current GPS location
        :param current_gps: tuple containing the GPS locations (lon,lat)
        :return: list of objects of the form {"id":<location_id>, "descriptors":[[...],[...]]}
        """

        # get nearest sites
        legal_id_list = self._get_closest_sites(current_gps)

        # initialize sql query
        query = "select id,descriptors from PockeTour where "

        # build query request for specific id's
        for index, id in enumerate(legal_id_list):
            query += "id=" + str(id)

            # if not last iteration, delimit with 'or'
            if index < len(legal_id_list) - 1:
                query += " or "

        # query descriptors from database
        if len(legal_id_list) == 0:
            print "no matching sites found"
        self._cursor.execute(query)

        # fetch data from database
        id_descriptors_list = self._cursor.fetchall()

        # remap data and parse json
        id_descriptors_list = map(lambda location: {"id": int(location[0]), "desc": json.loads(location[1])},
                                  id_descriptors_list)

        return id_descriptors_list

    def _get_closest_sites(self, current_gps, radius_km=0.2):


        

        # request db for id's and GPS
        self._cursor.execute('SELECT id,gps FROM PockeTour')

        # parse id's and GPS from json
        id_gps_list = map(lambda location: (int(location[0]), tuple(json.loads(location[1]))), self._cursor.fetchall())

        # filter sites by distance
        id_gps_list = filter(lambda location: get_distance(current_gps, location[1]).km < radius_km, id_gps_list)

        # generate an id list from the remaining results
        id_list = map(lambda location: location[0], id_gps_list)

        return id_list

    def get_site_by_id(self, id):
        """
        return the data of a site represented by its id
        :param id: the sites id, and integer
        :return: a json object of the form {"name": ... ,"description": ... ,"image_url": ... ,"website_url": ...}
        """

        # build site data query with given id
        query = "select name,description,image_url,website from PockeTour where id=" + str(id)

        # query and fetch data from database
        self._cursor.execute(query)
        site_data = self._cursor.fetchall()[0]

        # return a json of an object holding the requested data
        return json.dumps({"name": site_data[0],
                           "description": site_data[1],
                           "image_url": site_data[2],
                           "website_url": site_data[3]})
