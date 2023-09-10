import re, random, string, uuid, secrets
from flask_mail import Message


class Flash_Messages:
    error = 'error'
    info = 'info'
    Warning = 'warning'
 
def validate_email(email):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.match(pattern, email):
        return True
    else:
        return False
    
def validate_name(name):
    # Regular expression pattern to match names
    pattern = r"^[A-Za-z\s'-]+$"

    # Check if the name matches the pattern
    if re.match(pattern, name):
        return True
    else:
        return False
    
# Minimum 8 characters.
# The alphabet must be between [a-z]
# At least one alphabet should be of Upper Case [A-Z]
# At least 1 number or digit between [0-9].
# At least 1 character from [ _ or @ or $ ].
    
def validate_password(password):
    flag = 0
    if (len(password)<=8):
        flag = -1
    elif not re.search("[a-z]", password):
        flag = -1
    elif not re.search("[A-Z]", password):
        flag = -1
    elif not re.search("[0-9]", password):
        flag = -1
    elif not re.search("[_@$]" , password):
        flag = -1
    elif re.search("\s" , password):
        flag = -1

    if flag == -1:
        return False
    else:
        return True
    
def validate_filename(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename():
    # Generate a unique identifier (UUID)
    unique_id = str(uuid.uuid4())

    # Generate a random string
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    # Combine the unique identifier and random string to form the file name
    file_name = unique_id + '_' + random_string

    return file_name

def convert_text_to_html(text):
    text = text.strip()
    text = re.sub(r'\n+', '\n', text, count=re.DOTALL, flags=re.DOTALL)
    text = re.sub(r'\n+\s', '', text, count=re.DOTALL, flags=re.DOTALL)
    paragraphs = text.split("\n")  # Split text into paragraphs

    # Trim leading and trailing white spaces in each paragraph
    paragraphs = [paragraph.strip() for paragraph in paragraphs]

    # Wrap each paragraph in <p> tags
    paragraphs_with_tags = ['<p>{}</p>'.format(paragraph) for paragraph in paragraphs]

    # Join the paragraphs with tags into a single string
    wrapped_text = '\n'.join(paragraphs_with_tags)

    return wrapped_text

import re

def convert_html_to_text(html_text):
    # Remove <p> tags and extract the inner text
    inner_text = re.sub(r'<p>', '', html_text, flags=re.DOTALL)
    inner_text = re.sub(r'</p>', '', inner_text, flags=re.DOTALL)

    # Normalize line breaks by replacing consecutive line breaks with a single '\n'
    normalized_text = re.sub(r'\n+', '\n', inner_text)

    # Remove leading and trailing whitespace
    trimmed_text = normalized_text.strip()

    return trimmed_text

def remove_milliseconds(datetime_str):
    # Split the datetime string at the dot and exclude the last item (milliseconds)
    parts = datetime_str.split('.')
    formatted_datetime = '.'.join(parts[:-1])
    return formatted_datetime

def format_price(price):
    # Convert input to float
    price = float(price)
    formatted_price = "{:.2f}".format(price)
    return formatted_price

def generate_activation_token(length=32):
    # Define characters to be used in the token
    characters = string.ascii_letters + string.digits
    # Generate a random token of specified length
    token = ''.join(secrets.choice(characters) for _ in range(length))
    return token

def create_activation_email(website, user):
    subject = f'{website.name} Email Activation'
    sender = f'noreply@{website.name}'
    recipients = [user.email]
    activation_link = f'{website.address}/activate-account/{user.email}/{user.activation_token}'
    html = f'''
        <h2>Click the link to activate your account:</h2>
        <a href="{activation_link}">Activate Account</a>
    '''
    message = Message(subject=subject, sender=sender, recipients=recipients)
    message.html = html

    return message

