"""
here some functions to extract links and emails.
"""
import re

__version__ = 0.1
__doc__ = "Find URLs in a text string"""

url_re = re.compile("(?:\w+://|www\.)[^ ,.?!#%=+][^ ][^ \r]*")
bad_chars = '\'\\.,[](){}:;"'

def FindUrls (text):
 return [s.strip(bad_chars) for s in url_re.findall(text)]


def FindEmails(text):
	emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text)
	return emails