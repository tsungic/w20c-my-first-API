  
from flask import Flask , request,Response
import json
import random
import mariadb
import dbcreds


app = Flask(__name__)

# animals=[{"name":"Snake"},{"name":"Owl"}]


@app.route('/animals',methods = ['POST', 'GET','PATCH','DELETE'])
def animals_route():
    if request.method == "GET":
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM animals")
            result = cursor.fetchall()
            animals=[]
            for item in result : 
                animal={ "id" : item[0] , "name" : item[1]}
                animals.append(animal)
        except mariadb.OperationalError as e:
            print("Error connecting to MariaDB Platform: {e}")
        except:
            print("an unanticipated error has occurred")
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
                return Response(json.dumps(animals,default=str) ,mimetype="application/json",status=200)
    elif request.method == "POST" : 
        animal= request.json
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO animals(name) VALUES (?)",[animal["name"],])
            conn.commit()        

        except mariadb.OperationalError as e:
            print("Error connecting to MariaDB Platform: {e}")
        except:
            print("an unanticipated error has occurred")
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
                return Response("Success",mimetype="text/html",status=201)
    elif request.method == "PATCH":
        animal= request.json
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("UPDATE animals SET name=? WHERE id = ?",[animal["name"],animal["id"]])
            conn.commit()
            
        except mariadb.OperationalError as e:
            print("Error connecting to MariaDB Platform: {e}")
        except:
            print("an unanticipated error has occurred")
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
                return Response("Update success",mimetype="text/html",status=202)
    elif request.method=="DELETE":
        animal_id = request.json["id"]
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM animals WHERE id = ?",[animal_id])
            conn.commit()
            
        except mariadb.OperationalError as e:
            print("Error connecting to MariaDB Platform: {e}")
        except:
            print("an unanticipated error has occurred")
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
                return Response("Delete success",mimetype="text/html",status=203)
