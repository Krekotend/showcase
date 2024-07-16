import psycopg2
from config import load_config


def join_base():
    try:
        connection = psycopg2.connect(host=load_config().db.host, user=load_config().db.userb,
                                      port=load_config().db.port,
                                      password=load_config().db.password, database=load_config().db.db_name)
        connection.autocommit = True

        return connection

    except Exception as ex:
        print('This is ERROR ', ex)


def write_users_table(name: str, tg_id: int, lang: str):
    with join_base().cursor() as cursor:
        insert_sql = 'SELECT user_name FROM users WHERE tg_id = %s;'
        cursor.execute(insert_sql, (tg_id,))
        if cursor.fetchone() == None:
            insert_sql = 'INSERT INTO users (user_name,tg_id,lang) VALUES (%s,%s,%s);'
            value = (name, tg_id, lang)
            cursor.execute(insert_sql, value)
            return lang
        else:
            update_query = 'UPDATE users SET lang = %s WHERE tg_id = %s;'
            value = (lang, tg_id)
            cursor.execute(update_query, value)
            return lang


def get_lang(tg_id):
    with join_base().cursor() as cursor:
        lang_sql = 'SELECT lang FROM users WHERE tg_id = %s;'
        cursor.execute(lang_sql, (tg_id,))
        return cursor.fetchone()[0]


def write_media_table(photo_id: str, photo_name: str, disc: str):
    with join_base().cursor() as cursor:
        check_name_sql = 'SELECT name FROM media WHERE name = %s;'
        cursor.execute(check_name_sql, (photo_name,))
        if cursor.fetchone() is None:
            insert_sql = 'INSERT INTO media (id, name, discript) VALUES (%s, %s, %s);'
            values = (photo_id, photo_name, disc)
            try:
                cursor.execute(insert_sql, values)
                connection = cursor.connection
                connection.commit()
                return True
            except Exception as e:
                print(f"Error inserting media: {e}")
                return False
        elif photo_name in ['mainwall', 'lang']:
            update_sql = 'UPDATE media SET id = %s, name = %s, discript = %s WHERE name = %s;'
            values = (photo_id, photo_name, disc, photo_name)
            try:
                cursor.execute(update_sql, values)
                connection = cursor.connection
                connection.commit()
                return True
            except Exception as e:
                print(f"Error updating media: {e}")
                return False


def write_item(article: int, name: str):
    with join_base().cursor() as cursor:
        insert_sql = 'SELECT article FROM items WHERE article = %s;'
        cursor.execute(insert_sql, (article,))
        if cursor.fetchone() == None:
            insert_sql = 'INSERT INTO items (article,name) VALUES (%s,%s);'
            value = (article, name)
            cursor.execute(insert_sql, value)


def add_desc_item(article: int, desc: str):
    with join_base().cursor() as cursor:
        update_query = 'UPDATE items SET discript = %s WHERE article = %s'
        cursor.execute(update_query, (desc, article))


def add_pay_item(article: int, pay: list):
    with join_base().cursor() as cursor:
        insert_query = 'UPDATE items SET pay = %s WHERE article = %s'
        cursor.execute(insert_query, (pay, article))


def add_photo_item(article: int, photo: str):
    with join_base().cursor() as cursor:
        update_query = 'UPDATE items SET images = array_append(images, %s) WHERE article = %s'
        cursor.execute(update_query, (photo, article))


def take_media(name: str):
    with join_base().cursor() as cursor:
        insert_sql = f'SELECT id FROM media WHERE name = %s;'
        cursor.execute(insert_sql, (name,))
        return cursor.fetchone()[0]


def take_info_items() -> list:
    with join_base().cursor() as cursor:
        req_sql = f'SELECT article,name FROM items;'
        cursor.execute(req_sql)
        return cursor.fetchall()


def take_item(article):
    with join_base().cursor() as cursor:
        req_sql = f'SELECT name,article,discript,pay,images FROM items WHERE article = %s;'
        cursor.execute(req_sql, (article,))
        return cursor.fetchall()


def del_item(article):
    with join_base().cursor() as cursor:
        req_sql = f'DELETE FROM items WHERE article = %s;'
        cursor.execute(req_sql, (article,))


def take_rews():
    with join_base().cursor() as cursor:
        insert_sql = f'SELECT id FROM media WHERE discript = %s;'
        cursor.execute(insert_sql, ('rews',))
        return [img[0] for img in cursor.fetchall()]


if __name__ == 'main':
    pass
