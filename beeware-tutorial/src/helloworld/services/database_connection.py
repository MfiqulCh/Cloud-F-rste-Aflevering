import mysql.connector
from mysql.connector import connect
import ssl 

db_password = 'Thisthepassword3'

sql_query_template = {}

sql_query_template['get_dcr_role'] = "SELECT Role FROM DCRUsers WHERE Email = %(email)s"
# TODO: fill in these templates with the right SQL query
sql_query_template['update_dcr_role'] = "UPDATE DCRUsers SET Role = %(role)s WHERE Email = %(email)s"
sql_query_template['get_all_instances'] = "SELECT Instances.InstanceID, Instances.IsInValidState, UserInstances.Email FROM Instances INNER JOIN UserInstances ON Instances.InstanceID = UserInstances.InstanceID"
sql_query_template['get_instances_for_user'] = "SELECT Instances.InstanceID, Instances.IsInValidState FROM Instances INNER JOIN UserInstances ON Instances.InstanceID = UserInstances.InstanceID WHERE UserInstances.Email = %(email)s"
sql_query_template['insert_instance'] = "INSERT INTO Instances (InstanceID, IsInValidState) VALUES (%(id)s, %(valid)s)"
sql_query_template['insert_instance_for_user'] = "INSERT INTO UserInstances (Email, InstanceID) VALUES (%(email)s, %(instance_id)s)"
sql_query_template['update_instance'] = "UPDATE Instances SET IsInValidState = %(valid)s WHERE InstanceID = %(id)s"
sql_query_template['delete_instance_from_user_instance'] = "DELETE FROM UserInstances WHERE InstanceID = %(id)s"
sql_query_template['delete_instance'] = "DELETE FROM Instances WHERE InstanceID = %(id)s"

def db_connect():
    from pathlib import Path
    resources_folder = Path(__file__).parent.resolve()
    cert_filepath = str(resources_folder.joinpath("DigiCertGlobalRootCA.crt.pem"))
    cnx = mysql.connector.connect(user="Group3",
                                  password=db_password,
                                  host="group3.mysql.database.azure.com",
                                  port=3306,
                                  database="group3",
                                  ssl_ca=cert_filepath,
                                  ssl_disabled=False)
    print(f'[i] cnx is connected: {cnx.is_connected()}')
    return cnx

def get_dcr_role(email):
    try:
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(sql_query_template['get_dcr_role'], {'email':email})
        query_result = cursor.fetchone()[0]
        cursor.close()
        cnx.close()
        return query_result
    except Exception as ex:
        print(f'[x] error get_dcr_role! {ex}')
        return None
    
def update_dcr_role(email,role):
    try:
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(sql_query_template['update_dcr_role'], {'role':role,'email':email}, multi=False)
        cnx.commit()
        cursor.close()
        cnx.close()
    except Exception as ex:
        print(f'[x] error update_dcr_role! {ex}')
        
def get_all_instances():
    try:
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(sql_query_template['get_all_instances'])
        query_result = cursor.fetchall()
        cursor.close()
        cnx.close()
        return query_result
    except Exception as ex:
        print(f'[x] error get_all_instances! {ex}')
        return None
    
def get_instances_for_user(email):
    try:
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(sql_query_template['get_instances_for_user'], {'email':email})
        query_result = cursor.fetchall()
        cursor.close()
        cnx.close()
        return query_result
    except Exception as ex:
        print(f'[x] error get_instances_for_user! {ex}')
        return None
    
def insert_instance(id, valid, email):
    try:
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(sql_query_template['insert_instance'], {'id':id,'valid':valid}, multi=False)
        cursor.execute(sql_query_template['insert_instance_for_user'], {'email':email,'instance_id':id}, multi=False)
        cnx.commit()
        cursor.close()
        cnx.close()
    except Exception as ex:
        print(f'[x] error insert_instance! {ex}')
        
def update_instance(id, valid):
    try:
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(sql_query_template['update_instance'],{'id':id,'valid':valid}, multi=False)
        cnx.commit()
        cursor.close()
        cnx.close()
    except Exception as ex:
        print(f'[x] error update_instance! {ex}')
        
def delete_instance(id):
    try:
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(sql_query_template['delete_instance_from_user_instance'], {'id':id}, multi=False)
        cursor.execute(sql_query_template['delete_instance'], {'id':id}, multi=False)
        cnx.commit()
        cursor.close()
        cnx.close()
    except Exception as ex:
        print(f'[x] error delete_instance! {ex}')