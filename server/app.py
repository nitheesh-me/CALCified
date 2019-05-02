#!flask/bin/python

# Author: Nitheesh Chandra
# Email: nitheesh.my@gmail.com
# Git repository: https://github.com/nitheesh-me/se-app
# This work based on jQuery-File-Upload which can be found at https://github.com/blueimp/jQuery-File-Upload/

import os
import PIL
from PIL import Image
import simplejson
import traceback
from pprint import pprint
from flask_cors import CORS


from flask import Flask, Response, request, render_template, redirect, url_for, send_from_directory, jsonify
from flask_bootstrap import Bootstrap
from werkzeug import secure_filename

from lib.upload_file import uploadfile

import os
import shutil

import random
import string
shutil.rmtree("data/")
os.makedirs('data/thumbnail',exist_ok=True)

MAJOR_DICT = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'This is a hardest string to guess'
app.config['UPLOAD_FOLDER'] = 'data/'
app.config['THUMBNAIL_FOLDER'] = 'data/thumbnail/'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

CORS(app, support_credentials=True)

ALLOWED_EXTENSIONS = set(['txt', 'gif','mp3', 'png', 'jpg', 'jpeg', 'bmp', 'rar', 'zip', '7zip', 'doc', 'docx'])
IGNORED_FILES = set(['.gitignore'])

bootstrap = Bootstrap(app)


def allowed_file(filename):
    """
    Check if the file is in allowed extensions
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def gen_random_folder_name(num):
    randomSource = string.ascii_lowercase + string.ascii_uppercase + string.digits
    folder = random.choice(randomSource)
    for i in range(num):
        folder += random.choice(randomSource)
    while folder in os.listdir("data"):
        folder = gen_random_folder_name(10)
    return folder

def gen_file_name(filename,folder):
    """
    If file was exist already, rename it and return a new name
    """

    i = 1
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],str(folder), filename)):
        name, extension = os.path.splitext(filename)
        if name[-2]=="_":
            name = name[:-2]
        filename = '%s_%s%s' % (name, str(i), extension)
        i += 1

    return filename


def create_thumbnail(image,folder):
    try:
        base_width = 80
        img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], str(folder), image))
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)
        os.makedirs(os.path.join(app.config['THUMBNAIL_FOLDER'], str(folder)), exist_ok=True)
        img.save(os.path.join(app.config['THUMBNAIL_FOLDER'], str(folder), image))

        return True

    except:
        print (traceback.format_exc())
        return False


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files['file']
        pprint(vars(request))
        exp,res = (request.form.get('exp'),request.form.get('res'))

        folder = gen_random_folder_name(10)
        print(exp,res,folder)
        MAJOR_DICT[exp+'--'+res] = {'folder':folder,'files':[]}
        if files:
            filename = secure_filename(files.filename)
            filename = gen_file_name(filename,folder)
            xx = '1'
            mime_type = files.content_type

            if not allowed_file(files.filename):
                result = uploadfile(name=filename, type=mime_type, size=0, not_allowed_msg="File type not allowed")

            else:
                os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], str(folder)), exist_ok=True)
                # save file to disk
                uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], str(folder), filename)
                files.save(uploaded_file_path)


                # create thumbnail after saving
                if mime_type.startswith('image'):
                    create_thumbnail(filename,folder)

                # get file size after saving
                size = os.path.getsize(uploaded_file_path)

                # return json for js call back
                result = uploadfile(folder=str(folder),name=filename, type=mime_type, size=size)
                MAJOR_DICT[exp+'--'+res]['files'].append(result.get_file())
            return simplejson.dumps({"files": [result.get_file()]})

    if request.method == 'GET':
        # get all file in ./data directory
        exp = request.args.get('exp')
        res = request.args.get('res')
        folder = MAJOR_DICT[exp+"--"+res]["folder"]
        files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']+folder) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'],folder,f)) ]

        file_display = []

        for f in files:
            size = os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'],folder, f))
            file_saved = uploadfile(folder = folder, name=f, size=size)
            file_display.append(file_saved.get_file())

        return simplejson.dumps({"files": file_display})

    return redirect("https://www.google.coin/search?q=calculator")


@app.route("/delete/<string:folder>/<string:filename>", methods=['DELETE'])
def delete(folder,filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'],folder, filename)
    file_thumb_path = os.path.join(app.config['THUMBNAIL_FOLDER'],folder, filename)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)

            if os.path.exists(file_thumb_path):
                os.remove(file_thumb_path)

            return simplejson.dumps({filename: 'True'})
        except:
            return simplejson.dumps({filename: 'False'})

# serve static files
@app.route("/thumbnail/<string:folder>/<string:filename>", methods=['GET'])
def get_thumbnail(folder,filename):
    return send_from_directory(os.path.join(app.config['THUMBNAIL_FOLDER'],folder), filename=filename)


@app.route("/data/<string:folder>/<string:filename>", methods=['GET'])
def get_file(folder,filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'],folder), filename=filename)

@app.route("/find", methods=['GET'])
def find():
    exp,res = request.args.get('exp'),request.args.get('res')
    try:
        x = MAJOR_DICT[exp+'--'+res]
    except:
        x = MAJOR_DICT

    resp = Response(response=simplejson.dumps(x),
        status=200,
        mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.type = 'opaque'
    return resp

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True,ssl_context='adhoc')
