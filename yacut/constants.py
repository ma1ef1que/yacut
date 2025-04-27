import string


SHORT_ID_LENGTH = 6
CHARACTERS = string.ascii_letters + string.digits
PATTERN = r'^[a-zA-Z0-9]{1,16}$'
MAX_URL_LENGTH = 2000