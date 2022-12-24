import os
from soft import db, app
from soft.constant import DB_USER, DB_HOSTNAME, DB_PORT, DB_PASSWORD, DB_NAME, db_save_path, table_save_path
from soft.func.date_func import today_datetime, convert_date_str_to_date_to_string


def create_db_save_name():
    db_save_name = 'gestion_loc_{}.sql'.format(today_datetime())
    return db_save_name


def create_table_name(table_name: str):
    table_save_name = 'gestion_loc_{}-{}.sql'.format(today_datetime(), table_name)
    return table_save_name


def import_db():
    # Create DB save file
    os.popen(
        "mysqldump -h {} -P {} -u {} -p{} {} > {}".format(
            DB_HOSTNAME,
            DB_PORT,
            DB_USER,
            DB_PASSWORD,
            DB_NAME,
            db_save_path + create_db_save_name()
        )
    )


def import_table(table_name: str):
    # Create DB save file
    os.popen(
        "mysqldump -h {} -P {} -u {} -p{} {} {} > {}".format(
            DB_HOSTNAME,
            DB_PORT,
            DB_USER,
            DB_PASSWORD,
            DB_NAME,
            table_name,
            table_save_path + create_table_name(table_name)
        )
    )


def export_db(db_name: str):
    os.popen(
        "mysql -h {} -P {} -u {} -p{} {} < {}".format(
            DB_HOSTNAME,
            DB_PORT,
            DB_USER,
            DB_PASSWORD,
            DB_NAME,
            db_save_path + db_name
        )
    )


def export_table_to_db(file_name: str, table_name: str):
    print("mysql -h {} -P {} -u {} -p{} {} {} < {}".format(
            DB_HOSTNAME,
            DB_PORT,
            DB_USER,
            DB_PASSWORD,
            DB_NAME,
            table_name,
            table_save_path + file_name
        ))
    os.popen(
        "mysql -h {} -P {} -u {} -p{} {} < {}".format(
            DB_HOSTNAME,
            DB_PORT,
            DB_USER,
            DB_PASSWORD,
            DB_NAME,
            table_save_path + file_name
        )
    )


def delete_db(db_name: str):
    os.remove(os.path.join(db_save_path, db_name))


def delete_table(table_name: str):
    os.remove(os.path.join(table_save_path, table_name))


def get_date_from_db_save_name(d):
    date_ = d.replace('gestion_loc_', '')
    result = date_[:8]
    return convert_date_str_to_date_to_string(result)

def get_table_name(t: str):
    table_name = t.replace('gestion_loc_', '')
    result = table_name[14:]
    return result.replace('.sql', '')


def get_table_list():
    with app.app_context():
        table_list = db.engine.table_names()
        return table_list
