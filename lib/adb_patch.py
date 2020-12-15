import subprocess
import shutil
import os


def adb_devices():
    subprocess.run("adb kill-server")
    output = subprocess.check_output('adb devices', text=True).split('\n', 1)[1].split("device")[0].strip()
    return output


def auth_check():
    command = "adb shell su -c id"
    output = subprocess.check_output(command, text=True)
    return output


def push_adbkey(path_key):
    command = []
    command.append("adb push " + path_key + " /sdcard")  # adb push adbkey.pub /sdcard
    command.append("adb shell su -c cp /sdcard/adbkey.pub /data/misc/adb/adb_keys")  # cp pub > adb_keys
    command.append("adb shell su -c chown system /data/misc/adb/adb_keys")  # chown system
    command.append("adb shell su -c chmod 440 /data/misc/adb/adb_keys")  # chmod 440
    command.append("adb shell su -c rm /sdcard/adbkey.pub")  # rm pub

    for i in range(len(command)):
        subprocess.run(command[i])


def backup_pri_key(pubkey_path):
    prikey_path = pubkey_path.split(".pub", 1)[0]
    if not os.path.isdir("./backup"):
        os.mkdir("./backup")
    shutil.copy(prikey_path, "./backup/")
