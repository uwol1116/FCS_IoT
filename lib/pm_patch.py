import subprocess
import os


def get_app():
    if not os.path.isdir("./app"):
        command = "adb pull /system/app"
        output = subprocess.check_output(command, text=True)
        return output


def create_whiteList():
    output = subprocess.check_output("adb shell su -c ls /data/misc/", text=True)
    if not "pmwhitelist" in output:
        pwd = os.getcwd()
        path = "./app/"
        file_list = os.listdir(path)
        file_list_rsa = [file for file in file_list]  # file list return

        whitelist = open('whitelist', mode='wb')

        for file in file_list_rsa:
            path = "./app/" + file
            if not os.path.isdir(path):
                continue
            os.chdir(path)

            keytool_cmd = 'keytool -printcert -jarfile ' + file + '.apk'

            popen = subprocess.Popen(keytool_cmd, stdout=subprocess.PIPE, shell=True)
            (stdout_data,
             stderr_data) = popen.communicate()

            cert_decode = stdout_data.decode()
            cert_find = cert_decode.rfind('SHA256: ')

            cert_extract = stdout_data[cert_find + 8:cert_find + 103]
            cert_string = ''.join(cert_extract.decode().lower().split(':')) + '\n'

            whitelist.write(cert_string.encode())
            os.chdir(pwd)

        whitelist.close()

        read_whitelist = open('whitelist', mode='r')
        write_whitelist = open('pmwhitelist', mode='w')

        lines = read_whitelist.readlines()

        lines = list(set(lines))

        for line in lines:
            write_whitelist.write(line)

        write_whitelist.close()
        read_whitelist.close()

        command = []
        command.append("adb push ./pmwhitelist /sdcard")
        command.append("adb shell su -c cp /sdcard/pmwhitelist /data/misc/ ")
        command.append("adb shell su -c chown system:system /data/misc/pmwhitelist")
        command.append("adb shell su -c chmod 644 /data/misc/pmwhitelist")
        command.append("adb shell su -c rm /sdcard/pmwhitelist")

        for i in range(len(command)):
            subprocess.run(command[i])

        os.remove("./whitelist")
        os.remove("./pmwhitelist")

        return ""
    else:
        return "Exist pmwhitelist"


def append_to_whitelist(apk_name):
    file = "\"" + apk_name + "\""

    output = subprocess.check_output("adb shell su -c ls /data/misc/", text=True)
    if "pmwhitelist" in output:
        command = "adb pull /data/misc/pmwhitelist"
        subprocess.run(command)

        whitelist = open('./pmwhitelist', mode='ab')

        keytool_cmd = 'keytool -printcert -jarfile ' + file

        popen = subprocess.Popen(keytool_cmd, stdout=subprocess.PIPE, shell=True)
        (stdout_data,
         stderr_data) = popen.communicate()

        cert_decode = stdout_data.decode()
        cert_find = cert_decode.rfind('SHA256: ')

        cert_extract = stdout_data[cert_find + 8:cert_find + 103]
        cert_string = ''.join(cert_extract.decode().lower().split(':')) + '\n'

        whitelist.write(cert_string.encode())

        whitelist.close()

        command = []
        command.append("adb push ./pmwhitelist /sdcard")
        command.append("adb shell su -c cp /sdcard/pmwhitelist /data/misc/ ")
        command.append("adb shell su -c chown system:system /data/misc/pmwhitelist")
        command.append("adb shell su -c chmod 644 /data/misc/pmwhitelist")
        command.append("adb shell su -c rm /sdcard/pmwhitelist")

        for i in range(len(command)):
            subprocess.run(command[i])

        os.remove("./pmwhitelist")

        return ""
    else:
        return "Not Exist"


def install_apk(apk_name):
    command = "adb install -r " + "\"" + apk_name + "\""
    output = subprocess.check_output(command, text=True)
    return output

