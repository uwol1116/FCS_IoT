 FCS_IoT-Patch-Tool 1.0.ver
=============
FCS_IoT Patch Tool 1.0.ver             
**For securing all Android 6.0 devices.**         

***This tool used the File Replace method(only for SM-N915S), so other devices must change the SMALI code.**                                  


Contents
===========
* Project name       
* Description         
* Requirements         
* Installation       
* Usage        
* Support     
* Authors         
               
               
               
1.Project name      
===================
This is **FCS_IoT Patch Tool** project.           
This is a type of BOB(Best Of the Best) program belonging to KITRI(Korea Information Technology Research Institute).          
                 
                 
                 
2.Description
==================
A vulnerability has been identified in Android 6.0 devices (electronic blackboard), so this tool is an automated patch tool that enhances security for these vulnerabilities.

2.1. **The opening of the Android Debugging Bridge (ADB) allows access to all users.**          
2.2. **The possibility to install apps with unknown sources can lead to malicious behavior by attackers.**
 * **Patch Plan(1)** :            
Modify the ADB debugging function to ensure that only users with a specific public key can access ADB.            
 * **Patch Plan(2)** :               
Modify the Package Manager (PM) related functions so that only apps with the public key registered in the pmwhitelist can be installed.

                 
                 
3.Requirements
================
There are several conditions for running Patch Tool.

3.1.Environment
-----------------
OS: Windows 10(64bit)          

3.2.Preparing the Framework
-------------------------

(1) **Install Python 3.5 or higher version.**             
Recommended: Python Anaconda(https://www.anaconda.com/products/individual).
             
(2) **Install PyQt5 of Python module.**           
You can proceed quickly with the simple command below.

```
pip install PyQt5
```

(3) **Install java JDK 15.0.1 or higher version.**            
* Of course, environmental variables need to be set.

(4) **Install ADB(https://developer.android.com/studio/releases/platform-tools).**        
* for Debugging your Android device.
* Make sure your Android device is connected to ADB.

(5) **Rooting your Android Device.**         
          
                
                   
4.Installation
================
1. **Download and decompress FCS_IoT Patch Tool.zip.**          

2. **Enter the FCS_IoT_Patch_Tool.1.0.ver folder.**          

3. **Type "cmd" in the address bar of the file explorer and type Enter.**            
And you can see the Command Prompt window.            

4. **Finally, type "python FCS_IoT.py".**           



5.Usage     
===================
We conducted verification on the 6.0 version of mobile phone(Note 4 Edge: SM-N915S)
and Smart Interactive Board(Korean Model), and it was completed.



6.Support
================
Contact below e-mail, if you need any help. 

swpark990714@gmail.com
dudwn03090@gmail.com

7.Authors
================
Seung-Won Park, Jae-Joon Kim, Ju-Young Lee,                       
Tae-Ho Park, Hye-Won Ji, Si-Eun Rho, Cheol-Kyu Han, Jeong-Gyu Yang.



