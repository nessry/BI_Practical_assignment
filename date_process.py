# -*- coding: utf-8 -*-
"""
@author: Nessrine Hammami

This file contains date preparation step
"""

from datetime import datetime
import re
from dateutil.parser import parse

# Regex of possible valid date format
date_regex=[r"[\d]{1,2}/[\d]{1,2}/[\d]{2}",r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember))\s+\d{1,2}\,\s+\d{4}',
            r'\d{1,2}\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember))\s+\d{4}',r"[\d]{1,2}/[\d]{1,2}/[\d]{4}",
            r"[\d]{1,2}-[\d]{1,2}-[\d]{4}",r"[\d]{1,2}.[\d]{1,2}.[\d]{4}",r"[\d]{4}-[\d]{1,2}-[\d]{1,2}",r"[\d]{1,2} [ADFJMNOS]\w* [\d]{4}",r"(\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4})",
            r"[ADFJMNOS]\w*[\d]{1,2}\,[\d]{4}",r'\d{1,2}\-(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember))\-\d{4}',
            r'\d{1,2}\-(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember))\-\d{2}']


# Check whether a string can be interpreted as a valid date format
def is_date(string):
    dt = "None"
    string = string.replace("\n","")
    for elem_dt in date_regex:
        if re.findall(elem_dt,string):
            dt = re.findall(elem_dt,string)[0]
            break
    return dt

# Extract date and convert it to the format "Day - Month - Year"    
def convert_date_treatment(text_val):
    try:
        val  = is_date(text_val) # Check whether a string can be interpreted as a valid date format
        converted_date = datetime.strftime(parse(val), '%d %B %Y')
        final_date = datetime.strptime(converted_date, '%d %B %Y')
        # Two digits year is interpreted in a wrong way
        if final_date.year > 2020:
            final_date = final_date.replace(final_date.year-100)
        final_date = datetime.strftime(final_date, '%d %B %Y')
    except:
        final_date = text_val
    return final_date