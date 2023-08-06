import mysql.connector
import os
from dotenv import load_dotenv
from logger_local_python_package.localLogger import logger_local
load_dotenv()




class database():
    
    def connect_to_database(self):
        try:
            host=os.getenv("RDS_HOSTNAME")if os.getenv("RDS_HOSTNAME") else " "
            user=os.getenv("RDS_USERNAME")if os.getenv("RDS_USERNAME") else " "
            password=os.getenv("RDS_PASSWORD")if os.getenv("RDS_PASSWORD") else " "
            object1={
                'host':os.getenv("RDS_HOSTNAME"),
                'user':os.getenv("RDS_USERNAME"),
                'password':os.getenv("RDS_PASSWORD"),
                'component_id':112
            }
            logger_local.start(object=object1)
            mydb = mysql.connector.connect(
            host=os.getenv("RDS_HOSTNAME"),
            user=os.getenv("RDS_USERNAME"),
            password=os.getenv("RDS_PASSWORD")
        )
            object2={
                'host':mydb._host,
                'component_id':112

            }
            logger_local.end(object=object2)
            return mydb
        except Exception as e:
            st=str(host+" "+user+" "+password)
            logger_local.exception(st,object=e)

        
