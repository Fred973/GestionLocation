import os
from soft.constant import DB_USER, DB_HOSTNAME, DB_PORT, DB_PASSWORD, DB_NAME, db_save_path
from soft.func.date_func import today_datetime


def create_db_save_name():
    db_save_name = 'gestion_loc_{}.sql'.format(today_datetime())
    return db_save_name


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


def delete_db(db_name: str):
    os.remove(os.path.join(db_save_path, db_name))