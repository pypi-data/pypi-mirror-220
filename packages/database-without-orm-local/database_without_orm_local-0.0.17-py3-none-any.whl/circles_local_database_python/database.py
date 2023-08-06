import mysql.connector
import os
from dotenv import load_dotenv
from logger_local_python_package.LoggerLocal import logger_local
load_dotenv()

DATABASE_WITHOUT_ORM_COMPONENT_ID = 112


class database():
    def connect_to_database(self):
        logger_local.init(
            object={'component_id': DATABASE_WITHOUT_ORM_COMPONENT_ID})
        try:
            host = os.getenv("RDS_HOSTNAME")if os.getenv(
                "RDS_HOSTNAME") else " "
            user = os.getenv("RDS_USERNAME")if os.getenv(
                "RDS_USERNAME") else " "
            password = os.getenv("RDS_PASSWORD")if os.getenv(
                "RDS_PASSWORD") else " "
            object1 = {
                'host': os.getenv("RDS_HOSTNAME"),
                'user': os.getenv("RDS_USERNAME")
            }
            logger_local.start(object=object1)
            mydb = mysql.connector.connect(
                host=os.getenv("RDS_HOSTNAME"),
                user=os.getenv("RDS_USERNAME"),
                password=os.getenv("RDS_PASSWORD")
            )
            logger_local.end(object={'mydb': str(mydb)})
            return mydb
        except Exception as e:
            logger_local.exception(
                str("host: "+host+" user: "+user+" password: "+password), object=e)
