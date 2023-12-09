from jinja2 import Environment, BaseLoader, TemplateSyntaxError, Template
import re

# Your HTML template as a string
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Head content goes here -->
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
          <td>{{ order_id }}</td>
        </tr>
        <tr>
          <th>Shipping Date</th>
          <td>{{ shipping_date }}</td>
        </tr>
        <tr>
          <th>Estimated Delivery Date</th>
          <td>{{ estimated_delivery_date }}</td>
        </tr>
        <tr>
          <th>Tracking Number</th>
          <td class="tracking-number">{{ tracking_number }}</td>
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

# Example dynamic data
dynamic_data = {
    "customer_name": "John Doe",
    "order_id": "12345",
    "shipping_date": "2023-12-08",
    "estimated_delivery_date": "2023-12-15",
    "tracking_number": "ABC123456",
}

# Extract placeholders from the template using regular expressions
try:
    template_env = Environment(loader=BaseLoader())
    template = template_env.from_string(html_template)
    template.placeholders = set(re.findall(r"{{\s*(\w+)\s*}}", html_template))
except TemplateSyntaxError as e:
    print(f"Template syntax error: {e}")
    template.placeholders = set()

# Check if all required fields are present in dynamic_data
missing_fields = template.placeholders - set(dynamic_data.keys())

if missing_fields:
    print(f"Error: Missing fields in dynamic_data: {', '.join(missing_fields)}")
else:
    # Render the template with dynamic data
    rendered_template = template.render(dynamic_data)
    print(rendered_template)
