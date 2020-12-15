import sys
import subprocess
from lib import services_patch
from lib import adb_patch
from lib import pm_patch


def main():
    # check device
    if not adb_patch.adb_devices():
        print("Please Connect device to PC and Retry")
        sys.exit()
    else:
        print("adb_device end \n")

    # check root
    if not 'root' in adb_patch.auth_check():  # emulator check
        print("You Don't have root permission")
        sys.exit()
    else:
        print("auth_check end \n")

    # get framework
    if not 'files pulled' in services_patch.get_framework():
        print("ADB Pull Framework is failed! Please Check Your ADB!")
        sys.exit()
    else:
        print("get framework end \n")

    adb, pm = 0, 0
    while True:
        print("패치종류: adb, pm, both")
        combo = input("패치 종류를 입력하세요: ")
        if combo == "both":
            adb, pm = 1, 1
            break
        elif combo == "adb":
            adb = 1
            break
        elif combo == "pm":
            pm = 1
            break
        else:
            print("다시 입력하세요")

    # services.odex -> out
    try:
        services_patch.odex_to_smali()
    except subprocess.CalledProcessError as e:
        print(e)

    print("odex_to_smali end \n")

    if adb == 1:
        # adb smali patch
        services_patch.adb_replace_patch()
    if pm == 1:
        # pm smali patch
        services_patch.pm_replace_patch()

    # out -> classes.dex
    services_patch.smali_to_dex()

    # set save directory
    save_dir = '../'

    # jar patched_services.jar
    services_patch.make_services(save_dir)

    if adb == 1:
        # pubkey set
        pubkey_path = r"C:\Users\swpar\.android\adbkey.pub"

        # push adbkey.pub
        adb_patch.push_adbkey(pubkey_path)  # adb patch

        # backup private key
        adb_patch.backup_pri_key(pubkey_path)
    if pm == 1:
        # apk set
        apk_name = r"C:\Users\swpar\Downloads\adb_single_patch v.0.4\APK\terminal\terminal.apk"

        pm_patch.get_app()

        # create whitelist
        pm_patch.create_whiteList()

        # append signature
        pm_patch.append_to_whitelist(apk_name)

        install = 'N'
        print("pmwhitelist 에 해당 apk 파일의 Signature 를 추가했습니다.")
        input("설치하시겠습니까?(Y or N)")
        if install == 'Y':
            pm_patch.install_apk(apk_name)

    # push services.jar
    services_patch.push_services()  # services patch

    # rm file
    services_patch.rm_file()


if __name__ == "__main__":
    main()
