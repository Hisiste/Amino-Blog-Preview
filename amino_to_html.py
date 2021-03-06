"""
This will convert text from an Amino Blog style, to HTML.
"""

import os

def get_text(fileName):
    """Opens a file and returns every line of it."""
    try:
        with open(fileName, "r", encoding="utf-8") as f:
            return f.readlines()

    except IOError as e:
        print("{}\nError opening {}. Terminating program.".format(e, file),
                file=sys.stderr)
        sys.exit(1)

def check_for_URL(line):
    bracketO = -1
    bracketC = -1
    pairs = []

    for letter_pos in range(len(line)):
        if   line[letter_pos] == '[':
            bracketO = letter_pos
        elif line[letter_pos] == ']' and bracketO != -1:
            bracketC = letter_pos
            if '|' in line[ bracketO+2 : bracketC-1 ]:
                pairs.append([bracketO, bracketC])
            bracketO = -1

    return pairs

def make_url(text):
    pos = check_for_URL(text)

    result = ''
    lastClose = 0

    for [bOpen, bClose] in pos:
        result += text[lastClose:bOpen]

        html =  "<a class='text-link' href='"
        html += text[ bOpen+1 : bClose ].split('|')[1]
        html += "' target='_blank'>"
        html += text[ bOpen+1 : bClose ].split('|')[0]
        html += "</a>"

        result += html
        lastClose = bClose + 1

    result += text[lastClose:]

    return result

def make_p(text, args = []):
    """Formats to HTML <p> having in count BICUS."""
    BICUS = {
            'B' : ' bold' ,
            'I' : ' italic' ,
            'C' : ' center' ,
            'U' : ' underline' ,
            'S' : ' strikethrough'
            }

    p = '<p class="line'
    for letter in args:
        p += BICUS[letter]
    p += '">' + text[:-1] + '</p>\n'

    return p

def check_duplicates(text):
    """Checks if there is any duplicate letter."""
    A = set()
    for letter in text:
        A.add(letter)
    if (len(A) == len(text)):
        return False
    return True

def make_figure(path, caption):
    figure =  "<figure class='img-container' tabindex='0' contenteditable='false'>\n"
    figure += "<div class='media-wrapper'><img src='"
    figure += os.path.join( os.path.dirname(__file__), path )
    figure += "'></div>\n"
    figure += "<figcaption>\n"
    figure += caption
    figure += "</figcaption>\n"
    figure += "</figure>\n"
    return figure
        
def bicus(text):
    """Formats wether there are valid Amino formatting, or not."""
    format_and_text = text.split(']')
    if (not check_duplicates(format_and_text[0]) and all(letter in 'BICUS' for letter in format_and_text[0][1:])):
        return make_p(format_and_text[1], format_and_text[0][1:])
    elif (format_and_text[0][1:5] == 'IMG='):
        return make_figure(format_and_text[0][5:], format_and_text[1])
    else:
        return make_p(text)

def amino_line_to_html(line):
    """Converts a line to HTML, with Amino formating."""
    line = make_url(line)

    if (line[0] == '[' and ']' in line):
        return bicus(line)
    else:
        return make_p(line)

def head_html():
    html =  "<!DOCTYPE html>\n"
    html += "<html>\n"
    html += "<head>\n"
    html += "<title>Page Title</title>\n"
    html += "<link rel='stylesheet' type='text/css' href='https://wa1.narvii.com/static/dist/css/1.dc5d9e4fb.css'>\n"
    html += "</head>\n"
    html += "<body>\n"
    html += "<div class='content-editor'>\n"
    return html

def bottom_html():
    html =  "</div>\n"
    html += "</body>\n"
    html += "</html>"
    return html


def main():
    Amino = input("Nombre del archivo > ")
    Output = input("Nombre de salida > ")

    AminoPath = os.path.join( os.path.dirname(__file__), Amino )
    OutputPath = os.path.join( os.path.dirname(__file__), Output )

    with open(Output, "w", encoding="utf-8") as out:
        out.write(head_html())
        for line in get_text(Amino):
            out.write(amino_line_to_html(line))
        out.write(bottom_html())

    print("Program ended with no errors :D")

if __name__ == "__main__":
    main()

