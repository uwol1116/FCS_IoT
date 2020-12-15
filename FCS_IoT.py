import sys
import os
import subprocess
import shutil
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication, QBasicTimer
from PyQt5.QtGui import *
from PyQt5 import uic

from lib import adb_patch
from lib import pm_patch
from lib import services_patch

form_main = uic.loadUiType(".\\UI\\main.ui")[0]
form_make_jar = uic.loadUiType(".\\UI\\make_jar.ui")[0]
form_select = uic.loadUiType(".\\UI\\select_patch.ui")[0]
form_make_progress = uic.loadUiType(".\\UI\\Make_Progress.ui")[0]
form_next_to_finish = uic.loadUiType(".\\UI\\Next_or_Finish.ui")[0]
form_file_path_adb = uic.loadUiType(".\\UI\\File_path_adb.ui")[0]
form_append_whitelist = uic.loadUiType(".\\UI\\whitelist.ui")[0]
form_patch_progress = uic.loadUiType(".\\UI\\Patch_progress.ui")[0]
form_finish = uic.loadUiType(".\\UI\\Finish.ui")[0]

patch_list = ["Binary Patch", "save_dir", "Both", "pub", "N"]
apk_list = []


class MyWindow(QMainWindow, form_main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # ui setup
        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load("UI/img/FCS_IoT main logo.jpg")
        self.setWindowIcon(QIcon("UI/img/fcs_iot_icon.ico"))
        self.label_logo.setPixmap(self.qPixmapVar)
        self.make_jar = Make_jar_Window()
        self.sel_patch = "Binary Patch"

        self.btn_next.clicked.connect(self.next)
        self.btn_quit.clicked.connect(QCoreApplication.instance().quit)

        self.radio1.clicked.connect(self.radioButtonClicked)
        self.radio2.clicked.connect(self.radioButtonClicked)

    def next(self):
        self.hide()
        if self.sel_patch == "Binary Patch":
            self.make_jar.show()
        elif self.sel_patch == "Image Patch":
            self.make_jar.show()

    def radioButtonClicked(self):
        if self.radio1.isChecked():
            self.sel_patch = "Binary Patch"
        elif self.radio2.isChecked():
            self.sel_patch = "Image Patch"


class Make_jar_Window(QDialog, form_make_jar):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # ui setup
        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load(".UI\\img\\FCS_IoT icon.png")
        self.label_logo.setPixmap(self.qPixmapVar)
        self.setWindowIcon(QIcon("UI/img/fcs_iot_icon.ico"))
        self.sel_patch = select_patch_Window()

        self.btn_check_con.clicked.connect(self.check_con)
        self.btn_save_dir.clicked.connect(self.save_dir)

        self.btn_next.clicked.connect(self.next)
        self.btn_back.clicked.connect(self.back)
        self.btn_quit.clicked.connect(QCoreApplication.instance().quit)

    def check_con(self):
        # check device
        if not adb_patch.adb_devices():
            QMessageBox.question(self, 'Message', 'Please Connect device to PC and Retry',
                                 QMessageBox.Ok, QMessageBox.Ok)
            self.label_check_con.setText("Please Connect device to PC and Retry")
            return
        else:
            # check root
            if not 'root' in adb_patch.auth_check():
                QMessageBox.question(self, 'Message', 'You Don\'t have root permission',
                                     QMessageBox.Ok, QMessageBox.Ok)
                self.label_check_con.setText("You Don\'t have root permission")
                return
            else:
                QMessageBox.question(self, 'Message', 'You connected devices and had root permission',
                                     QMessageBox.Ok, QMessageBox.Ok)
                self.btn_check_con.setEnabled(False)
                self.btn_next.setEnabled(True)
                self.label_check_con.setText("You connected devices and had root permission")
                return

    def save_dir(self):
        path = QFileDialog.getExistingDirectory(self)
        if path == '':
            patch_list[1] = path
            self.label_dir.setText("Please select Directory")
            return
        self.label_dir.setText(path)
        patch_list[1] = path

    def next(self):
        if patch_list[1] == "" or patch_list[1] == "save_dir":
            QMessageBox.question(self, 'Message', '저장할 디렉터리 경로가 설정되지 않았습니다.',
                                 QMessageBox.Ok, QMessageBox.Ok)
            return
        self.hide()
        self.sel_patch.show()

    def back(self):
        self.hide()
        self.main = MyWindow()
        self.main.show()


class select_patch_Window(QDialog, form_select):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # ui setup
        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load(".UI\\img\\FCS_IoT icon.png")
        self.label_logo.setPixmap(self.qPixmapVar)
        self.setWindowIcon(QIcon("UI/img/fcs_iot_icon.ico"))
        self.make_Progress = Make_ProgressWindow()
        self.sel_patch = "Both"

        self.radio_adb.clicked.connect(self.radioButtonClicked)  # ADB
        self.radio_pm.clicked.connect(self.radioButtonClicked)  # PM
        self.radio_both.clicked.connect(self.radioButtonClicked)  # Both

        self.btn_next.clicked.connect(self.next)
        self.btn_back.clicked.connect(self.back)
        self.btn_quit.clicked.connect(QCoreApplication.instance().quit)

    def radioButtonClicked(self):
        if self.radio_adb.isChecked():
            self.sel_patch = "ADB"
            patch_list[2] = self.sel_patch
        elif self.radio_pm.isChecked():
            self.sel_patch = "PM"
            patch_list[2] = self.sel_patch
        elif self.radio_both.isChecked():
            self.sel_patch = "Both"
            patch_list[2] = self.sel_patch

    def next(self):
        self.hide()
        self.make_Progress.time_start()
        self.make_Progress.show()

    def back(self):
        self.hide()
        self.make_jar = Make_jar_Window()
        self.make_jar.show()

    '''
    def make_services(self):
        if not 'files pulled' in services_patch.get_framework():
            QMessageBox.question(self, 'Message', 'ADB Pull Framework is failed! Please Check Your ADB!',
                                 QMessageBox.Ok, QMessageBox.Ok)
            sys.exit()
        else:
            self.make_Progress.tb.setPlainText("Execute: adb pull /system/framework")

        # services.odex -> out
        try:
            services_patch.odex_to_smali()
            self.make_Progress.tb.append(
                "Execute: java -jar tool/baksmali.jar x framework/oat/arm/services.odex -a 23 -b framework/arm/boot.oat"
            )
            self.make_Progress.tb.append("Output folder: ./out")
        except subprocess.CalledProcessError as e:
            QMessageBox.question(self, 'Message', str(e),
                                 QMessageBox.Ok, QMessageBox.Ok)
            services_patch.rm_file()
            sys.exit()

        adb_pm = [0, 0]
        if patch_list[2] == "Both":
            adb_pm[0] = 1
            adb_pm[1] = 1
        elif patch_list[2] == "ADB":
            adb_pm[0] = 1
        elif patch_list[2] == "PM":
            adb_pm[1] = 1

        if adb_pm[0]:  # ADB
            # adb smali patch
            try:
                services_patch.adb_replace_patch()
                self.make_Progress.tb.append(
                    "Execute: copy "
                    + "./lib/patched_smali/ADB_smali/UsbDebuggingManager.smali "
                    + "./out/com/android/server/usb/"
                )
                self.make_Progress.tb.append(
                    "Execute: copy "
                    + "./lib/patched_smali/ADB_smali/UsbDebuggingManager$UsbDebuggingHandler.smali "
                    + "./out/com/android/server/usb/"
                )
            except:
                QMessageBox.question(self, 'Message', "Error adb smali",
                                     QMessageBox.Ok, QMessageBox.Ok)
                services_patch.rm_file()
                sys.exit()

        if adb_pm[1]:  # PM
            # pm smali patch
            try:
                services_patch.pm_replace_patch()
                self.make_Progress.tb.append(
                    "Execute: copy "
                    + "./lib/patched_smali/PM_smali/checkCert.smali "
                    + "./out/com/android/server/pm/"
                )
                self.make_Progress.tb.append(
                    "Execute: copy "
                    + "./lib/patched_smali/PM_smali/PackageManagerService.smali "
                    + "./out/com/android/server/pm/"
                )
            except:
                QMessageBox.question(self, 'Message', "Error pm smali",
                                     QMessageBox.Ok, QMessageBox.Ok)
                services_patch.rm_file()
                sys.exit()

        # out -> classes.dex
        try:
            services_patch.smali_to_dex()
            self.make_Progress.tb.append("java -jar tool/smali.jar a ./out -o classes.dex")
            self.make_Progress.tb.append("Extract: classes.dex")
        except subprocess.CalledProcessError as e:
            QMessageBox.question(self, 'Message', str(e),
                                 QMessageBox.Ok, QMessageBox.Ok)
            services_patch.rm_file()
            sys.exit()

        # jar patched_services.jar
        try:
            services_patch.make_services(patch_list[1])
            self.make_Progress.tb.append("Execute: jar xf ../framework/services.jar")
            self.make_Progress.tb.append("Execute: jar cvf patched_services.jar")
            self.make_Progress.tb.append("Extract: patched_services.jar")
        except subprocess.CalledProcessError as e:
            QMessageBox.question(self, 'Message', str(e),
                                 QMessageBox.Ok, QMessageBox.Ok)
            services_patch.rm_file()
            sys.exit()

        # rm file
        try:
            services_patch.rm_file()
        except subprocess.CalledProcessError as e:
            QMessageBox.question(self, 'Message', str(e),
                                 QMessageBox.Ok, QMessageBox.Ok)
    '''


class Make_ProgressWindow(QDialog, form_make_progress):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load(".UI\\img\\FCS_IoT icon.png")
        self.label_logo.setPixmap(self.qPixmapVar)
        self.setWindowIcon(QIcon("UI/img/fcs_iot_icon.ico"))

        self.next_to_finish = Next_or_Finish_Window()

        self.timer = QBasicTimer()
        self.step = 0

    def time_start(self):
        self.timer.start(100, self)

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.next()
            return

        if self.step == 50:
            self.timer.stop()
            self.make_services()
            self.timer.start(100, self)

        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def next(self):
        self.hide()
        self.next_to_finish.show()

    def make_services(self):
        if not 'files pulled' in services_patch.get_framework():
            QMessageBox.question(self, 'Message', 'ADB Pull Framework is failed! Please Check Your ADB!',
                                 QMessageBox.Ok, QMessageBox.Ok)
            sys.exit()
        else:
            self.tb.setPlainText("Execute: adb pull /system/framework")

        # services.odex -> out
        try:
            services_patch.odex_to_smali()
            self.tb.append(
                "Execute: java -jar tool/baksmali.jar x framework/oat/arm/services.odex -a 23 -b framework/arm/boot.oat"
            )
            self.tb.append("Output folder: ./out")
        except subprocess.CalledProcessError as e:
            QMessageBox.question(self, 'Message', str(e),
                                 QMessageBox.Ok, QMessageBox.Ok)
            services_patch.rm_file()
            sys.exit()

        adb_pm = [0, 0]
        if patch_list[2] == "Both":
            adb_pm[0] = 1
            adb_pm[1] = 1
        elif patch_list[2] == "ADB":
            adb_pm[0] = 1
        elif patch_list[2] == "PM":
            adb_pm[1] = 1

        if adb_pm[0]:  # ADB
            # adb smali patch
            try:
                services_patch.adb_replace_patch()
                self.tb.append(
                    "Execute: copy "
                    + "./lib/patched_smali/ADB_smali/UsbDebuggingManager.smali "
                    + "./out/com/android/server/usb/"
                )
                self.tb.append(
                    "Execute: copy "
                    + "./lib/patched_smali/ADB_smali/UsbDebuggingManager$UsbDebuggingHandler.smali "
                    + "./out/com/android/server/usb/"
                )
            except:
                QMessageBox.question(self, 'Message', "Error adb smali",
                                     QMessageBox.Ok, QMessageBox.Ok)
                services_patch.rm_file()
                sys.exit()

        if adb_pm[1]:  # PM
            # pm smali patch
            try:
                services_patch.pm_replace_patch()
                self.tb.append(
                    "Execute: copy "
                    + "./lib/patched_smali/PM_smali/checkCert.smali "
                    + "./out/com/android/server/pm/"
                )
                self.tb.append(
                    "Execute: copy "
                    + "./lib/patched_smali/PM_smali/PackageManagerService.smali "
                    + "./out/com/android/server/pm/"
                )
            except:
                QMessageBox.question(self, 'Message', "Error pm smali",
                                     QMessageBox.Ok, QMessageBox.Ok)
                services_patch.rm_file()
                sys.exit()

        # out -> classes.dex
        try:
            services_patch.smali_to_dex()
            self.tb.append("java -jar tool/smali.jar a ./out -o classes.dex")
            self.tb.append("Extract: classes.dex")
        except subprocess.CalledProcessError as e:
            QMessageBox.question(self, 'Message', str(e),
                                 QMessageBox.Ok, QMessageBox.Ok)
            services_patch.rm_file()
            sys.exit()

        # jar patched_services.jar
        try:
            services_patch.make_services(patch_list[1])
            self.tb.append("Execute: jar xf ../framework/services.jar")
            self.tb.append("Execute: jar cvf patched_services.jar")
            self.tb.append("Extract: patched_services.jar")
        except subprocess.CalledProcessError as e:
            QMessageBox.question(self, 'Message', str(e),
                                 QMessageBox.Ok, QMessageBox.Ok)
            services_patch.rm_file()
            sys.exit()

        # rm file
        try:
            services_patch.rm_file()
        except subprocess.CalledProcessError as e:
            QMessageBox.question(self, 'Message', str(e),
                                 QMessageBox.Ok, QMessageBox.Ok)


class Next_or_Finish_Window(QDialog, form_next_to_finish):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load(".UI\\img\\FCS_IoT icon.png")
        self.label_logo.setPixmap(self.qPixmapVar)
        self.setWindowIcon(QIcon("UI/img/fcs_iot_icon.ico"))
        self.file_path_adb = file_path_adb_Window()
        self.append_whitelist = append_to_whitelist_Window()

        self.btn_next.clicked.connect(self.next)
        self.btn_finish.clicked.connect(QCoreApplication.instance().quit)

    def next(self):
        self.hide()
        if patch_list[2] == "Both":
            self.file_path_adb.show()
            self.file_path_adb.btn_next.setText('Next >')
        elif patch_list[2] == "ADB":
            self.file_path_adb.show()
        elif patch_list[2] == "PM":
            self.append_whitelist.show()


class file_path_adb_Window(QDialog, form_file_path_adb):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load(".UI\\img\\FCS_IoT icon.png")
        self.label_logo.setPixmap(self.qPixmapVar)
        self.setWindowIcon(QIcon("UI/img/fcs_iot_icon.ico"))
        self.patch_progress = Patch_Progress()

        self.btn_pub.clicked.connect(self.get_pub)

        self.btn_next.clicked.connect(self.patch)
        self.btn_back.clicked.connect(self.back)
        self.btn_quit.clicked.connect(self.cancel)

    def get_pub(self):
        user = os.environ['USERPROFILE']
        android = user + "/.android/"
        path = QFileDialog.getOpenFileName(self, "파일 선택", android, "Files (*.pub)")
        if path[0] == '':
            patch_list[3] = path[0]
            self.label_pub.setText("Please Select Public Key File")
            return
        self.label_pub.setText(path[0])
        patch_list[3] = path[0]

    def patch(self):
        if patch_list[3] == "" or patch_list[3] == "pub":
            QMessageBox.question(self, 'Message', 'pubkey File 경로가 설정되지 않았습니다.',
                                 QMessageBox.Ok, QMessageBox.Ok)
            return
        self.hide()
        if patch_list[2] == "Both":
            self.append_whitelist = append_to_whitelist_Window()
            self.append_whitelist.show()
        else:
            self.patch_progress.time_start()
            self.patch_progress.show()

    def back(self):
        self.hide()
        self.next_or_finish = Next_or_Finish_Window()
        self.next_or_finish.show()

    def cancel(self):
        self.close()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def adb_patch(self):
        # pubkey set
        pubkey_path = patch_list[3]

        # push adbkey.pub
        try:
            adb_patch.push_adbkey(pubkey_path)  # adb patch
        except subprocess.CalledProcessError as e:
            QMessageBox.question(self, 'Message', str(e),
                                 QMessageBox.Ok, QMessageBox.Ok)
            sys.exit()

        # backup private key
        try:
            adb_patch.backup_pri_key(pubkey_path)
        except:
            QMessageBox.question(self, 'Message', "Don\'t backup key",
                                 QMessageBox.Ok, QMessageBox.Ok)

        if patch_list[2] == "ADB":
            # push services.jar
            try:
                services_patch.push_services()  # services patch
            except subprocess.CalledProcessError as e:
                QMessageBox.question(self, 'Message', str(e),
                                 QMessageBox.Ok, QMessageBox.Ok)
                sys.exit()


class append_to_whitelist_Window(QDialog, form_append_whitelist):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load(".UI\\img\\FCS_IoT icon.png")
        self.label_logo.setPixmap(self.qPixmapVar)
        self.setWindowIcon(QIcon("UI/img/fcs_iot_icon.ico"))

        self.patch_progress = Patch_Progress()

        self.btn_add.clicked.connect(self.add)
        self.btn_remove.clicked.connect(self.remove)

        self.btn_patch.clicked.connect(self.patch)
        self.btn_back.clicked.connect(self.back)
        self.btn_quit.clicked.connect(self.cancel)

        self.chk_install.stateChanged.connect(self.chkFunction)

    def chkFunction(self):
        pass
        if self.chk_install.isChecked():
            patch_list[4] = 'Y'
        else:
            patch_list[4] = 'N'

    def add(self):
        path = QFileDialog.getOpenFileName(self, "파일 선택", "C:\\", "Files (*.apk)")
        if path[0] == '':
            return
        apk_list.append(path[0])
        self.listWidget_apk.addItem(path[0])  # 한 개 추가
        self.btn_add.setEnabled(False)
        self.btn_remove.setEnabled(True)
        self.chk_install.setEnabled(True)
        self.chk_install.setChecked(True)
        patch_list[4] = 'Y'

    def remove(self):
        # ListWidget에서 현재 선택한 항목을 삭제할 때는 선택한 항목의 줄을 반환한 후, takeItem함수를 이용해 삭제합니다.
        self.removeItemRow = self.listWidget_apk.currentRow()
        self.listWidget_apk.takeItem(self.removeItemRow)
        del apk_list[-1]
        self.btn_add.setEnabled(True)
        self.btn_remove.setEnabled(False)
        self.chk_install.setEnabled(False)
        self.chk_install.setChecked(False)
        patch_list[4] = 'N'

    def patch(self):
        self.hide()
        self.patch_progress.time_start()
        self.patch_progress.show()

    def back(self):
        self.hide()
        if patch_list[2] == "Both":
            self.file_path_adb = file_path_adb_Window()
            self.file_path_adb.show()
        else:
            self.next_or_finish = Next_or_Finish_Window()
            self.next_or_finish.show()

    def cancel(self):
        self.close()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def pm_patch(self):
        try:
            pm_patch.get_app()
        except subprocess.CalledProcessError as e:
            QMessageBox.question(self, 'Message', str(e),
                                 QMessageBox.Ok, QMessageBox.Ok)
            if os.path.isdir("./app"):
                shutil.rmtree("./app")
            sys.exit()

        # create whitelist
        try:
            exist_state = pm_patch.create_whiteList()
            if "Exist" in exist_state:
                QMessageBox.question(self, 'Message', exist_state + "\n이미 pmwhitelist가 존재합니다.",
                                     QMessageBox.Ok, QMessageBox.Ok)
        except subprocess.CalledProcessError as e:
            QMessageBox.question(self, 'Message', str(e) + "\npmwhitelist를 생성하지 못했습니다.",
                                 QMessageBox.Ok, QMessageBox.Ok)
            sys.exit()

        if len(apk_list) >= 1:
            print(apk_list)
            for i in range(len(apk_list)):
                # append signature
                try:
                    exist_State = pm_patch.append_to_whitelist(apk_list[i])
                    if "Not Exist" in exist_State:
                        QMessageBox.question(self, 'Message',
                                             exist_State + "\npmwhitelist가 존재하지않아 시그니처를 등록하지 못했습니다",
                                             QMessageBox.Ok, QMessageBox.Ok)
                except subprocess.CalledProcessError as e:
                    QMessageBox.question(self, 'Message', str(e) + "\n해당 apk의 시그니처가 등록이 되지 않았습니다.",
                                         QMessageBox.Ok, QMessageBox.Ok)

                # Install APK
                if patch_list[4] == 'Y':
                    try:
                        output = pm_patch.install_apk(apk_list[i])
                        if "Failure" in output:
                            QMessageBox.question(self, 'Message', output + "\n해당 apk의 시그니처가 등록이 되지 않았습니다.",
                                                 QMessageBox.Ok, QMessageBox.Ok)
                    except subprocess.CalledProcessError as e:
                        QMessageBox.question(self, 'Message', "설정하신 apk 파일이 설치가 안됐습니다.\n따로 설치해주세요",
                                             QMessageBox.Ok, QMessageBox.Ok)

        # push services.jar
        try:
            services_patch.push_services()  # services patch
        except subprocess.CalledProcessError as e:
            QMessageBox.question(self, 'Message', str(e),
                                 QMessageBox.Ok, QMessageBox.Ok)
            services_patch.rm_file()
            sys.exit()

        # rm file
        try:
            if os.path.isdir("./app"):
                pass
                # shutil.rmtree("./app")
        except:
            QMessageBox.question(self, 'Message', "Error shutil.rmtree",
                                 QMessageBox.Ok, QMessageBox.Ok)


class Patch_Progress(QDialog, form_patch_progress):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load(".UI\\img\\FCS_IoT icon.png")
        self.label_logo.setPixmap(self.qPixmapVar)
        self.setWindowIcon(QIcon("UI/img/fcs_iot_icon.ico"))

        self.finish = FinishWindow()

        self.timer = QBasicTimer()
        self.step = 0

    def time_start(self):
        self.timer.start(100, self)

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.next()
            return

        if self.step == 50:
            self.timer.stop()
            self.file_path_adb = file_path_adb_Window()
            self.append_whitelist = append_to_whitelist_Window()
            if patch_list[2] == "Both":
                self.file_path_adb.adb_patch()
                self.append_whitelist.pm_patch()
            elif patch_list[2] == "ADB":
                self.file_path_adb.adb_patch()
            elif patch_list[2] == "PM":
                self.append_whitelist.pm_patch()
            self.timer.start(100, self)

        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def next(self):
        self.hide()
        self.finish.show()


class FinishWindow(QDialog, form_finish):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load("UI/img/FCS_IoT main logo.jpg")
        self.label_logo.setPixmap(self.qPixmapVar)
        self.setWindowIcon(QIcon("UI/img/fcs_iot_icon.ico"))

        self.btn_finish.clicked.connect(QCoreApplication.instance().quit)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
