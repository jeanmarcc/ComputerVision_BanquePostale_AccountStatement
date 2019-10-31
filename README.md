# Project Title
BanquePostale_AccountStatement

## Getting Started

__For test pupose only__

![](https://github.com/johnmarcc/OpenCV_BanquePostale_AccountStatement/blob/master/BanquePostaleVirtualKeyboard.jpg)

Python script which connects to https://www.labanquepostale.fr/ automatically in order to download bank account statements. 

This uses OpenCV library to detect which image buttons ahev to be clicked on in the virtual keyboard displayed in Login page according to 
password

This script can be run in foreground (param_HEADLESS_PROCESS = 'False') or in background on a server (param_HEADLESS_PROCESS = 'True')

## Input JSON file
All the input parameters (bank account number, password...) are extracted from a JSON file "BanquePostale_Account.json" that must be set in the directory the script is launched

1- param_NumeroDeCompte: Bank account 11 char (eg '123456789X0') <br/>
2- param_ID: id to connect to internet site, 6 digits <br/>
3- param_PWD: password to connect to internet site, 6 digits <br/>
4- param_DownloadFolder: local download directory where the pdf bank account statements are downloaded <br/>
5- param_HEADLESS_PROCESS: 'True' when we want the script to run a firefox instance in a background else 'False' for the foreground process

## Output PDF file
At the end od the script, the bank account statement file format PDF is downloaded to the specified directory (local machine or remote server)

## Authors

https://github.com/johnmarcc
