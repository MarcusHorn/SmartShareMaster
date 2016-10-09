import os
from datetime import *
import time
import requests

datetime_frt = '%Y-%m-%d %H:%M:%S'
def getLastModifiedTime():
    # 2016-10-08 19:16:11.230971534
    # now = datetime.utcnow() # UTC time
    last_modified = os.popen("adb shell stat -c '%y' /sdcard/beam/nfc-code").read() # Eastern time
    if(len(last_modified) == 57):
        return

    last_modified = last_modified[:last_modified.index('.')]

    last_modified = datetime.strptime(last_modified, datetime_frt)
    return last_modified

def getDiffTimeLocalUTC(d1, d2):
    return (d2 - d1).total_seconds() - 14400

def getNFCCode():
    code = os.popen("adb shell cat /sdcard/beam/nfc-code").read()
    return code

rental_id = 1

def run():
    while True:

        last_mod = getLastModifiedTime()
        diff = None
        if(last_mod is not None):
            diff = getDiffTimeLocalUTC(last_mod, datetime.utcnow())

            # If the file has been modified in the last three seconds
            if(diff < 3):
                # Check if the key is correct
                r = requests.post('http://0.0.0.0:8080/getnfccode/', data={'rental_id': '1'})
                valid_key = r.text + '\n'
                provided_key = getNFCCode()
                # print(len(valid_key), len(provided_key))
                if(provided_key == valid_key):
                    print('----------UPDATED------------')
                    print(provided_key)
                    os.system('adb shell rm /sdcard/beam/nfc-code')
                else:
                    print('Invalid key provided!')            

        time.sleep(1)

if __name__ == '__main__':
    run()