def send_email():
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    sender_email = "dobbyaturservice@gmail.com"
    recipient = "arpitjain101992@gmail.com"
    password = "Covid@2021"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Vaccine slot test"
    message["From"] = sender_email
    message["To"] = recipient

    # Create the plain-text and HTML version of your message
    html = f"""\
    <html>
    <body>
        <p>Hi,<br>
        Please find below vaccine slot availablity for you,<br>
        <a href="https://www.cowin.gov.in/home">Click here to book the appointment</a>
        </p>
        <p>Please reply back to us on this email if you dont want to receive the updates anymore.</p>
        <p>Regards,<br>
        Team Dobby<br>
        </p>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part2)

    # # Create secure connection with server and send email
    # FROM = user
    # TO = recipient if isinstance(recipient, list) else [recipient]
    # SUBJECT = subject
    # TEXT = body

    # # Prepare actual message
    # message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    # """ % (
    #     FROM,
    #     ", ".join(TO),
    #     SUBJECT,
    #     TEXT,
    # )
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient, message.as_string())
        server.close()
        print("successfully sent the mail")
    except:
        print("failed to send mail")


send_email()
