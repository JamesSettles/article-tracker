import re
from pypdf import PdfReader
from datetime import datetime

class ArticleData:
    """
    Class for storing article data
    """
    def __init__(self, title:str, author:str, date_submitted:datetime, page_count:int, word_count:int):
        if not isinstance(date_submitted, datetime):
            raise TypeError(f"date_submitted must be a datetime object, not {type(date_submitted)}")
        if not isinstance(word_count,int):
            raise TypeError(f"word_count must be an int, not {type(word_count)}")
        if not isinstance(page_count,int):
            raise TypeError(f"page_count must be an int, , not {type(page_count)}")

        self.title = title
        self.author = author
        self.date_submitted = date_submitted
        self.page_count = page_count
        self.word_count = word_count
    
    def __str__(self):
        return (f"Title: {self.title}\n"
                f"Author: {self.author}\n"
                f"Page Count: {self.page_count}\n"
                f"Date Submitted: {self.date_submitted.strftime('%Y-%m-%d')}\n"
                f"Word Count: {self.word_count}")
    
def convert_to_datetime(date_str):
    """
    Converts a string in the format YYYY-MM-DD to a datetime object.
    """
    # Define the format of the date string
    date_format = "%Y-%m-%d"
    try:
        # Convert the date string to a datetime object
        date_obj = datetime.strptime(date_str, date_format)
        return date_obj
    except ValueError as e:
        # Handle invalid date format
        print(f"Error: {e}")
        return None

def get_text_and_pg_count_from_file(file):
    """
    Uses PdfReader to extract text from PDF file object. Returns a string with all the PDF text and a count of pages
    """
    if file is None:
        raise TypeError("Input is NoneType")
    
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text,len(reader.pages)

def clean_text(text:str)->list:
    """
    Cleans text using regex. Returns a list of all words in text.
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

def save_article_data_to_memory_file(article_data:ArticleData,filename:str):
    """
    Saves article data to a memory file. If there is no existing memory file this creates a new one.
    """
    entry_number = 1

    # Read existing entries if the file exists
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("Entry Number:"):
                    entry_number = int(line.split(":")[1].strip()) + 1
    except FileNotFoundError:
         # File does not exist, create a new one
            with open(filename, 'w') as file:
                pass

    # Append the new entry
    with open(filename, 'a') as file:
        file.write(f"Entry Number: {entry_number}\n")
        file.write(f"Title: {article_data.title}\n")
        file.write(f"Author: {article_data.author}\n")
        file.write(f"Page Count: {article_data.page_count}\n")
        file.write(f"Date Submitted: {article_data.date_submitted.strftime('%Y-%m-%d')}\n")
        file.write(f"Word Count: {article_data.word_count}\n")
        file.write("\n")  # Add a newline for separation between entries