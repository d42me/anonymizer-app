# Flask backend

## Project setup
First of all please follow the installation guidelines from Presidio, which can be found here: https://github.com/microsoft/presidio/blob/master/docs/deploy.md#install-presidio-analyzer-as-a-python-package. Run them in the backend folder of our project.

After that install the following Python3 packages:

```
pip3 install flask pytesseract pdf2image flask_cors
```

Also please make sure to install PIL and Tesseract.

### Compiles and hot-reloads for development
```
python3 server.py
```
