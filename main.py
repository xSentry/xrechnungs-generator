import os
import csv
import sys
import requests
from pathlib import Path
from datetime import datetime
from jinja2 import Template
from PyQt5.QtGui import QCursor, QPixmap, QIcon
from PyQt5.QtCore import Qt, QByteArray
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QFileDialog, QMessageBox, QLabel, QGridLayout, QComboBox, QDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('xrechnungs.gen')

from logofp import img
from logoicon import icon

class Invoice():
    def __init__(self):
        self.invoiceNumber = None
        self.leitwegID = None
        self.invoiceDate = None
        self.dueDate = None
        self.note = None
        self.dueDays = None #Berechnen
        self.periodStart = None
        self.periodEnd = None
        self.customerCompanyID = None #UmstID
        self.customerStreetname = None
        self.customerPostalZone = None
        self.customerCityname = None
        self.customerEmail = None
        self.customerCompanyName = None
        #Zusatzadresse
        self.priceNet = None
        self.priceFull = None
        self.priceTax = None #Berechnen
        self.positionName = None
        self.taxPercent = None
        self.ownStreetname = None
        self.ownPostalCode = None
        self.ownCityname = None
        self.ownCompanyName = None
        self.ownCompanyID = None #UmstID
        self.ownTaxNo = None #Steuernummer
        #ownContactCompanyName
        self.ownContactName = None
        self.ownContactPhone = None
        self.ownContactEmail = None
        self.ownIban = None
        self.ownBic = None
        self.ownAccountOwner = None
        self.ownHraNo = None #Handelsregisternummer
        self.ownHraName = None #Handelsregister Name

class XRechnungGenerator(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'XRechnungs Generator'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 100

        self.windowIcon = QPixmap()
        self.windowIcon.loadFromData(QByteArray.fromBase64(icon))
        self.setWindowIcon(QIcon(self.windowIcon))
        
        self.selectedFileName = None
        self.selectedUblVersion = None
        self.alertText = ''

        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, 220)

        selectUblVersionLabel = QLabel()
        selectUblVersionLabel.setStyleSheet("color: grey")
        selectUblVersionLabel.setText("Select UBL Version")
        self.selectUblVersion = QComboBox()
        self.selectUblVersion.addItems(['3.0.1'])

        self.selectedFileInfo = QLabel()
        self.selectedFileInfo.setStyleSheet("color: grey")

        buttonFileSelect = QPushButton('Select CSV')
        buttonFileSelect.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.buttonStartGen = QPushButton('Generate XRechnungen')
        self.buttonStartGen.setEnabled(False)
        self.buttonStartGen.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        buttonValidateXml = QPushButton('Validate XRechnung')
        buttonValidateXml.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        buttonFileSelect.clicked.connect(self.openFileNameDialog)
        self.buttonStartGen.clicked.connect(self.generateXRechnungFromCsv)
        buttonValidateXml.clicked.connect(self.openXmlValidationDialog)

        logo = QPixmap()
        logo.loadFromData(QByteArray.fromBase64(img))
        logoLabel = QLabel()
        logoLabel.setPixmap(logo)

        layout = QGridLayout(self)
        layout.setContentsMargins(50, 10, 50, 50)
        layout.setRowStretch(0 | 1 | 2 | 3 | 4, 25)
        layout.setColumnStretch(0 | 1 | 2, 25)
        layout.setColumnMinimumWidth(0, 400)
        layout.setColumnMinimumWidth(1, 400)
        layout.addWidget(logoLabel, 0, 0)
        layout.addWidget(selectUblVersionLabel, 1, 0)
        layout.addWidget(self.selectUblVersion, 2, 0)
        layout.addWidget(buttonValidateXml, 2, 1)
        layout.addWidget(self.selectedFileInfo, 3, 0)
        layout.addWidget(buttonFileSelect, 4, 0)
        layout.addWidget(self.buttonStartGen, 4, 1)
        
        self.show()
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Select Invoice-CSVs", "./","CSV Files (*.csv)", options=options)
        if fileName:
            self.selectedFileName = fileName
            self.selectedFileInfo.setText(fileName)
            self.buttonStartGen.setEnabled(True)

    def openXmlValidationDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Select XRechnung", "./rechnungen","XML Files (*.xml)", options=options)
        if fileName:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            self.validateXmlFile(fileName)

    def validateXmlFile(self, fileName):
        try:
            url = 'https://xrechnung-validator.demo.epoconsulting.com/'
        
            files = {'file': open(fileName, 'rb')}

            request = requests.post(url, files=files)
            response = request.text
            
            if (response):
                QApplication.restoreOverrideCursor()

                dialog = QDialog()
                dialog.setGeometry(100, 100, 0, 0)
                dialog.setStyleSheet('padding: 0')
                dialog.setFixedSize(900, 800)
                dialog.setWindowIcon(QIcon(self.windowIcon))
                dialog.setWindowTitle('Validate XRechnung')

                htmlView = QWebEngineView(dialog)
                htmlView.setHtml(response)
                htmlView.setGeometry(0, 0, 900, 800)
                dialog.exec_()
        except:
            self.alertText = 'Validating XML failed. Is the file format correct and an internet connection available?'
            self.openAlert()

    def openAlert(self):
        windowIcon = QPixmap()
        windowIcon.loadFromData(QByteArray.fromBase64(icon))

        alert = QMessageBox()
        alert.setWindowIcon(QIcon(windowIcon))
        alert.setWindowTitle('XRechnung - An error has occurred!')
        alert.setText(self.alertText)
        alert.exec()
        self.alertText = ''

    def generateXRechnungFromCsv(self):
        if not self.selectedFileName or self.selectedFileName == '':
            return

        csvInvoices = []

        file = self.selectedFileName

        failedCsvImports = 0

        with open(file, 'r') as f:
            reader = csv.reader(f, delimiter=';')

            expectedCsvStructure = ['RECHNUNGSNUMMER', 'LEITSTELLEN_ID_KUNDE', 'RECHNUNGSDATUM', 'FAELLIGKEITSDATUM', 'LEISTUNGSDATUM_BEGINN', 'LEISTUNGSDATUM_ENDE', 'UMST_ID_KUNDE', 'ADRESSE', 'PLZ', 'ORT', 'EMAIL_KUNDE', 'FIRMENNAME_KUNDE', 'NETTOPREIS', 'BRUTTOPREIS', 'LEISTUNGSNAME', 'MEHRWERTSTEUER', 'EIGENE_ADRESSE', 'EIGENE_PLZ', 'EIGENER_ORT', 'EIGENER_FIRMENNAME', 'EIGENE_UMST_ID', 'EIGENE_STEUERNUMMER', 'EIGENER_ANSPRECHPARTNER_NAME', 'EIGENER_ANSPRECHPARTNER_TELEFON', 'EIGENER_ANSPRECHPARTNER_EMAIL', 'IBAN', 'BIC', 'KONTOINHABER', 'REGISTERNUMMER', 'REGISTERGERICHT', 'NOTIZ']

            for index, row in enumerate(reader):
                if index == 0:
                    if row != expectedCsvStructure:
                        self.alertText = 'The CSV file is in an incorrect format! \n \n Expected: \n' + str(expectedCsvStructure) + '\n \n Erhalten: \n' + str(row)
                        self.openAlert()
                        return
                    continue

                invoice = Invoice()

                invoiceDate = datetime.strptime(row[2], '%d.%m.%Y').strftime('%Y-%m-%d')
                dueDate = datetime.strptime(row[3], '%d.%m.%Y').strftime('%Y-%m-%d')
                periodStartDate = datetime.strptime(row[4], '%d.%m.%Y').strftime('%Y-%m-%d')
                periodEndDate = datetime.strptime(row[5], '%d.%m.%Y').strftime('%Y-%m-%d')

                invoice.invoiceNumber = row[0]
                invoice.leitwegID = row[1]
                invoice.invoiceDate = invoiceDate
                invoice.dueDate = dueDate
                invoice.note = row[30]
                invoice.periodStart = periodStartDate
                invoice.periodEnd = periodEndDate
                invoice.customerCompanyID = row[6]
                invoice.customerStreetname = row[7]
                invoice.customerPostalZone = row[8]
                invoice.customerCityname = row[9]
                invoice.customerEmail = row[10]
                invoice.customerCompanyName = row[11].replace('&', '&amp;')
                invoice.priceNet = float(row[12].replace(',', '.'))
                invoice.priceFull = float(row[13].replace(',', '.'))
                invoice.priceTax = round(invoice.priceFull - invoice.priceNet, 2)
                invoice.positionName = row[14]
                invoice.taxPercent = row[15]
                invoice.ownStreetname = row[16]
                invoice.ownPostalCode = row[17]
                invoice.ownCityname = row[18]
                invoice.ownCompanyName = row[19].replace('&', '&amp;')
                invoice.ownCompanyID = row[20]
                invoice.ownTaxNo = row[21]
                invoice.ownContactName = row[22]
                invoice.ownContactPhone = row[23]
                invoice.ownContactEmail = row[24]
                invoice.ownIban = row[25]
                invoice.ownBic = row[26]
                invoice.ownAccountOwner = row[27]
                invoice.ownHraNo = row[28]
                invoice.ownHraName = row[29]

                invoiceDateObject = datetime.strptime(invoice.invoiceDate, '%Y-%m-%d')
                dueDateObject = datetime.strptime(invoice.dueDate, '%Y-%m-%d')

                dateDiff = dueDateObject - invoiceDateObject
                invoice.dueDays = dateDiff.days

                csvInvoices.append(invoice)

        if failedCsvImports == 1:
            self.alertText = str(failedCsvImports) + ' CSV entry was incorrect and could not be imported!'
            self.openAlert()

        if failedCsvImports > 1:
            self.alertText = str(failedCsvImports) + ' CSV entries were incorrect and could not be imported!'
            self.openAlert()

        Path("./rechnungen").mkdir(exist_ok=True)

        for invoice in csvInvoices:
            templateFile = resource_path('./templates/ubl-' + self.selectUblVersion.currentText() + '-xrechnung-template.xml')
            with open(templateFile, encoding='utf-8') as xrechnung:
                template = Template(xrechnung.read())

            renderedXml = template.render(data=invoice)

            with open('./rechnungen/' + invoice.invoiceNumber + '.xml', 'w', encoding='utf-8') as renderedXRechnung:
                renderedXRechnung.write(renderedXml)

        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(__file__)

        folderPath = application_path + '/rechnungen'
        os.startfile(
            folderPath
        )

def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

app = QApplication(sys.argv)

app.setStyle('Fusion')

ex = XRechnungGenerator()
sys.exit(app.exec_())