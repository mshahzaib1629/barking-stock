from jinja2 import Template

def _template():
    # Define your template
    email_template = """
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Stock Announcements</title>
                <style>
                    .announcement {
                        border-bottom: 1px solid #ddd;
                        padding: 10px 0;
                    }
                    .logo {
                        width: 50px;
                        height: auto;
                        vertical-align: middle;
                        margin-right: 10px;
                    }
                    .stock-name {
                        font-size: 16px;
                        vertical-align: middle;
                        font-weight: bold;
                    }
                    .details {
                        font-size: 14px;
                        margin: 5px 0;
                    }
                </style>
            </head>
            <body>
                <p>Dear {{ recipient_name }},</p>

                <p>We hope this email finds you well. Below is a list of the latest announcements for various stocks that may interest you. Each announcement includes the stock name, logo, symbol, title, and links to any relevant attachments.</p>

                <hr>

                {% for announcement in announcements %}
                <div class="announcement">
                    <img src="{{ announcement.logo_url }}" alt="{{ announcement.stock_name }} Logo" class="logo">
                    <span class="stock-name">{{ announcement.stock_name }} ({{ announcement.symbol }})</span>
                    <div class="details">
                        <p><strong>Announcement Title:</strong> {{ announcement.title }}</p>
                        <p><strong>Attachments:</strong> 
                            {% for link in announcement.attachment_links %}
                                <a href="{{ link.url }}" style="color: #1a73e8;">{{ link.name }}</a>{% if not loop.last %}, {% endif %}
                            {% endfor %}
                        </p>
                    </div>
                </div>
                {% endfor %}

                <p>Please let us know if you have any questions or need further information about any of these announcements. We are here to help!</p>

                <p>Best regards,<br>
                {{ sender_name }}<br>
                {{ sender_position }}<br>
                {{ sender_company }}</p>
            </body>
            </html>
    """

    return email_template

def stock_announcement_body(announcements):
    
    email_template = _template()
    # Create a Jinja2 template object
    template = Template(email_template)

    # Render the template with data
    rendered_email = template.render(announcements)
    return rendered_email