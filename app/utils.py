import re

def DateType(date):
    date_pattern = re.compile('^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$')
    if not (date_pattern.match(date)):
        raise ValueError('Date must be in YYYY-MM-DD format.')    
    return date