from flask import  Flask, render_template, redirect, session, url_for, request
from geopy.geocoders import Nominatim
from database import Database


app = Flask(__name__)
geolocator = Nominatim(user_agent="geoapiExercises")
db = Database(ssl_ca_path='DigiCertGlobalRootG2.crt.pem', ip="localhost", username="root", password="*****", database="DATA")


@app.route("/", methods=["GET"])
def root():
   
   #db.get_all_dev_EUI_values()
   sensor_data = db.get_all__data(reverse=True)

   return render_template("sensor-data.html", sensor_data=sensor_data)

@app.route("/map/showone/<id>", methods=["GET"])
def map_one(id):
   sensor_data = db.get_data_by_dev_ID(id)
   dev_EUI_list = db.get_all_dev_EUI_values()
   return render_template("map.html", sensor_data=sensor_data, dev_EUI_list=dev_EUI_list)



@app.route("/map/showall", methods=["GET"])
def map_all():
   
   sensor_data = db.get_all__data()
   dev_EUI_list = db.get_all_dev_EUI_values()
   return render_template("map.html", sensor_data=sensor_data, dev_EUI_list=dev_EUI_list)

@app.route("/map/show-last-24h", methods=["GET"])
def map_all_24h():
   sensor_data = db.get_last_24h_data()
   dev_EUI_list = db.get_all_dev_EUI_values()
   return render_template("map.html", sensor_data=sensor_data, dev_EUI_list=dev_EUI_list)


@app.route("/map/<dev_EUI>", methods=["GET"])
def map_dev_eui(dev_EUI):
   sensor_data = db.get_data_by_dev_EUI(dev_EUI)
   dev_EUI_list = db.get_all_dev_EUI_values()
   return render_template("map.html", sensor_data=sensor_data, dev_EUI_list=dev_EUI_list)


@app.route("/project", methods=["GET"])
def map():
   return render_template("project-voorstel.html")


@app.route("/api", methods=["POST"])
def api():

   content = request.json # content die wordt doorgesturen via POST (json)

    # Nuttige Data
   latitude = content["decoded"]["payload"]["latitude"]
   longitude = content["decoded"]["payload"]["longitude"]
   temp = content["decoded"]["payload"]["temp"]
   dev_eui = content["dev_eui"]
   location = geolocator.reverse(str(latitude)+","+str(longitude)).raw['address'].get("city", "")


    #city = location.get('city', '') #https://www.geeksforgeeks.org/get-the-city-state-and-country-names-from-latitude-and-longitude-using-python/

   # Stuurt de data naar de database
   db.send_data(dev_EUI=dev_eui, lat=latitude, long=longitude, location=location, temp=temp)

   
   return "200"






if __name__ == '__main__':
    app.run(debug=True, port=80, host="0.0.0.0")

