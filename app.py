from flask import  Flask, render_template, redirect, session, url_for, request
from geopy.geocoders import Nominatim
from database import Database


app = Flask(__name__)
geolocator = Nominatim(user_agent="geoapiExercises")
db = Database(app=app, key="verry_secret_key", ip="*****", username="****", password="******", database="DATA")



@app.route("/", methods=["GET"])
def root():
   sensor_data = db.get_all__data()

   return render_template("sensor-data.html", sensor_data=sensor_data)

@app.route("/map", methods=["GET"])
def project():
   sensor_data = db.get_all__data()
   return render_template("map.html", sensor_data=sensor_data)

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
   location = geolocator.reverse(str(latitude)+","+str(longitude)).raw['address'].get("village", "")


    #city = location.get('city', '') #https://www.geeksforgeeks.org/get-the-city-state-and-country-names-from-latitude-and-longitude-using-python/

      # Stuurt de data naar de database
   db.send_data(dev_EUI=dev_eui, lat=latitude, long=longitude, location=location, temp=temp)

   
   return "200"






if __name__ == '__main__':
    app.run(debug=True, port=80, host="0.0.0.0")

