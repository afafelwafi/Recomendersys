import itertools
import psycopg2
import psycopg2.extras
from psycopg2.extensions import register_adapter, register_type, AsIs
import numpy
import pandas as pd
import operator
#
STORE_ID=-1
#sizes_sheet= {'men': pd.read_excel("C:\\Users\\afafe\\Desktop\\stage\\taille.xlsx", sheet_name='H', header=1, dtype={'Vestes FR':str, 'Vestes US':str, 'Vestes IT':str, 'Vestes UK':str, 'Vestes Jap':str, 'Chemises FR':str, 'Chemises US':str, 'Pantalons FR':str, 'Pantalons US':str, 'Pantalons IT':str}),\
#             'women': pd.read_excel("C:\\Users\\afafe\\Desktop\\stage\\taille.xlsx", sheet_name='F', header=1, dtype={'Tops FR':str, 'Tops US':str, 'Tops IT':str, 'Tops UK':str, 'Tops JAP':str, 'Pantalons FR':str, 'Pantalons US':str}),\
#             'shoes': pd.read_excel("C:\\Users\\afafe\\Desktop\\stage\\taille.xlsx", sheet_name='Chaussures', header=1, dtype={'FR':str, 'US':str, 'UK':str, 'IT':str, 'Tops JAP':str})}
#
#sizes_kept = ['XXXS', 'XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL']

def _addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)

def _addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)

def _connect_database(db_name='postgres', username=None, password=None, host=None, port=None, database_url=None):
    try:
        if database_url != None:
            connectionString= database_url
        else:
            connectionString = "dbname='" + db_name + "'"
            if username != None and username != '':
                connectionString += " user='" + username + "'"
            if host != None and host != '':
                connectionString += " host='" + host + "'"
            if password != None and password != '':
                connectionString += " password='" + password + "'"
            if port != None:
                connectionString += " port='" + str(port) + "'"

        connection  = psycopg2.connect(connectionString)
        register_adapter(numpy.float64, _addapt_numpy_float64)
        register_adapter(numpy.int64, _addapt_numpy_int64)

        DEC2FLOAT = psycopg2.extensions.new_type(
            psycopg2.extensions.DECIMAL.values,
            'DEC2FLOAT',
            lambda value, curs: float(value) if value is not None else None)

        NewDate = psycopg2.extensions.new_type((1114,), 'TIMESTAMP', psycopg2.STRING)

        register_type(NewDate)
        register_type(DEC2FLOAT)
    except:
        raise

    return connection

def update_categories_6(storeId):
    products=get_products(storeId)
    for p in products:
        cursor.execute("UPDATE products SET normalized_category=%s WHERE store_id=%s AND product_id=%s",(p['category'],storeId,p['product_id'],))
    connection.commit()
 
def update_categories_except_8_and_6(storeId):
    cat=get_categories(storeId)
    products=get_products(storeId)
    for p in products:
        for c in cat:
            if c[0]==p['product_id']:
                cursor.execute("UPDATE products SET normalized_category=%s WHERE store_id=%s AND product_id=%s",(c[1],storeId,c[0],))
    connection.commit()
    
def update_categories_8(storeId=8):
    cat=get_categories(storeId)
    products=get_products(storeId)
    for p in products:
        for c in cat:
            if c[0]==p['product_id']:
                if c[1]!='vetements':
                    curso*r.execute("UPDATE products SET normalized_category=%s WHERE store_id=%s AND product_id=%s",(c[1],storeId,c[0],))
    connection.commit()
    
    
    
def popular_products(storeId):
    cursor.execute("SELECT products_liked FROM preferences WHERE store_id=%s AND products_liked IS NOT NULL",(storeId,))
    products_liked=cursor.fetchall()
    Liste=[p['products_liked'] for p in products_liked]
    flat_liste=[s for sublist in Liste for s in sublist]
    dic_pop={p:flat_liste.count(p) for p in flat_liste} 
    sorted_pop = sorted(dic_pop.items(), key=operator.itemgetter(1),reverse=True)
    liste=[s[0]  for s in sorted_pop[:4]]
    cursor.execute("SELECT picture_url FROM products WHERE product_id IN (%s,%s,%s,%s)",(tuple(liste)))
    return cursor.fetchall()
    

    
    
    
    cursor.execute(query,(storeId,storeId,))
    return cursor.fetchall()
def normalized_categories(storeId):
    query = 'SELECT DISTINCT normalized_category FROM  products WHERE store_id=%s'
    cursor.execute(query, (storeId,))
    ras=cursor.fetchall()
    return [ras[s]['normalized_category'] for s in range(len(ras))]





def categories(storeId):
    query = 'SELECT DISTINCT category FROM  products WHERE store_id=%s AND category IS NOT NULL'
    cursor.execute(query, (storeId,))
    ras=cursor.fetchall()
    return [ras[s]['category'] for s in range(len(ras))]

def stores_ids():
    query = 'SELECT DISTINCT store_id FROM products'
    cursor.execute(query)
    ras=cursor.fetchall()
    return [ras[s]['store_id'] for s in range(len(ras))]
    

def get_categories(store_Id):
    cursor_cat.execute("SELECT categories.name, products.product_id from categories, products WHERE categories.id=products.category_id AND products.store_id=%s",(store_Id,) )
    L= cursor_cat.fetchall()
    return [(s['product_id'],s['name']['main']) for s in L]
    

def _create_cursor(connection):
    return connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

def set_store_id(storeId):
    global STORE_ID
    STORE_ID = storeId



def insert_normalized_category(M):
    for i,l in enumerate(M):
        cursor.execute("UPDATE products SET normalized_category=%s WHERE store_id=%s AND product_id=%s",(None,6,l[0],))
    connection.commit()
    
def insert_many_features(ids, features, model):

    tensors=[]
    for feature in features :
        tensor = []
        for a in feature:
            tensor.append(a.tolist())
        tensors.append(tensor)


    tup = zip(ids, tensors, itertools.repeat(model))
    args_str = b','.join([cursor.mogrify("(%s,%s,%s)", u) for u in tup])
    cursor.execute("INSERT INTO features (product_id, tensor, model) VALUES " + args_str.decode('utf8'))
    connection.commit()

connection = _connect_database(db_name='postgres', username='postgres', host='35.195.88.77', password='rkhj2rpDq5tB')
cursor= _create_cursor(connection)

def get_users(storeId):
    cursor.execute("SELECT * FROM preferences JOIN (SELECT data,id FROM users) AS datai ON preferences.user_id=datai.id AND store_id=%s",(storeId,))
    return cursor.fetchall()

def insert_products(products):
    cursor.execute()
    connection.commit()

def get_column_names(table):
    cursor.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name=%s", (table,))
    return [col['column_name'] for col in cursor.fetchall()]

def get_nb_products(storeId):
   cursor.execute("SELECT COUNT(*) FROM products WHERE store_id=%s",(storeId,))
   return cursor.fetchall()[0]['count']

def get_user_data(userId):## to see data 
    cursor.execute('SELECT data FROM users WHERE id=%s',(userId,))
    return cursor.fetchall()[0]

def get_features(product_id=None, store_id=STORE_ID, model='ResNet50'):
    if isinstance(product_id, (list,)):
        query = "SELECT features.* FROM unnest(%s::text[]) product_ids JOIN features ON product_ids = features.product_id AND features.store_id = %s AND features.model = %s"
        cursor.execute(query, (product_id, store_id, model))
        res = cursor.fetchall()
        product_ids_fetched = [r['product_id'] for r in res]
        final = []
        for idx, pid in enumerate(product_id) :
            if pid not in product_ids_fetched:
                final.append({})
            else:
                final.append({'tensor': res[product_ids_fetched.index(pid)]['tensor']})
        return final
    elif product_id != None:
        cursor.execute("SELECT * FROM features WHERE product_id = %s AND store_id = %s AND model = %s", (str(product_id), store_id, model))
        res=cursor.fetchall()[0]
        return res

def get_products(store_id=STORE_ID, offset=0):
    cursor.execute("SELECT * FROM products WHERE store_id=%s OFFSET %s ROWS FETCH FIRST 100000 ROW ONLY",(store_id, offset))
    return cursor.fetchall()


def get_user(userId, storeId=STORE_ID):
    query = 'SELECT * FROM preferences WHERE user_id=%s AND store_id=%s'
    cursor.execute(query, (userId, storeId))
    return cursor.fetchall()

#Used to verify if fesatures for a certain product_id has been
#calculated
def get_products_not_in_list(values, column='product_id', store_id=STORE_ID, offset=0):
    query = "SELECT products.* FROM products LEFT OUTER JOIN unnest(%s::text[]) value ON value = products."+column+" WHERE value IS NULL AND products.store_id = %s OFFSET %s ROWS FETCH FIRST 100000 ROW ONLY"
    cursor.execute(query, (values, store_id, offset))
    return cursor.fetchall()

def get_products_from_ids(product_ids, store_id=STORE_ID):
    if isinstance(product_ids, (list,)):
        query = "SELECT products.* FROM unnest(%s::text[]) L JOIN products ON L = products.product_id AND products.store_id = %s"
        cursor.execute(query, (product_ids, store_id))
        return cursor.fetchall()
    elif product_ids!=None:
        query = "SELECT * FROM products WHERE  product_id=%s AND store_id = %s"
        cursor.execute(query, (product_ids, store_id))
        return cursor.fetchall()

def get_sample_products(store_id=STORE_ID):
    cursor.execute("SELECT * FROM products TABLESAMPLE SYSTEM (10) WHERE store_id = %s LIMIT 3500", (store_id,))
    return cursor.fetchall()

def get_sample_products_not_in_list(store_id=STORE_ID):
    cursor.execute("SELECT * FROM products TABLESAMPLE SYSTEM (10) WHERE store_id = %s LIMIT 3500", (store_id,))
    return cursor.fetchall()
    query = "SELECT products.* FROM products LEFT OUTER JOIN unnest(%s::text[]) value ON value = products."+column+" WHERE value IS NULL AND products.store_id = %s TABLESAMPLE SYSTEM (10) LIMIT 3500"
    cursor.execute(query, (values, store_id, offset))
    return cursor.fetchall()

def get_sample_products_from_category(category, store_id=STORE_ID):
    cursor.execute("SELECT * FROM products TABLESAMPLE SYSTEM (10) WHERE category ~ CONCAT(\'^(\', CONCAT(%s,\')(\\..*)*$\')) AND store_id = %s LIMIT 3500", (category, store_id))
    return cursor.fetchall()

def get_random_product(store_id=STORE_ID):
    cursor.execute("WITH products_store AS (SELECT * FROM products WHERE store_id = %s) SELECT * FROM products_store OFFSET FLOOR(RANDOM()*(SELECT COUNT(*) FROM products_store)) LIMIT 1", (store_id,))

    return cursor.fetchall()[0]

#Get a random product in a pool and not previsously seen
#product_ids are those that we don't want like previously seen
def get_random_product_reco(product_ids, pool_name, store_id=STORE_ID):
    query = "WITH product_ids AS (select * from unnest(%s::text[])) SELECT p_id FROM product_ids JOIN select unnest(product_ids) p_id from pools where name=%s and store_id=%s ON unnest(product_ids) != p_id WHERE OFFSET FLOOR(RANDOM()*(SELECT COUNT(*) FROM product_ids)) LIMIT 1;"
    cursor.execute(query, (product_ids, store_id))
    return cursor.fetchall()

def get_random_celio_pool_not_in_list(product_ids):
    query = "WITH product_ids AS (select * from ((select unnest(product_ids) product_id from pools WHERE store_id='2' AND name='Celio') p LEFT OUTER JOIN unnest(%s::text[]) value ON value = p.product_id) foo WHERE value IS NULL)  SELECT product_id FROM product_ids OFFSET FLOOR(RANDOM()*(SELECT COUNT(*) FROM product_ids)) LIMIT 1;"
    cursor.execute(query, (product_ids,))
    return cursor.fetchall()

def get_random_product_not_in_list(product_ids, number, store_id=STORE_ID):
    query = "WITH product_ids AS (select * from products LEFT OUTER JOIN unnest(%s::text[]) value ON value = products.product_id WHERE value IS NULL AND products.store_id = %s) SELECT product_id FROM product_ids order by random() LIMIT %s;"
    cursor.execute(query, (product_ids, store_id, number))
    return cursor.fetchall()



    
def get_recommendable_products(product_ids, user_preferences, number, store_id=STORE_ID):
    table_columns = get_column_names('products')
    
    where_str = " AND ".join([k + '=%s' for k in user_preferences.keys() if k in table_columns])
    if len(where_str) > 0:
        where_str = " AND " + where_str

    query_str = "WITH product_ids AS (select * from products LEFT OUTER JOIN unnest(%s::text[]) value ON value = products.product_id WHERE value IS NULL AND products.store_id = %s {}) SELECT * FROM product_ids order by random() LIMIT %s;".format(where_str)

    user_preferences_values = [user_preferences[k] for k in user_preferences.keys() if k in table_columns]


    query = cursor.mogrify(query_str, (product_ids, store_id, *user_preferences_values, number))
    #print(query.decode('utf8'))

    cursor.execute(query.decode('utf8'))
    #return cursor.fetchall()
    return cursor.fetchall()

def get_cursor():
    return cursor

def get_connection():
    return connection

#connection = _connect_database(db_name='postgres', username='postgres', host='35.195.88.77', password='rkhj2rpDq5tB')
#cursor= _create_cursor(connection)

#connection to categories:
connection_cat = _connect_database(db_name='postgres', username='cleed', host='35.233.37.139', password='Ed7BHToR1p25')
cursor_cat= _create_cursor(connection_cat)    

# Connect to Cleed's database
connection = _connect_database(db_name='postgres', username='postgres', host='35.195.88.77', password='rkhj2rpDq5tB')
cursor= _create_cursor(connection)

#Connect to the features database
connection2 = _connect_database(db_name='postgres', username='cleed', host='35.222.20.69', password='ffs')
cursor2 = _create_cursor(connection2)
###Categories