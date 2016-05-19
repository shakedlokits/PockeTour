import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import json
import urllib2

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set([ 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/image', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return "failed to retrieve image"


@app.route("/")
def hello():
    img = request.args.get('img')
    gps = request.args.get('gps')
    imVec = json.loads(urllib2.unquote(img))
    gpsVec = json.loads(urllib2.unquote(gps))
 #   return showim(imVec, gpsVec)
    return "im = "+str(imVec[1]) +" gps = "+ str(gpsVec)



if __name__ == "__main__":
    app.run()