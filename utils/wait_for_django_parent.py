# This try/while/if are used for the first time raising a container, because parent run some key commands
# and might take a while to be ready on the first time, preventing Django first time migration
# and breaking Django deployment.
import requests
import time
import os


def main():
    tries = 0
    retry = True
    parent = os.environ.get("DJANGO_PARENT")
    parent_port = os.environ.get("DJANGO_PARENT_PORT")

    while retry:
        time.sleep(5)
        if tries < 20:
            try:
                requests.get(f"http://{parent}:{parent_port}/")
                retry = False

            except:
                print("Django parent does not seems ready!")
                tries += 1

        else:
            print("Django parent took too long to be ready! Stopping deployment.")
            raise TimeoutError

    else:
        print("Django parent seems ready!")


if __name__ == '__main__':
    main()
