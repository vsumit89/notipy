import requests
from jinja2 import BaseLoader, Environment


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


def send_simple_message(html_content):
    # Attach file

    with open(attachment_path, "rb") as file:
        files = [("attachment", (attachment_path, file.read()))]

    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", f"{api_key}"),
        data={
            "from": f"Excited User <mailgun@{domain}>",
            "to": ["vsumit030201@gmail.com"],
            "subject": "Hello",
            "html": html_content,
        },
        files=files,
    )


# Replace these with your Mailgun API key, domain, and other details
api_key = "b12fc7ca061fd71b92da9e028d293b3f-0a688b4a-3679d9ea"
domain = "sandboxf025f1c5362f47f39394e138b9a67081.mailgun.org"
to_email = "vsumit030201@gmail.com"
email_subject = "Test Email"
email_text = "Hello, this is the email body."
attachment_path = "sample.pdf"


html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: 'Arial', sans-serif;
      margin: 0;
      padding: 0;
      background-color: #f4f4f4;
    }

    .container {
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
      background-color: #fff;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }

    h1 {
      color: #333;
    }

    p {
      color: #666;
    }

    .tracking-info {
      margin-top: 20px;
    }

    .tracking-info table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 15px;
    }

    .tracking-info table th,
    .tracking-info table td {
      padding: 10px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }

    .tracking-number {
      font-weight: bold;
    }

    .footer {
      margin-top: 20px;
      color: #888;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Shipping Information</h1>
    <p>Hello {{ customer_name }},</p>

    <div class="tracking-info">
      <p>Your order has been shipped! Here are the details:</p>

      <table>
        <tr>
          <th>Order ID</th>
          <td>{{order_id}}</td>
        </tr>
        <tr>
          <th>Shipping Date</th>
          <td>{{shipping_date}}</td>
        </tr>
        <tr>
          <th>Estimated Delivery Date</th>
          <td>{{estimated_delivery_date}}</td>
        </tr>
        <tr>
          <th>Tracking Number</th>
          <td class="tracking-number">{{tracking_number}}</td>
        </tr>
      </table>
    </div>

    <div class="footer">
      <p>Thank you for choosing us!</p>
    </div>
  </div>
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

print(value.text)
 