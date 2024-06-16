import app.settings as settings
import sqlite3


def init_db_connection():

    db = sqlite3.connect(settings.DB_PATH)
    db.execute("CREATE TABLE if not EXISTS movies (asin TEXT, data TEXT)")
    return db
