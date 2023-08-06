from circles_local_database_python.database import database
from CirclesGetCountryName.opencage_get_country_name import Country
from dotenv import load_dotenv
from logger_local_python_package.localLogger import _local_logger as local_logger
from functools import wraps
load_dotenv()


def log_function_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        local_logger.start("Function %s started." % func.__name__)
        result = func(*args, **kwargs)  # Execute the function
        local_logger.end("Function %s completed." % func.__name__)
        return result
    return wrapper


class Importer:
    def __init__(self, source):
        self.source_name = source

    @log_function_execution
    def insert_new_entity(self, entity_type_name):
        object1={
            'entity_type_name':entity_type_name
        }
        local_logger.start(object=object1)
        database_conn = database()
        db = database_conn.connect_to_database()
        cursor = db.cursor()

        cursor.execute("SELECT entity_type_id FROM {} WHERE entity_type_name = '{}'".format('entity_type.entity_type_ml_table', entity_type_name))
        entity_type_id = cursor.fetchone()

        if not entity_type_id:
            query_entity = "INSERT INTO {}(`created_user_id`,`updated_user_id`)" \
                              " VALUES (1, 1)".format('entity_type.entity_type_table')
            cursor.execute(query_entity)
            db.commit()

            last_inserted_id = cursor.lastrowid
            query_entity_ml = "INSERT INTO {}(`entity_type_name`,`entity_type_id`,`lang_code`,`created_user_id`,`updated_user_id`)" \
                              " VALUES (%s, %s, %s, 1, 1)".format('entity_type.entity_type_ml_table')
            cursor.execute(query_entity_ml, (entity_type_name, last_inserted_id, 'en'))
            local_logger.end("End Inserted Entity %s ." % entity_type_name)
            db.commit()
        else:
            local_logger.end("Entity %s already exist." % entity_type_name)
        db.close()

    @log_function_execution
    def insert_new_source(self):
        local_logger.start("Start insert_new_source()")
        database_conn = database()
        db = database_conn.connect_to_database()
        cursor = db.cursor()

        cursor.execute("SELECT source_id FROM {} WHERE source_name = '{}'".format('source.source_ml_table', self.source_name))
        source_id = cursor.fetchone()

        if not source_id:
            query_importer_source = "INSERT INTO {}(`created_user_id`,`updated_user_id`)" \
                              " VALUES (1, 1)".format('source.source_table')
            cursor.execute(query_importer_source)
            db.commit()

            last_inserted_id = cursor.lastrowid
            query_importer_source_ml = "INSERT INTO {}(`source_name`,`source_id`,`created_user_id`,`updated_user_id`)" \
                              " VALUES (%s, %s, 1, 1)".format('source.source_ml_table')
            cursor.execute(query_importer_source_ml, (self.source_name, last_inserted_id))
            db.commit()
            local_logger.end("end insert_new_source %s."%self.source_name)
        else:
            local_logger.end("Source %s already exist." % self.source_name)
        db.close()

    @log_function_execution
    def insert_record_source(self, location, entity_type_name, entity_id, url):
        
        object1={
            'entity_type_name':entity_type_name,
            'entity_id':entity_id,
            'url':url,
        }
        local_logger.start(object=object1)
        database_conn = database()
        db = database_conn.connect_to_database()
        cursor = db.cursor()

        cursor.execute("SELECT source_id FROM {} WHERE source_name = '{}'".format('source.source_ml_table', self.source_name))
        source_id = cursor.fetchone()

        country_name =  Country.get_country_name(location)
        cursor.execute(
            "SELECT id FROM {} WHERE name = '{}'".format('location.country_table', country_name))
        country_id = cursor.fetchone()

        cursor.execute("SELECT entity_type_id FROM {} WHERE entity_type_name = '{}'".format('entity_type.entity_type_ml_table', entity_type_name))
        entity_type_id = cursor.fetchone()

        query_importer = "INSERT INTO {}(`source_id`,`country_id`,`entity_type_id`,`entity_id`,`url`,`created_user_id`,`updated_user_id`)" \
                          " VALUES (%s, %s, %s, %s, %s, 1, 1)".format('importer.importer_table')

        cursor.execute(query_importer, (source_id[0], country_id[0], entity_type_id[0], entity_id, url))

        db.commit()
        db.close()
        local_logger.end("Function insert_record_source() ended")


if __name__ == "__main__":
    pass

