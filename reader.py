from re import finditer, Match

# IMPORT pytesseract, module for 'Google Tesseract OCR' image-to-text processor
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

# IMPORT system-specific variables
import config


# PATH to Google Tesseract OCR ['...\Tesseract-OCR\tesseract']
pytesseract.pytesseract.tesseract_cmd = config.tesseract_exe_install_path


# FUNCTION Definitions
def regex_search_img(_path: str, _pattern: str) -> Match:
    """Input image path, returns re.Match object with regex full matches

    :param _path: str, path to image [.jpeg/.png/.jpg/.gif]
    :param _pattern: str, regex pattern to re.finditer with
    :return: iteratable containing re.Match objects
    """
    pyt_list = pytesseract.image_to_string(Image.open(_path))
    img_str = ''.join(pyt_list)
    return finditer(
                _pattern,
                img_str)


def group_separated_list(re_iterable) -> list:
    """Extracts named group from re.Match object and places it into correspon-
       ding list within returned list

   :param re_iterable: iterable, contains re.Match objects
   :return: list of lists, one in order appended, one for (?P<full>), and one
                           for (?P<nonum>)  (ex) [[<ord>], [<full>], [<nonum>]]
   """
    matches = [[], [], []]
    for item in re_iterable:
        if item.group('full'):
            matches[0].append(item.group('full'))
            matches[1].append(item.group('full'))

        elif item.group('nonum'):
            matches[0].append(item.group('nonum'))
            matches[2].append(item.group('nonum'))

        else:
            raise ValueError
    return matches


def filter_str(_str: str) -> tuple:
    """Turns uncommon symbols into ' ', calls str.split(' '), trims
       with str.strip()

    :param _str: str, to be filtered and formatted
    :return: list, of words in-order
    """
    filter_dict = dict.fromkeys(map(ord, '@#$.+=*&%()'), ' ')
    filtered_str = _str.translate(filter_dict)
    return filtered_str.strip()


if __name__ == "__main__":
    img_matches = regex_search_img(
                r'src/img/salmon.jpg',
                r'(?P<full>((\d+/\d+)|\d+)([^\w\n]{1,3}\b[a-zA-Z.,!]+\b)+)|'
                r'(?P<nonum>[^\d\n]{10,}[ ]{1,3})')
    matches = group_separated_list(img_matches)

    for i in (1, 2):
        for j in range(len(matches[i])):
            matches[i][j] = filter_str(matches[i][j])

    print(matches)
