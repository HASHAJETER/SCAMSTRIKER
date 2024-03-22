
import imaplib
import email
from bs4 import BeautifulSoup
import re

# Function to fetch emails and extract URLs
def fetch_emails(username, password, server="imap.SERVER.com", folder="INBOX"):
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(server)
    mail.login(username, password)
    mail.select(folder)

    # Search for all unseen emails
    result, data = mail.search(None, "UNSEE")
    email_ids = data[0].split()

    for email_id in email_ids:
        # Fetch the email data
        result, data = mail.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Check if email is multipart
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                # If part is HTML, extract URLs
                if "text/html" in content_type and "attachment" not in content_disposition:
                    html_content = part.get_payload(decode=True).decode()
                    urls = extract_urls_from_html(html_content)
                    print("\nURLs found in email:", urls)
        else:
            content_type = msg.get_content_type()
            body = msg.get_payload(decode=True).decode()

            # If content is HTML, extract URLs
            if "text/html" in content_type:
                urls = extract_urls_from_html(body)
                print("URLs found in email:", urls)

    mail.close()
    mail.logout()

# Function to extract URLs from HTML content
def extract_urls_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    urls = []
    for link in soup.find_all("a", href=True):
        urls.append(link["href"])
    return urls

# Example usage
if __name__ == "__main__":
    # Enter your email credentials and server details
    username = "mail"
    password = "pass"
    server = "imap.SERVER.com"

    fetch_emails(username, password, server)
