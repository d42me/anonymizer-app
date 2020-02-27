
# Import libraries 
from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os
import random
import string
  
# Converts a PDF file into plain text
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