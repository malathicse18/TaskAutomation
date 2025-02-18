import smtplib
import os
import csv
import logging
import re
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config import EMAIL_SENDER, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT

# Configure logging
logging.basicConfig(filename='email_errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def is_valid_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

def send_emails(task):
    from database import save_email_log  # Import inside the function to avoid circular import

    emails = task["emails"]
    subject = task["subject"]
    message = task["message"]
    attachment = task.get("attachment", None)
    user_details = task["user_details"]

    print(f"Running Email Automation with:\n"
          f"  📧 Emails: {len(emails)} recipients\n"
          f"  📝 Subject: {subject}\n"
          f"  💬 Message: {message}\n"
          f"  📎 Attachment: {attachment if attachment else 'None'}\n"
          f"  👤 User: {user_details['name']} ({user_details['email']})\n")

    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        print("❌ ERROR: Email credentials missing. Check .env file!")
        return

    for email in emails:
        if not is_valid_email(email):
            continue  # Skip invalid email addresses

        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        if attachment:
            try:
                with open(attachment, "rb") as attachment_file:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment_file.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {os.path.basename(attachment)}",
                    )
                    msg.attach(part)
            except FileNotFoundError:
                print(f"❌ ERROR: Attachment file {attachment} not found!")
                continue

        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, email, msg.as_string())
            server.quit()

            print(f"✅ Email sent successfully to {email}")
            save_email_log(email, subject, message, "sent")

        except Exception as e:
            error_message = str(e)
            logging.error(f"Failed to send email to {email} - Reason: {error_message}")
            save_email_log(email, subject, message, "failed", error_message)
            print(f"❌ Failed to send email to {email} - Check email_errors.log for details")

def email_automation(args):
    from database import save_email_task, save_user_details_in_task  # Import inside the function to avoid circular import

    try:
        with open(args['file'], "r") as f:
            reader = csv.reader(f)
            emails = [row[0] for row in reader if row]
    except FileNotFoundError:
        print(f"❌ ERROR: File {args['file']} not found!")
        return

    valid_emails = [email for email in emails if is_valid_email(email)]
    invalid_emails = [email for email in emails if not is_valid_email(email)]

    if invalid_emails:
        print("❌ Invalid email addresses found:")
        for email in invalid_emails:
            print(f"  - {email}")

    if not valid_emails:
        print("No valid email addresses to send.")
        return

    if not args['user_name']:
        print("❌ ERROR: User name is required!")
        return

    user_details = {
        "user_id": f"{args['user_email']}_{uuid.uuid4()}",
        "name": args['user_name'],
        "email": args['user_email']
    }

    task = {
        "emails": valid_emails,
        "subject": args['subject'],
        "message": args['message'],
        "attachment": getattr(args, "attachment", None),
        "user_details": user_details
    }

    save_email_task(valid_emails, args['subject'], args['message'], task.get("attachment", None), args.get('schedule'), user_details)
    send_emails(task)