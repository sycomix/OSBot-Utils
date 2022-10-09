from html import escape, unescape

def html_escape(value):
    return escape(value)

def html_unescape(value):
    return unescape(value)


html_encode = html_escape
html_decode = html_unescape