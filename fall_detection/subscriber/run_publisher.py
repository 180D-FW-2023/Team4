import subprocess
import time
def main():
    try:
        subprocess.run("./home/pi/subscriber/bin/simple_publisher")
    finally:
        time.sleep(1)
        main()

if __name__ == '__main__':
    main()
