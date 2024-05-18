# XRechnung XML Generator

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Introduction
The **XRechnung XML Generator** is a tool designed to generate XML files that comply with the XRechnung standard from CSV exports. XRechnung is an XML-based semantic data model used for electronic invoices, particularly in transactions with public clients in Germany. Starting January 1, 2025, all companies will be required to issue and receive e-invoices in accordance with EN 16931.

## Table of Contents
1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Adding a New UBL Template](#adding-a-new-ubl-template)
5. [Contributing](#contributing)
6. [License](#license)
7. [Contact](#contact)

## Features
- Generate XRechnung-compliant XML files from CSV inputs.
- Supports multiple UBL template versions.
- Simple command-line interface for generating executable files.

## Installation
To install and set up the project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/xSentry/xrechnungs-generator.git
    cd xrechnungs-generator
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. To create an executable file, run:
    ```bash
    pyinstaller main.spec
    ```

4. The new executable file (`xRechnung-v*.exe`) will be located in the `dist/` folder. Replace `*` with the version number.

## Usage
To generate XML files using the tool:

1. Place your CSV file in the appropriate directory.
2. Run the executable or the `main.py` script.
3. Follow the prompts to select the CSV file and desired output location.

## Adding a New UBL Template
To add a new UBL template, follow these steps:

1. Create a template in the `/templates/` folder with the format `ubl-VERSION_NUMBER-xrechnung-template.xml`.
2. Add the version number to the array on line 81 of `main.py`:
    ```python
    self.selectUblVersion.addItems(['3.0.1', 'VERSION_NUMBER'])
    ```
3. Update `main.spec` to include the new template file in the `datas` field:
    ```python
    datas=[('templates/ubl-3.0.1-xrechnung-template.xml', 'templates'), ('templates/ubl-VERSION_NUMBER-xrechnung-template.xml', 'templates')],
    ```
4. Generate a new executable as described in the Installation section.

## Contributing
We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
    ```bash
    git checkout -b feature-name
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add feature-name"
    ```
4. Push to the branch:
    ```bash
    git push origin feature-name
    ```
5. Create a Pull Request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For questions or support, please open an issue on the GitHub repository or contact the maintainer directly through GitHub.
