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
        sms_content,
    ):
        self.name = name
        self.description = description
        self.email = {
            "subject": email_subject,
            "is_html": is_html,
            "content": email_content,
            "no_of_attachments": no_of_attachments,
        }
        self.sms = {"content": sms_content}

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "channels": {"email": self.email, "sms": self.sms},
        }


# Example usage:
shipment_data = {
    "name": "CREATE SHIPMENT",
    "description": "This creates a shipment",
    "email_subject": "Shipment Successfully Booked",
    "is_html": True,
    "no_of_attachments": 2,
    "sms_content": "send this text to everyone",
}

shipment_data[
    "email_content"
] = """
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
