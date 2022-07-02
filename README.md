# Temporary-Files-Remover
This is a python script embed with a `data.json` file which will help you in removing any temporary files you want. It basically will delete every file inside your temporary folder based on your customized settings. If you wish the code to run faster, then make sure that your temporary files folder is in your default disk, in most cases it is the `C:\` disk.

Customzing the `data.json` file:

This is the default view of the file:
{"folder_name": "temp-files", "folder_location": "", "directory": "", "delDelay": "86400"}

Key Values:
The "folder_name" is the name of your temporary folder with the default value `temp-files` as the name. *Note that the code will only look for the first folder to make it run faster*
The "folder_location" is the location of your folder which the code will find it based on your folder name. *It is highly recommended to not alter this field*
The "directory" is a list of all your disks in the system which will be filled when you run the code. *It is highly recommend to not alter this field*
The "delDelay" is the time duration in seconds with the default value `86400` or `1 day` for which you want every file in the temporary folder to be deleted after.

However it is highly recommended to not alter the `.json` file for a better performance without any errors.

How to Understand the `logs.log` file:
This file is basically the place where every action of the code will be written *not including the editing of the `data.json` file*

Different Log Readings:

DEBUG: This log type means there was a problem in one of the Key Values and has been restored to default.
ERROR: This is an error meaning one of the Key Values has not been found/is incorrect. *However if there is a "folder_location" value then usually the error won't be thrown. In such cases, reset the "folder_location" to `""` for checking if your temporary file exists or not. In Error Logs, the code doesn't restore values, to avoid further errors, thus it is to be done manually*
WARNING: This is just a warning indicating that you misentered/altered a value in the `data.json` incorrectly. *In most cases the values are restored to default, and if not then it is highly recommend to restore them to the default. If you don't know what the default values are, just overwrite the whole `data.json` file to `{}`.*
INFO: This is just an information indicating that the code is on and running well. *Unless you do some mischieve with it*
CRITICAL: This is just the log indicating that a file in the temporary folder has been deleted. *Even from the recycle bin, put in less efforts*

Self Error Handling:
If the `data.json` file is empty, then you need to make it an empty json file. Meaning, just type `{}` and save it, then the code should function properly.

