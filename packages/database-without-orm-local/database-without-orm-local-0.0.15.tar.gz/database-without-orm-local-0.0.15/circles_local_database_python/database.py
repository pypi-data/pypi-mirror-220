import mysql.connector
import os
from dotenv import load_dotenv
from logger_local_python_package.LocalLogger import logger_local
load_dotenv()

component_id=112


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
                'component_id' :component_id
            }
            logger_local.start(object=object1)
            mydb = mysql.connector.connect(
            host=os.getenv("RDS_HOSTNAME"),
            user=os.getenv("RDS_USERNAME"),
            password=os.getenv("RDS_PASSWORD")
        )
            logger_local.end(object={'component_id' :component_id})
            return mydb
        except Exception as e:
            logger_local.exception(str(host+" "+user+" "+password),object=e)

        
