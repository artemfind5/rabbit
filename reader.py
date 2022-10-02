from mysql.connector import connect, Error

def reader(N):
    try:
        N = int(N)
        with connect(
                host="localhost",
                user="root",
                password="12345678",
                database="av_db",
        ) as connection:
            print(connection)
            select_query = "SELECT * FROM words"
            with connection.cursor() as cursor:
                cursor.execute(select_query)
                result = cursor.fetchall()
                for row in result:
                    #print(row)
                    if row[1] >= N:
                        filename = row[0]+'.txt'
                        f = open("output/" + filename, 'w')
                        text = row[0] + '\n' + str(row[1])
                        written_symbols = f.write(text)
                        f.close()
                        if written_symbols == len(text): # проверка на успешную запись файла перед удалением строки
                            delete_query = """DELETE FROM words WHERE word = '{0}';""".format(row[0])
                            cursor.execute(delete_query)
                            print("Deleted the row '" + str(row) + "' and wrote the file: " + filename)
                        else:
                            print("Write error")

                print("Successfully")
                connection.commit()
    except Error as e:
        print(e)
    except ValueError:
        print("Invalid literal for int() with base 10:" + N)

def main():
    N = input("Enter N: ")
    reader(N)

if __name__ == "__main__":
    main()