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
    "name": "Simple MAIL",
    "description": "this is used for testing simple mail",
    "email_subject": "This is your IMAGE",
    "is_html": False,
    "no_of_attachments": 0,
}

shipment_data[
    "email_content"
] = """
Hello {{ recipient_name }},

This is a sample email template using Jinja for dynamic content. You can include plain text content here and customize it according to your needs.

Here are some dynamic details:
- Email Address: {{ recipient_email }}
- Account Balance: ${{ account_balance }}

Feel free to add more paragraphs, bullet points, or any other plain text elements.

Best regards,
Your Name
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
