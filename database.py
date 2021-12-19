# from flask_mysqldb import MySQL
# import MySQLdb
import mysql.connector
from mysql.connector import errorcode
from decimal import Decimal
import datetime




class Database():
    def __init__(self, ssl_ca_path, ip, username, password, database, port=3306): # Geef de gevenesns in van de database


        self.config = {
            'host': ip,
            'user': username,
            'password': password,
            'database': database,
            'client_flags': [mysql.connector.ClientFlag.SSL],
            'ssl_ca': ssl_ca_path 
        }
    

     

    def _connect_to_db(self):

        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor(dictionary=True)

    def _disconnect_to_db(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def _calc_delte_time(self, pub_time): # Deze functie zal het verschil van tijd berekenen van wanneer de data in de database is gepubliseerd en het momentele tijd stipt (hiermee kan je berekenen hoe oud de sensor data is)
        current_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).split() # Gaat de momentele tijd + datum ophalen en splitsen in een lijst bv: [datum, tijd]

        if pub_time[0] == current_time[0]: # Als de pub_time datum overeen komt met de current_data 
            time1 = datetime.datetime.strptime(pub_time[1],"%H:%M:%S")
            time2 = datetime.datetime.strptime(current_time[1],"%H:%M:%S")
            interval = time2 - time1


        else: 
            time1 = datetime.datetime.strptime(pub_time[0],"%Y-%m-%d")
            time2 = datetime.datetime.strptime(current_time[0],"%Y-%m-%d")
            interval = time2 - time1
            interval = str(interval).split()[0] # Ze splitten de informatie "1 day, 0:00:00" in aangezien we enkel intressen hebben in de "1 day"

        return interval



  


    def send_data(self, dev_EUI, lat, long, location, temp): # stuurt sensor data naar database
        self._connect_to_db()

        self.cursor.execute("INSERT INTO SENSOR_DATA (DEV_EUI, LATITUDE, LONGITUDE, LOCATION, TEMP) VALUES (%s, %s, %s, %s, %s)", (dev_EUI, lat, long, location, temp))
        self.conn.commit()
        reponse = self.cursor.fetchone()

    

        return reponse


    def get_all__data(self, reverse=False): # Haalt alle sensor data uit de database 
        self._connect_to_db()


        self.cursor.execute("SELECT ID, DEV_EUI, CAST(LATITUDE AS CHAR) AS LATITUDE, CAST(LONGITUDE AS CHAR) AS LONGITUDE, LOCATION, CAST(PUBLISH_TIME AS CHAR) AS PUBLISH_TIME, CAST(TEMP AS CHAR) AS TEMP FROM SENSOR_DATA")
        rows = self.cursor.fetchall()

    

        if reverse == True:
            rows = tuple(reversed(rows)) # zorgt er voor dat nieuwste informatie boven komt te staan

        
        good_data = []
        interval = 0
        for row in rows: # Gaat door alle data die is ontvangen door database, en vormt dit om naar de data die we nodig hebben 
            pub_time = str(row["PUBLISH_TIME"]).split() # Neemt de publish time van de sensor data
            interval = self._calc_delte_time(pub_time) # berekend de interval 

    
            good_data.append({"id": row["ID"],"dev_EUI": row["DEV_EUI"], "lat": float(row["LATITUDE"]), "long": float(row["LONGITUDE"]), "location": row["LOCATION"],"time": row["PUBLISH_TIME"], "temp": float(row["TEMP"]), "interval": interval})

            
            # self._disconnect_to_db()
            
            
        return good_data

    def get_last_24h_data(self):
        self._connect_to_db()
        self.cursor.execute("SELECT DEV_EUI, CAST(LATITUDE AS CHAR) AS LATITUDE, CAST(LONGITUDE AS CHAR) AS LONGITUDE, LOCATION, CAST(PUBLISH_TIME AS CHAR) AS PUBLISH_TIME, CAST(TEMP AS CHAR) AS TEMP FROM SENSOR_DATA WHERE PUBLISH_TIME >= now() - INTERVAL 1 DAY")

        rows = self.cursor.fetchall()



        good_data = []
        interval = 0
        for row in rows: # Gaat door alle data die is ontvangen door database, en vormt dit om naar de data die we nodig hebben 
            pub_time = str(row["PUBLISH_TIME"]).split() # Neemt de publish time van de sensor data
            interval = self._calc_delte_time(pub_time) # berekend de interval 

    
            good_data.append({"dev_EUI": row["DEV_EUI"], "lat": float(row["LATITUDE"]), "long": float(row["LONGITUDE"]), "location": row["LOCATION"],"time": row["PUBLISH_TIME"], "temp": float(row["TEMP"]), "interval": interval})

   
            
        return good_data



    def get_all_dev_EUI_values(self): # Geeft alle dev_EUI waardes terug die in de database voorkomen
        self._connect_to_db()
        self.cursor.execute("SELECT DEV_EUI FROM DATA.SENSOR_DATA GROUP BY DEV_EUI")
        rows = self.cursor.fetchall()
        good_data = []
        for row in rows:
            good_data.append(row["DEV_EUI"])
        return good_data
            



    def get_data_by_dev_EUI(self, dev_EUI): # geeft enkel de data van een bepaald device
        self._connect_to_db()
        self.cursor.execute(f"SELECT DEV_EUI, CAST(LATITUDE AS CHAR) AS LATITUDE, CAST(LONGITUDE AS CHAR) AS LONGITUDE, LOCATION, CAST(PUBLISH_TIME AS CHAR) AS PUBLISH_TIME, CAST(TEMP AS CHAR) AS TEMP FROM SENSOR_DATA WHERE DEV_EUI='{dev_EUI}'")
        rows = self.cursor.fetchall()


        good_data = []
        interval = 0
        for row in rows: # Gaat door alle data die is ontvangen door database, en vormt dit om naar de data die we nodig hebben 
            pub_time = str(row["PUBLISH_TIME"]).split() # Neemt de publish time van de sensor data
            interval = self._calc_delte_time(pub_time) # berekend de interval 

    
            good_data.append({"dev_EUI": row["DEV_EUI"], "lat": float(row["LATITUDE"]), "long": float(row["LONGITUDE"]), "location": row["LOCATION"],"time": row["PUBLISH_TIME"], "temp": float(row["TEMP"]), "interval": interval})

   
            
        return good_data

    def get_data_by_dev_ID(self, id):
        self._connect_to_db()
        self.cursor.execute(f"SELECT DEV_EUI, CAST(LATITUDE AS CHAR) AS LATITUDE, CAST(LONGITUDE AS CHAR) AS LONGITUDE, LOCATION, CAST(PUBLISH_TIME AS CHAR) AS PUBLISH_TIME, CAST(TEMP AS CHAR) AS TEMP FROM SENSOR_DATA WHERE ID='{id}'")
        rows = self.cursor.fetchall()
        good_data = []

        for row in rows: # Gaat door alle data die is ontvangen door database, en vormt dit om naar de data die we nodig hebben 
            pub_time = str(row["PUBLISH_TIME"]).split() # Neemt de publish time van de sensor data
            interval = self._calc_delte_time(pub_time) # berekend de interval 

    
            good_data.append({"dev_EUI": row["DEV_EUI"], "lat": float(row["LATITUDE"]), "long": float(row["LONGITUDE"]), "location": row["LOCATION"],"time": row["PUBLISH_TIME"], "temp": float(row["TEMP"]), "interval": interval})

   
            
        return good_data


    




    def get_amount_of_data(): # Geeft een getal hoeveel sensor data er is verstuurd
        pass
    



 


