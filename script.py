import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import streamlit as st
import os
from streamlit_quill import st_quill
# import os, yaml


# with open("config.yml", "r") as file:
#     config = yaml.safe_load(file)

SENDER_EMAIL = "yourEmail"
SENDER_PASSWORD = "yourPass"

UPLOAD_FOLDER = "uploads"


# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def send_email(receiver_email, subject, message, attachment_path=None):
    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the message body
    msg.attach(MIMEText(message, 'html'))

    # Attach the PDF file if provided
    if attachment_path:
        part = MIMEBase('application', 'octet-stream')
        with open(attachment_path, 'rb') as attachment:
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
        msg.attach(part)

    # Connect to the SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()

        # Log in to the email server
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Send the email
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())


st.title("Email Sender")
email = st.text_area('Enter recipient\'s email addresses:')
# name_input = st.text_area("Enter names")
subject = st.text_input('Enter the subject of your message:', 'Subject')
# message = st.text_area('Write your message here:', height=200)

# Spawn a new Quill editor
message = st_quill(placeholder='Enter text...', html=True)

attachment_file = st.file_uploader("Choose a PDF file for attachment", type="pdf")

if st.button("send email"):
    # print(message)
    if len(email) > 0:
        emails = email.split(",")
        # names = name_input.split(",")
        for i, receiver_email in enumerate(emails):
            # new_msg = message.replace("{name}", names[i].strip())

            attachment_path = None
            if attachment_file:
                print(attachment_file.read())
                uploaded_file_path = os.path.join(UPLOAD_FOLDER, attachment_file.name)
                with open(uploaded_file_path, "wb") as f:
                    f.write(attachment_file.getvalue())

                attachment_path = uploaded_file_path

            send_email(receiver_email.strip(), subject, message, attachment_path)
        st.success("Email sent successfully")
    else:
        st.error("Please enter a valid email address")
