from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from analyzer import AnalyzerEngine
from PIL import Image
import pytesseract 
import sys 
from pdf2image import convert_from_path 
from flask_cors import CORS
import random
import string
import os

# Static definitions
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}

# Start the Presidio Engine (https://github.com/microsoft/presidio)
engine = AnalyzerEngine()

# Initialize Flask
app = Flask(__name__)

# Allow CORS
CORS(app)

# Set upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

''' 
Part #1 - Helper Functions
'''

# Helper function which converts a PDF file into plain text
def convert_pdf_to_text(pdf_file_url):  
    
    ''' 
    Part #1 : Converting PDF to images 
    '''
    
    # Store all the pages of the PDF in a variable 
    pages = convert_from_path(pdf_file_url, 500)

    # Variable to store all the file names
    filenames = []
    
    # Iterate through all the pages stored above 
    for page in pages: 
    
        # Declaring filename for each page of PDF as JPG 
        # For each page, filename will be: 
        # PDF page 1 -> page_xxxxxx.jpg 
        # PDF page 2 -> page_xxxxxx.jpg 
        # PDF page 3 -> page_xxxxxx.jpg
        # xxxxx is a random string
        # PDF page n -> page_xxxxxx.jpg 
        filename = "./uploads/images/page_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) + ".jpg"
        filenames.append(filename)
        
        # Save the image of the page in system 
        page.save(filename, 'JPEG')
    
    ''' 
    Part #2 - Recognizing text from the images using OCR 
    '''
    
    # Result variable to store all text content
    res = ""
    
    # Iterate from 1 to total number of pages 
    for filename in filenames: 
            
        # Recognize the text as string in image using pytesserct 
        text = str(((pytesseract.image_to_string(Image.open(filename))))) 
    
        # The recognized text is stored in variable text 
        # Any string processing may be applied on text 
        # Here, basic formatting has been done: 
        # In many PDFs, at line ending, if a word can't 
        # be written fully, a 'hyphen' is added. 
        # The rest of the word is written in the next line 
        # Eg: This is a sample text this word here GeeksF- 
        # orGeeks is half on first line, remaining on next. 
        # To remove this, we replace every '-\n' to ''. 
        text = text.replace('-\n', '')     
    
        # Finally, store the processed text in the result variable. 
        res += text
    
    # Return the result variable aka complete text content
    return res

# Helper function to anonymize input text by using Presidio's Engine
# Returns anonymized text
def anonymize(inputText):
    response = engine.analyze(correlation_id=0,
                          text = inputText,
                          entities=[],
                          language='en',
                          all_fields=True,
                          score_threshold=0.5)
    temp = list(inputText)
    for item in response:
        print("Start = {}, end = {}, entity = {}, confidence = {}".format(item.start,
                                                                      item.end,
                                                                      item.entity_type,
                                                                      item.score))
        for i in range(item.start, item.end):
            temp[i] = "x"
    inputText = "".join(temp)
    return inputText

# Helper function which checks for allowed upload file format
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

''' 
Part #2 - Server Routes
'''

# Entry point route handler
@app.route('/')
def index():
    return 'Hello world'

# Upload route handler
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # If POST Request: return anonymized text
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            path = app.config['UPLOAD_FOLDER'] + '/' + filename
            text_converted = convert_pdf_to_text(path)
            text = anonymize(text_converted)
            return text

    # If GET Request: return simple html form with upload functionality
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

# Route to display uploaded file content
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')