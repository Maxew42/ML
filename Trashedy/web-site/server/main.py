import matplotlib.pyplot as plt
import cv2
import torchvision.transforms as transforms
import io
from helpers.ml_utils import *
from helpers.plotting import *
import torch
import exifread
from flask import Flask, flash, render_template, url_for, session
import flask
from flask.helpers import flash
from flask.json import jsonify
from datetime import datetime
from flask import request, redirect
import os
from flask_cors import CORS
import folium
from werkzeug.utils import secure_filename
from folium.plugins import HeatMap
from os.path import join, dirname, realpath
import geopy.geocoders
from geopy.geocoders import Nominatim
import pymysql
import pymysql.cursors
from PIL import Image, ExifTags
pymysql.install_as_MySQLdb()
## PARAMETRISATION ##
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploaded_imgs/')
# UPLOAD_FOLDER = 'static/uploaded_imgs/'

MODEL_PATH = "./static/ml_models/model_SGD_balanced_1.5_no_kebab"
MODEL_PATH = join(dirname(realpath(__file__)), MODEL_PATH)
DEVICE = torch.device(
    'cuda') if torch.cuda.is_available() else torch.device('cpu')
CAT_TO_INDEX = {'other': 1,
                'pet': 2,
                'plastic_bag': 3
                }
MODEL = torch.load(MODEL_PATH,map_location=DEVICE)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app)
app.secret_key = "super secret key"

##


def get_co():
    connection = pymysql.connect(host='localhost',
                                 database='trashedy',
                                 user='root',
                                 password='Patate01')
    return connection


@app.route('/getstats')
def get_stats():
    with get_co():
        with get_co().cursor() as cursor:
         # Create a new record
            sql = "SELECT COUNT(*) from dechet where date_ajout between date_sub(now(),INTERVAL 1 WEEK) and now();"
            cursor.execute(sql)
            result = cursor.fetchone()
            cursor.close()

    with get_co():
        with get_co().cursor() as cursor:
         # Create a new record
            sql = "select nom_departement from dechet group by nom_departement order by count(*) desc"
            cursor.execute(sql)
            result2 = cursor.fetchone()
            cursor.close()
    response = jsonify({'nbe_dechets': result, 'pire_departement': result2})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=["POST"])
def upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img = Image.open(file)
        try:

            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break

            exif = img._getexif()

            if exif[orientation] == 3:
                image = img.rotate(180, expand=True)
            elif exif[orientation] == 6:
                img = img.rotate(270, expand=True)
            elif exif[orientation] == 8:
                img = img.rotate(90, expand=True)

        except (AttributeError, KeyError, IndexError, TypeError):
            pass

        img = np.array(img)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], filename), img)
        #npimg = np.fromstring(filestr, np.uint8)
        #img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        img2 = np.asarray(img, dtype="float32")
        height = img2.shape[0]
        width = img2.shape[1]
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #img = Image.fromarray((img*255).astype(np.uint8))
        #img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # image = np.fromstring(image, np.float32)
        # image = file.read()
        # npimg = np.fromstring(image, np.float32)
        # image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        # image = np.asarray(image,dtype=np.float32)
        # image /= 255.0
        # tensor_transform = transforms.Compose([transforms.ToTensor()])
        # image = tensor_transform(image)

        tensor_image = transforms.ToTensor()(img)
        print(tensor_image.shape)
        results = light_evaluate(
            tensor_image, DEVICE, CAT_TO_INDEX, MODEL, erase_overlaping_boxes=True)
        # A séparer et compléter avec les autres écritures possible
        tags = exifread.process_file(file)
        try:
            l_lat = tags['GPS GPSLatitude'].values
            l_lng = tags['GPS GPSLongitude'].values

            lat = float(l_lat[0]) + float(l_lat[1]) / \
                60 + float(l_lat[2])/(60*60)
            lng = float(l_lng[0]) + float(l_lng[1]) / \
                60 + float(l_lng[2])/(60*60)
        except KeyError:
            print("Pas de données GPS")
            lat = ""
            lng = ""
        try:
            date = tags['Image DateTime'].values
            date = date.split(" ")
            date = date[0]
            date = date.split(":")
            date = "-".join(date)
        except KeyError:
            date = ""
            print("Pas de date enregistrée")

        if lat != "":
            folium_map = folium.Map(
                location=(lat, lng), zoom_start=13, tiles='openstreetmap')
            folium.Marker(
                [lat, lng], popup="<b> Emplacement des déchets detectés </b>").add_to(folium_map)
        else:
            folium_map = folium.Map(
                location=(47.299679, 1.917453), zoom_start=6, tiles='openstreetmap')
        folium_map.add_child(folium.LatLngPopup())
        results = list(results)
        results_j = []

        for row in results:
            results_j.append({'classes': row['classes'], 'xmin': float(row['xmin']), 'ymin': float(
                row['ymin']), 'xmax': float(row['xmax']), 'ymax': float(row['ymax']), 'scores': float(100*np.round(row['scores'], 4))})
        if lat != "":
            res = {'width': int(width), 'height': int(
                height), 'latitude': float(lat), 'longitude': float(lng), 'date': date, 'results': results_j, 'map': folium_map._repr_html_()}
        else:
            res = {'width': int(width), 'height': int(
                height), 'latitude': lat, 'longitude': lng, 'date': date, 'results': results_j, 'map': folium_map._repr_html_()}
        response = jsonify(res)
        response.headers.add("Access-Control-Allow-Origin", "*")
        print("ouiiiiiiiiiiiiiiiiiii")
        return response
    else:
        flash("Allowed images type are : jpg, jpeg, png, gif.")
        return redirect(request.url)


@app.route('/getmap', methods=["GET"])
def getmap():
    start_coords = (47.299679, 1.917453)
    with get_co():
        with get_co().cursor() as cursor:
         # Create a new record
            sql = "SELECT latitude, longitude from dechet;"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()

    show_usine = request.args.get('usine', '')
    show_usine_recyclage = request.args.get('usine_recyclage', '')
    folium_map = folium.Map(location=start_coords,
                            zoom_start=6, tiles='openstreetmap')
    if int(show_usine) == 1:
        print("bah du coup oui")
        with get_co():
            with get_co().cursor() as cursor:
                sql = "SELECT latitude,longitude,nom_usine,secteur from usine"
                cursor.execute(sql)

                result1 = cursor.fetchall()
                cursor.close()
        for row in result1:
            folium.Marker([row[0], row[1]], popup="<b>" + row[2] +
                          " : " + row[3] + "</b>").add_to(folium_map)

    lat, lng = [], []
    for row in result:
        lat.append(row[0])
        lng.append(row[1])
    folium_map.add_child(folium.LatLngPopup())
    HeatMap(list(zip(lat, lng))).add_to(folium_map)
    return folium_map._repr_html_()


@app.route('/get_rivers', methods=["GET"])
def get_rivers():
    res = []
    with get_co():
        with get_co().cursor() as cursor:
            sql = "SELECT f.nom_fleuve,f.longueur, count(*) compte from fleuve f join dechet d on f.nom_fleuve = d.nom_fleuve group by f.nom_fleuve, f.longueur order by compte desc;"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
        for row in result:
            res.append(
                {'nom_fleuve': row[0], 'longueur': row[1], 'nbe_dechets': row[2]})
    print(res)
    res = jsonify(res)
    res.headers.add("Access-Control-Allow-Origin", "*")
    return res


@app.route('/send_result', methods=['POST'])
def send_result():
    data = request.get_json()
    waste_info = data['waste_info']
    lat = data['latitude']
    lng = data['longitude']
    date = data['date']
    river = data['river']
    geolocator = Nominatim(user_agent='benoit_claudic@hotmail.fr')
    location = geolocator.reverse(str(lat) + "," + str(lng))
    departement = location.raw["address"]
    departement = departement['county']
    infos = []
    if date != "" and lng != "" and lat != "":
        for row in waste_info:
            infos.append([date, 'default_url', lat, lng, row['classes'],
                         departement, river, "benoit.claudic@efrei.net"])
        print(infos)
        try:
            con = get_co()
            with con.cursor() as cursor:
                sql = "Insert into dechet (date_ajout,url,latitude,longitude,type_dechet, nom_departement,nom_fleuve,nom_utilisateur) Values(%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.executemany(sql, infos)
                con.commit()
                cursor.close()
        except pymysql.err.IntegrityError:
            return 'Erreur', 500
    res = jsonify(message=['all good'])
    res.headers.add("Access-Control-Allow-Origin", "*")
    return res


@ app.route('/get_river', methods=["GET"])
def get_river_map():
    # A modifier avec les valeurs dans la table fleuve
    start_coords = (47.299679, 1.917453)
    river_name = request.args.get('river_name', '')
    with get_co():
        with get_co().cursor() as cursor:
         # Create a new record
            sql = "SELECT latitude, longitude from dechet WHERE nom_fleuve = %s;"
            cursor.execute(sql, (river_name))
            result = cursor.fetchall()
            cursor.close()

    folium_map = folium.Map(location=start_coords,
                            zoom_start=6, tiles='openstreetmap')
    with get_co():
        with get_co().cursor() as cursor:
            sql = "SELECT latitude,longitude,nom_usine,secteur from usine"
            cursor.execute(sql)
            result1 = cursor.fetchall()
            cursor.close()
    for row in result1:
        folium.Marker([row[0], row[1]], popup="<b>" + row[2] +
                      " : " + row[3] + "</b>").add_to(folium_map)

    lat, lng = [], []
    for row in result:
        lat.append(row[0])
        lng.append(row[1])
    folium_map.add_child(folium.LatLngPopup())
    HeatMap(list(zip(lat, lng))).add_to(folium_map)
    return folium_map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)
