from jinja2 import Template, UndefinedError

# Your dynamic data
dynamic_data = {
    "name": "John",
    "age": 30,
    # "city": "Example City",
    # Add other dynamic keys as needed
}

# Your dynamic template (structure and keys are not predefined)
dynamic_template = (
    "Hello, my name is {{ name }} and I am {{ age }} years old. I live in {{ city }}."
)

# Create a Jinja2 template object
template = Template(dynamic_template)

try:
    # Render the template with the dynamic data
    rendered_text = template.render(dynamic_data)
    print(rendered_text)
except UndefinedError as e:
    # Handle the case where a dynamic key is missing
    print(f"Error: {e}")
