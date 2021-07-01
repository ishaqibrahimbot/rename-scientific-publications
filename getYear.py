"""
A simple function to extract a YYYY format date from the date string extracted by Grobid
"""

def get_year(date):
    date = date.split()

    numerals = "0123456789"
    num_numerals = 0
    
    for portion in date:
        for character in portion:
            if character in numerals:
                num_numerals+=1

        if num_numerals >= 4:
            return portion
        else:
            num_numerals = 0
