import requests
from jinja2 import BaseLoader, Environment
from minio import Minio
from io import BytesIO
import mimetypes
import asyncio


def send_email(api_key, domain, to, subject, text, attachment_path):
    # Mailgun API endpoint
    url = f"https://api.mailgun.net/v3/{domain}/messages"

    # Mailgun API key
    api_key = f"api:{api_key}"

    # Email parameters
    data = {
        "from": f"Sumit Vishwakarma sumit.vishwakarma@factly.in",
        "to": to,
        "subject": subject,
        "text": text,
    }

    # Attach file
    # with open(attachment_path, "rb") as file:
    #     files = [("attachment", (attachment_path, file.read()))]

    # Make the request
    response = requests.post(url, auth=("api", api_key), data=data)

    # Print the response
    # Check for errors
    if response.status_code == 200:
        print("Email sent successfully!")
    else:
        print(f"Error {response.status_code}: {response.text}")


async def get_file_from_bucket(url):
    chunk_size = 1024 * 4
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # read file in chunks
            file = BytesIO()
            for chunk in response.iter_content(chunk_size=chunk_size):
                file.write(chunk)
            file.seek(0)
            print(url)

            file_ext = mimetypes.guess_extension(url)

            return file, file_ext or ".dat"
        else:
            raise Exception("unable to get file from bucket")
    except Exception as e:
        raise e


async def process_urls(urls):
    tasks = [get_file_from_bucket(url) for url in urls]
    files = await asyncio.gather(*tasks)
    attachments = []
    for i in files:
        attachments.append(("attachment", (f"file{i[1]}", i[0])))
    return attachments


def send_simple_message(html_content):
    # Attach file
    urls = [
        "http://localhost:9000/attachments/OD428525073160536100.pdf",
        "http://localhost:9000/attachments/Naval-Ravikant-TKP.pdf",
    ]

    files = asyncio.run(process_urls(urls))
    # for i in attachments:
    #     files.append(("attachment", (f"file{i[1]}", i[0])))

    print(files)

    # file = []
    # for i in attachments:
    #     file.append(i[0])

    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", f"{api_key}"),
        data={
            "from": f"Sumit Vishwakarma <vsumit030201@gmail.com>",
            "to": ["vsumit030201@gmail.com"],
            "subject": "Hello",
            "html": html_content,
        },
        files=files,
    )


# Replace these with your Mailgun API key, domain, and other details
api_key = "api_key"
domain = "domain"
to_email = "vsumit030201@gmail.com"
email_subject = "Test Email"
email_text = "Hello, this is the email body."
attachment_path = "sample.pdf"


html_content = """
       <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Your Email Title</title>
        </head>
        <body style="font-family: 'Arial', sans-serif;">

            <table role="presentation" cellspacing="0" cellpadding="0" width="100%">
                <tr>
                    <td align="center" style="padding: 40px 0;">
                        <img src="{{ dynamic_image_source }}" alt="Dynamic Image Alt Text" width="600" style="max-width: 100%;">
                    </td>
                </tr>
                <tr>
                    <td style="background-color: #f4f4f4; padding: 20px;">
                        <h2 style="color: #333;">Hello {{ name }}!</h2>
                        <p style="color: #666;">This is a sample email template with a dynamic image and customized greeting.</p>
                        <p style="color: #666;">Feel free to customize this template according to your needs.</p>
                        <p style="color: #3498db;"><a href="{{ dynamic_link_url }}" style="color: #3498db; text-decoration: none;">Click here</a> to visit our website.</p>
                    </td>
                </tr>
            </table>

        </body>
        </html>
"""

template_env = Environment(loader=BaseLoader())

# Example dynamic data
dynamic_data = {
    "customer_name": "John Doe",
    "order_id": "12345",
    "shipping_date": "2023-12-08",
    "estimated_delivery_date": "2023-12-15",
    "tracking_number": "ABC123456",
}


template = template_env.from_string(html_content)
rendered_template = template.render(dynamic_data)

# Send the email
value = send_simple_message(rendered_template)

# print(value.text)
