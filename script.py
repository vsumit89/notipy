import requests


class Shipment:
    def __init__(
        self,
        name,
        description,
        email_subject,
        is_html,
        email_content,
        no_of_attachments,
    ):
        self.name = name
        self.description = description
        self.email = {
            "subject": email_subject,
            "is_html": is_html,
            "content": email_content,
            "no_of_attachments": no_of_attachments,
        }

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "channels": {"email": self.email},
        }


# Example usage:
shipment_data = {
    "name": "FORGOT PASSWORD",
    "description": "this is used for forgot password",
    "email_subject": "Please reset your password",
    "is_html": True,
    "no_of_attachments": 0,
}

shipment_data[
    "email_content"
] = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }

        .container {
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        h2 {
            color: #333;
        }

        p {
            color: #666;
        }

        .button {
            display: inline-block;
            padding: 10px 20px;
            margin: 20px 0;
            text-decoration: none;
            background-color: #007BFF;
            color: #fff;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Password Reset</h2>
        <p>Dear {{ user }},</p>
        <p>We received a request to reset your password for {{ platform }}. To proceed with the password reset, please click the button below:</p>
        <a class="button" href="{{ reset_link }}">Reset Password</a>
        <p>If you did not request a password reset, please ignore this email. Your account security is important to us.</p>
        <p>Thank you for using {{ platform }}.</p>
        <p>Best regards,<br>{{ your_name }}<br>{{ your_company }}</p>
    </div>
</body>
</html>
"""
shipment_instance = Shipment(**shipment_data)


# Convert object to JSON
shipment_json = shipment_instance.to_json()
print(shipment_json)

# Make a POST request
url = "http://localhost:8000/api/v1/events"  # Replace with the actual API endpoint URL
headers = {
    "Content-Type": "application/json",
    # Add any other headers that your API requires
}
response = requests.post(url, headers=headers, json=shipment_json)

# Print the response
print(response.status_code)
print(response.text)
