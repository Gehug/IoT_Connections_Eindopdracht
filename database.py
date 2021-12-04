from flask_mysqldb import MySQL
import MySQLdb
from decimal import Decimal
import datetime




class Database():
    def __init__(self, app, key, ip, username, password, database, port=3306): # Geef de gevenesns in van de database
        self.db = MySQL(app)
        
        
        self.master = app
        self.master.secret_key = key
        self.master.config["MYSQL_HOST"] = ip
        self.master.config["MYSQL_USER"] = username
        self.master.config["MYSQL_PASSWORD"] = password
        self.master.config["MYSQL_DB"] = database
        self.master.config["MYSQL_CONNECT_TIMEOUT"] = 1
    

     

    def _connect_to_db(self):
        pass

    def _disconnect_to_db(self):
        pass

    # def _convert_mysql_decimal_to_float(self, object):
    #     # if (decimal_object == None):
    #     #     return None
    #     # else:
    #     #     return float(decimal_object)
    #     row_data = []
    #     if type(object) is Decimal:
    #         row_data.append(float(object))
    #     elif type(object) is datetime.datetime:
    #         row_data.append(str(dat))



    def send_data(self, dev_EUI, lat, long, location, temp): # stuurt sensor data naar database
        cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO SENSOR_DATA (DEV_EUI, LATITUDE, LONGITUDE, LOCATION, TEMP) VALUES (%s, %s, %s, %s, %s)", (dev_EUI, lat, long, location, temp))
        self.db.connection.commit()
        reponse = cursor.fetchone()


    def get_all__data(self): # Haalt alle sensor data uit de database 
        
        cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        print("test")
        cursor.execute("SELECT DEV_EUI, CAST(LATITUDE AS CHAR) AS LATITUDE, CAST(LONGITUDE AS CHAR) AS LONGITUDE, LOCATION, CAST(PUBLISH_TIME AS CHAR) AS PUBLISH_TIME, CAST(TEMP AS CHAR) AS TEMP FROM SENSOR_DATA")
        rows = cursor.fetchall()

    

        
        rows = tuple(reversed(rows)) # zorgt er voor dat nieuwste informatie boven komt te staan
        good_data = []
        interval = 0
        for row in rows: # Gaat door alle data die is ontvangen door database, en vormt dit om naar de data die we nodig hebben 
            pub_time = str(row["PUBLISH_TIME"]).split()
            current_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).split()

            if pub_time[0] == current_time[0]: # Als de pub_time datum overeen komt met de current_data 
                time1 = datetime.datetime.strptime(pub_time[1],"%H:%M:%S")
                time2 = datetime.datetime.strptime(current_time[1],"%H:%M:%S")
                interval = time2 - time1


            else: 
                time1 = datetime.datetime.strptime(pub_time[0],"%Y-%m-%d")
                time2 = datetime.datetime.strptime(current_time[0],"%Y-%m-%d")
                interval = time2 - time1
                interval = str(interval).split()[0] # Ze splitten de informatie "1 day, 0:00:00" in aangezien we enkel intressen hebben in de "1 day"



            
            good_data.append({"dev_EUI": row["DEV_EUI"], "lat": float(row["LATITUDE"]), "long": float(row["LONGITUDE"]), "location": row["LOCATION"],"time": row["PUBLISH_TIME"], "temp": float(row["TEMP"]), "interval": interval})
        return good_data



    def get_data_by_dev_EUI(self, dev_EUI): # geeft enkel de data van een bepaald device
        pass

    def get_amount_of_data(): # Geeft een getal hoeveel sensor data er is verstuurd
        pass
    



 


