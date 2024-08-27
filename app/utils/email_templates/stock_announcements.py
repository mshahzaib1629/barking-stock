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
                    margin-right: 5px;
                    font-weight: bold;
                    font-size: 18px;
                }
                .stock-name {
                    margin-left: 5px;
                    font-size: 16px;
                    vertical-align: middle;
                    font-weight: bold;
                }
                .details {
                    font-size: 14px;
                    margin: 5px 0;
                }
                .datetime {
                    font-size: 12px;
                    color: #666;
                }
            </style>
        </head>
        <body>
            <p>Dear {{ recipient_name }},</p>

            <p>Please find the latest announcements from your favorite stocks below.</p>

            <hr>

            {% for announcement in announcements %}
            <div class="announcement">
                <span class="logo">{{ announcement.SYMBOL }}</span>
                &mdash;
                <span class="stock-name">{{ announcement.NAME }}</span>
                <div class="details">
                    <p><strong>Announcement Title:</strong> {{ announcement.TITLE }}</p>
                    <p><strong>Attachments:</strong> 
                        <a href="{{ announcement.VIEW }}" style="color: #1a73e8;">View</a>, 
                        <a href="{{ announcement.PDF }}" style="color: #1a73e8;">PDF</a>
                    </p>
                    <p class="datetime"><strong>Date and Time:</strong> {{ announcement.DATE }} at {{ announcement.TIME }}</p>
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