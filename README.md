# Project Title
Computer Vision | BanquePostale_AccountStatement

## Project Description
This process automatically downloads the most recent bank account statement from https://www.labanquepostale.fr/.
It auto connects with the user/password of the bank's customer. 
The statment is downloaded as a PDF file to a custom directory (local or server). 
This process could be scheduled every month and executed as a server script.

## This script is for experiment only! ##

## Getting Started

Example of virtual keyboard from https://www.labanquepostale.fr/:                         
![](https://github.com/johnmarcc/OpenCV_BanquePostale_AccountStatement/blob/master/BanquePostaleVirtualKeyboard.gif)

This Python script uses OpenCV library to detect which buttons have to be clicked on the virtual keyboard according to
user's password

This script can be run in foreground (param_HEADLESS_PROCESS = 'False') or in background on a server (param_HEADLESS_PROCESS = 'True')

## Input JSON file
All the input parameters (bank account number, password...) are extracted from a JSON file "BanquePostale_Account.json" that must be set in the directory the script is run

1- param_NumeroDeCompte: Bank account 11 char (eg '123456789X0') <br/>
2- param_ID: id to connect to bank internet site, 6 digits <br/>
3- param_PWD: password to connect to bank internet site, 6 digits <br/>
4- param_DownloadFolder: local download folder where the pdf bank account statements are downloaded <br/>
5- param_HEADLESS_PROCESS: 'True' when we want the script to run a firefox instance in a background else 'False' for the foreground process

## Output PDF file
When the script completes successfully, the bank account statement file format PDF is downloaded to the specified directory (local machine or remote server)

## Authors

https://github.com/jeanmarcc
