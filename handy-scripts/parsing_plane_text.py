from jinja2 import Environment, meta

# Your Jinja template
template_string = """
Hello {{ recipient_name }},

This is a sample email template using Jinja for dynamic content. You can include plain text content here and customize it according to your needs.

Here are some dynamic details:
- Email Address: {{ recipient_email }}
- Account Balance: ${{ account_balance }}

Feel free to add more paragraphs, bullet points, or any other plain text elements.

Best regards,
Your Name
"""

# Create a Jinja environment
env = Environment()

# Parse the template to extract variable names
parsed_content = env.parse(template_string)
template_variables = meta.find_undeclared_variables(parsed_content)

# Your dynamic data
data = {
    "recipient_name": "John Doe",
    "recipient_email": "john.doe@example.com",
    # "account_balance": 5000
}

# Find missing keys
missing_keys = [variable for variable in template_variables if variable not in data]

# Print missing keys
if missing_keys:
    print(f"Missing keys in dynamic data: {', '.join(missing_keys)}")
else:
    print("All keys in the template are provided in the dynamic data.")
