################################################################################
# Script to download banking account statements from www.labanquepostale.fr
################################################################################
#__author__ = "https://github.com/johnmarcc"
#__copyright__ = ""
#__credits__ = []
#__license__ = ""
#__version__ = "1.0.0"
#__maintainer__ = ""
#__email__ = ""
#__status__ = "For test pupose only!"
################################################################################
# Requirements:
#  Firefox installed in environment
#  pip install opencv-python opencv-contrib-python
#  pip install selenium
################################################################################
# PARAMETERS
# All input parameters extracted from json file "BanquePostale_account.json"
# -- param_NumeroDeCompte: Bank account 11 char (eg '123456789X0')
# -- param_ID: id to connect to internet site, 6 digits
# -- param_PWD: password to connect to internet site, 6 digits
# -- param_DownloadFolder: local download directory where the pdf bank account
#    notes are downloaded
# -- param_HEADLESS_PROCESS: 'True' when we want the script to get a firefox
#    instance without visible window (batch process)
#    else 'False' when we want the script to open a visible firefox window
################################################################################
import sys
import pdb
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from skimage.measure import compare_ssim #for compare_ssim
from PIL import Image
import io
import cv2 #image matching
import glob #to check if file exist
import os
import json

#-> read banque account parameters from json file:
try:
    accountFileName = 'BanquePostale_account.json'
    with open(accountFileName) as json_file:
        data = json.load(json_file)
except:
    ThisError = sys.exc_info()[0]
    print("Error trying to import file",accountFileName,":",ThisError.__name__)
    sys.exit() #stop the script

try:
    param_NumeroDeCompte = data['account'][0]['param_NumeroDeCompte']
    param_ID = data['account'][0]['param_ID']
    param_PWD = data['account'][0]['param_PWD']
    param_DownloadFolder =  data['account'][0]['param_DownloadFolder']
    param_HEADLESS_PROCESS =  data['account'][0]['param_HEADLESS_PROCESS']
except :
    print("Incorrect input file format:",sys.exc_info())
    sys.exit() #stop the script

print("Parameters extracted from input file: ",param_NumeroDeCompte,    \
    '/',param_ID,'/',param_PWD,'/',param_DownloadFolder,'/',            \
    param_HEADLESS_PROCESS)

try:
    options = Options()

    if (param_HEADLESS_PROCESS):
        options.add_argument("--headless")

    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", param_DownloadFolder)
    options.set_preference("browser.download.useDownloadDir", True)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    options.set_preference("pdfjs.disabled", True)  # disable the built-in PDF viewer
    driver = webdriver.Firefox(firefox_options=options)
    driver.get("https://voscomptesenligne.labanquepostale.fr/wsost/OstBrokerWeb/loginform?TAM_OP=login&ERROR_CODE=0x00000000&URL=%2Fvoscomptes%2FcanalXHTML%2Fidentif.ea%3Forigin%3Dparticuliers")

except Exception as e:
    print("Error when opening webpage:",str(e).replace('%20',' '))
    sys.exit() #stop the script

# print(driver.page_source)  #to display whole page HTML

elt_val_cel_identifiant = driver.find_element_by_id("val_cel_identifiant").send_keys(param_ID)

dictPWD = {param_PWD[0]:"",param_PWD[1]:"",param_PWD[2]:"",param_PWD[3]:"",param_PWD[4]:"",param_PWD[5]:""}
listPWD = list(dictPWD)

#-> get each image of each button from the virtual keyboard
index = 0
for lineNum in range(16):
    id_image = "val_cel_"+ str(index)
    img = driver.find_element_by_id(id_image).screenshot_as_png
    image = Image.open(io.BytesIO(img))
    image.save('img/'+id_image+'.png')
    index += 1

#-> Match for first pwd digit
for element in range(len(listPWD)):

    # load Reference image for the current password digit
    if (param_HEADLESS_PROCESS):
        referenceDIR = 'REF_HEADLESS'
    else:
        referenceDIR = 'REF_LIVE_MODE'

    referenceImage = 'img/'+referenceDIR+'/'+listPWD[element]+'_REF.png'
    referenceIMG = cv2.imread(referenceImage)

    # 2) Check for similarities between the 2 images
    for index in range(16):

        localImage = 'val_cel_'+str(index)

        localIMG = cv2.imread('img/'+localImage+'.png')

        # convert the images to grayscale
        gray_referenceIMG = cv2.cvtColor(referenceIMG, cv2.COLOR_BGR2GRAY)
        gray_localIMG = cv2.cvtColor(localIMG, cv2.COLOR_BGR2GRAY)

        # compute the Structural Similarity Index (SSIM) between the two
        # images, ensuring that the difference image is returned
        (score, diff) = compare_ssim(gray_referenceIMG, gray_localIMG, full=True)

        if (score > 0.98):
            # print("SCORE=",score," LOCAL=",localImage,"REFERENCE=",referenceImage)
            dictPWD[listPWD[element]]=localImage
            break  #once we find the good match then skip to next pwd digit to search

#-> click on each button corresponding to the password
for digit in param_PWD:
    element = dictPWD.get(digit)
    driver.find_element_by_id(element).click()

#-> then click on Validate button
driver.find_element_by_id("valider").click()
driver.get("https://voscomptesenligne.labanquepostale.fr/voscomptes/canalXHTML/relevePdf/relevePdf_synthese/initPourCompteSelectionne-syntheseRelevesPDF.ea?compteNumero="+param_NumeroDeCompte)

#-> before downloading the file, get the list of same file in the directory
ListFileBefore = glob.glob(param_DownloadFolder+'\\releve_CCP*.pdf')

driver.find_element_by_class_name(name="compte").click()
driver.get("https://voscomptesenligne.labanquepostale.fr/voscomptes/canalXHTML/relevePdf/relevePdf_synthese/refPDF-syntheseRelevesPDF.ea?indexCompteReleves=0&indexReleve=0")

time.sleep(10)  #let some seconds to download before stopping the webdriver
driver.quit()   # kill the firefox instance

#-> after downloading the file, get the list of same file in the directory
ListFileAfter = glob.glob(param_DownloadFolder+'\\releve_CCP*.pdf')

newFile = ( (list(set(ListFileAfter) - set(ListFileBefore))) )[0]

print("New file downloaded to directory: ",os.path.basename(newFile))
