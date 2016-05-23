import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

import json
import urllib2
from site_matcher.pocket_matcher import match_site

app = Flask(__name__)


@app.route('/image', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # save image file
        b64_data = request.values['base64']
        with open("/cs/hackathon/pocketour/data/input_img.jpg", "wb") as file:
            file.write(b64_data.decode('base64'))

        # parse gps data
        gps = map(lambda cord: float(cord), json.loads(request.values['gps']))

        # fetch json response
        json_response = match_site("/cs/hackathon/pocketour/data/input_img.jpg", gps)

        return json_response
    return "failed to retrieve image"


@app.route('/test', methods=['GET', 'POST'])
def testing_conn():
    return "Everything is within normal parameters captain"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')
