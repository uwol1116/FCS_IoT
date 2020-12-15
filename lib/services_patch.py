import os
import subprocess
import shutil


def get_framework():
    if not os.path.isdir("framework"):
        command = "adb pull /system/framework"
        output = subprocess.check_output(command, text=True)
        return output
    return "files pulled"


def odex_to_smali():
    command = "java -jar tool/baksmali.jar x framework/oat/arm/services.odex -a 23 -b framework/arm/boot.oat"
    subprocess.run(command, text=True)


def adb_replace_patch():
    shutil.copy("./lib/patched_smali/ADB_smali/UsbDebuggingManager.smali", "./out/com/android/server/usb/")
    shutil.copy("./lib/patched_smali/ADB_smali/UsbDebuggingManager$UsbDebuggingHandler.smali",
                "./out/com/android/server/usb/")


def pm_replace_patch():
    shutil.copy("./lib/patched_smali/PM_smali/checkCert.smali", "./out/com/android/server/pm/")
    shutil.copy("./lib/patched_smali/PM_smali/PackageManagerService.smali", "./out/com/android/server/pm/")


def smali_to_dex():
    command = "java -jar tool/smali.jar a ./out -o classes.dex"
    subprocess.run(command, text=True)


def make_services(save_dir):
    if not os.path.isdir("./services"):
        os.mkdir('./services')
    os.chdir('./services')

    command = "jar xf ../framework/services.jar"
    subprocess.run(command)

    shutil.copy('../classes.dex', './')

    command = "jar cvf patched_services.jar ./"
    subprocess.run(command)

    shutil.copy("./patched_services.jar", save_dir)


def push_services():
    com_list = []
    com_list.append("adb shell su -c mount -o rw,remount -t ext4 /system")
    com_list.append("adb push patched_services.jar /sdcard")
    com_list.append("adb shell su -c cp /sdcard/patched_services.jar /system/framework/services.jar")
    com_list.append("adb shell su -c chmod 644 /system/framework/services.jar")
    com_list.append("adb shell su -c rm /system/framework/oat/arm/services.odex")
    com_list.append("adb shell su -c rm /sdcard/patched_services.jar")
    com_list.append("adb shell su -c reboot")

    for i in range(len(com_list)):
        subprocess.run(com_list[i])


def rm_file():
    if not (os.path.isfile("./FCS_IoT.py") or os.path.isfile("./FCS_IoT.exe")):
        os.chdir("../")

    if os.path.isfile("./classes.dex"):
        os.remove("./classes.dex")

    if os.path.isdir("./out"):
        shutil.rmtree("./out")

    if os.path.isdir("./services"):
        shutil.rmtree("./services")

    if os.path.isdir("./framework"):
        shutil.rmtree("./framework")

    if os.path.isdir("./app"):
        shutil.rmtree("./app")
