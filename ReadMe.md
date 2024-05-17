<div>
    <h1>
        XRechnung - XML Generator
    </h1>
</div>

<div>
    <strong>
        Generate XML Files from CSV-Files to use as an XRechnung.
    </strong>
    <br>
    XRechnung is an XML-based semantic data model that has been established as a standard for electronic invoices and is used in particular in the exchange of invoices with public clients in Germany.
    <br>
    In principle, all companies should be able to issue and receive e-invoices in accordance with EN 16931 from January 1, 2025
    <br>
    <br>
</div>

# New exe-Build

1. Run PyInstaller

    `pyinstaller main.spec`

2. The new `xRechnung-v.exe` is located under the `dist/` folder

3. Enter the versioning after the `v`. E.g.: `xRechnung-v1.0.exe`

# Add a new UBL template

1. Create a template in the `/templates/` folder with the format `ubl-VERSION_NUMBER-xrechnung-template.xml`

2. Add the version number to the array on line 81 of `main.py`. E.g. `self.selectUblVersion.addItems(['3.0.1', 'VERSION_NUMBER'])`

3. Add the new template file in the `main.spec` to the `datas` field. E.g.

    `datas=[('templates/ubl-3.0.1-xrechnung-template.xml', 'templates'), ('/ubl-VERSION_NUMBER_-xrechnung-template.xml', 'templates')],`

4. Generate new exe build (see above)

# Important links for XRechnung

Schema specifications come from [Peppol](https://peppol.eu)

The structure for XRechnung in UBL 3.0 format is available here [Peppol BIS Billing 3.0](https://docs.peppol.eu/poacc/billing/3.0/) and here [Invoice Tree](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/tree/)

A test suite is available on the Github repository [itplr-kosit/xrechnung-testsuite](https://github.com/itplr-kosit/xrechnung-testsuite) with matching [XML-Templates](https://github.com/itplr-kosit/xrechnung-testsuite/tree/master/src/test/business-cases/standard)
