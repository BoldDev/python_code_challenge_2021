# This try/while/if are used for the first time raising a container, because database might take a while
# to be ready on the first time, preventing Django first time migration and broken Django deployment.
import os
import time
import mysql.connector


def main():
    tries = 0
    retry = True

    while retry:
        time.sleep(5)
        if tries < 20:
            try:
                con = mysql.connector.connect(host=os.environ.get('MYSQL_HOST'),
                                              user=os.environ.get('MYSQL_USER'),
                                              password=os.environ.get('MYSQL_PASSWORD'),
                                              port=os.environ.get('MYSQL_PORT'),
                                              database=os.environ.get('MYSQL_NAME'),
                                              )

                con.close()
                retry = False

            except:
                print("Database does not seems ready!")
                tries += 1

        else:
            print("Database took too long to be ready! Stopping deployment.")
            raise TimeoutError

    else:
        print("Database seems ready!")


if __name__ == '__main__':
    main()
