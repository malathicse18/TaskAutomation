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
logging.basicConfig(filename='email_errors.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_valid_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

def send_emails(task):
    from database import save_email_log  # Import inside the function to avoid circular import

    emails = task.get("emails", [])
    subject = task.get("subject", "No Subject")
    message = task.get("message", "")
    attachment = task.get("attachment")
    user_details = task.get("user_details", {})

    logging.info(f"Starting Email Automation for {len(emails)} recipients.")

    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        logging.error("Email credentials missing. Check .env file!")
        return

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    except Exception as e:
        logging.error(f"Failed to connect to SMTP server: {e}")
        return

    for email in emails:
        if not is_valid_email(email):
            logging.warning(f"Invalid email address: {email}")
            continue

        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        if attachment:
            if os.path.exists(attachment):
                try:
                    with open(attachment, "rb") as attachment_file:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment_file.read())
                        encoders.encode_base64(part)
                        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment)}")
                        msg.attach(part)
                except Exception as e:
                    logging.error(f"Error reading attachment {attachment}: {e}")
                    continue
            else:
                logging.error(f"Attachment file {attachment} not found!")
                continue

        try:
            server.sendmail(EMAIL_SENDER, email, msg.as_string())
            logging.info(f"Email sent successfully to {email}")
            save_email_log(email, subject, message, "sent")
        except Exception as e:
            logging.error(f"Failed to send email to {email}: {e}")
            save_email_log(email, subject, message, "failed", str(e))

    server.quit()

def email_automation(args):
    from database import save_email_task

    try:
        with open(args.get('file', ''), "r") as f:
            reader = csv.reader(f)
            emails = [row[0] for row in reader if row]
    except FileNotFoundError:
        logging.error(f"File {args.get('file', '')} not found!")
        return

    valid_emails = [email for email in emails if is_valid_email(email)]
    if not valid_emails:
        logging.info("No valid email addresses found.")
        return

    user_details = {
        "user_id": f"{args.get('user_email', 'unknown')}_{uuid.uuid4()}",
        "name": args.get('user_name', 'Unknown'),
        "email": args.get('user_email', 'Unknown')
    }

    task = {
        "emails": valid_emails,
        "subject": args.get('subject', "No Subject"),
        "message": args.get('message', ""),
        "attachment": args.get("attachment"),
        "user_details": user_details
    }

    save_email_task(
        valid_emails, args.get('subject', "No Subject"), args.get('message', ""), task.get("attachment"),
        schedule_hour=args.get('schedule_hour'), schedule_minute=args.get('schedule_minute'), frequency=args.get('frequency'),
        user_details=user_details
    )
    send_emails(task)
