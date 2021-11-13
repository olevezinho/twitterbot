import mysql.connector as database

def database_auth(username, password, host, dbname):
    connection = database.connect(
        user=username,
        password=password,
        host=host,
        database=dbname)
    return connection

def add_data(connection, cursor, tweet_id, tweet_time, topic, author, body):
    try:
        statement = "INSERT INTO tweet (`tweet_id`, `tweet_time`, `topic`, `author`, `body`) VALUES (%s, STR_TO_DATE(%s, '%d-%m-%Y %H:%i'), %s, %s, %s)"
        data = (tweet_id, tweet_time, topic, author, body)
        cursor.execute(statement, data)
        connection.commit()
        print("Successfully added entry to database")
    except database.Error as e:
        print(f"Error adding entry to database: {e}")

def get_data(cursor, tweet_id):
    try:
      statement = "SELECT tweet_id, topic, author, body FROM tweet WHERE tweet_id=%s"
      data = (tweet_id,)
      cursor.execute(statement, data)
      for (tweet_id, topic, author, body) in cursor:
        print(f"Successfully retrieved {tweet_id}, {topic}, {author}, {body}")
    except database.Error as e:
      print(f"Error retrieving entry from database: {e}")

def close_connection(connection):
    connection.close()