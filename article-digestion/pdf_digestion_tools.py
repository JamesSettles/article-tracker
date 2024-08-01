import re
from pypdf import PdfReader


def get_text_from_file(file)->str:
    """
    Uses PdfReader to extract text from PDF file object. Returns a string with all the PDF text.
    """
    if file is None:
        raise TypeError("Input is NoneType")
    
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def clean_text(text:str)->str:
    """
    Cleans text using regex.
    """

    if text is None:
        raise TypeError("Input is NoneType")
    if not isinstance(text,str):
        raise TypeError(f"Input is type {type(text)}, not a str")
    
    # use regex to split lowercase chars followed by uppercase chars, i.e "MoneyBox" -> "Money" "Box"
    text = re.split(r'(?<=[a-z])(?=[A-Z])', text)
    text = ' '.join(text) 
    # splits on common pdf conversion errors, for example "/n"
    text = re.split('[' ', ;, \., :, \n, \t]' , text)                                                                                                                                                                                                                                                                                                                                   
    text = [x for x in text if x] # remove empty strings  
    
    return text

