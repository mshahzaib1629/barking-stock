from jinja2 import Template

def get_email_body():
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

    # Sample data to populate the template
    data = {
         "recipient_name": "John Doe",
        "announcements": [
            {
                "stock_name": "Apple Inc.",
                "symbol": "AAPL",
                "logo_url": "https://pngimg.com/d/apple_logo_PNG19666.png",
                "title": "Q3 Earnings Report",
                "attachment_links": [
                    {"name": "Q3 Earnings Report PDF", "url": "https://example.com/aapl_q3_report.pdf"},
                    {"name": "Investor Presentation", "url": "https://example.com/aapl_investor_presentation.pdf"}
                ]
            },
            {
                "stock_name": "Tesla Inc.",
                "symbol": "TSLA",
                "logo_url": "https://pngimg.com/uploads/tesla_logo/tesla_logo_PNG19.png",
                "title": "New Model Launch Event",
                "attachment_links": [
                    {"name": "Event Details PDF", "url": "https://example.com/tsla_event_details.pdf"}
                ]
            },
            {
                "stock_name": "Amazon.com Inc.",
                "symbol": "AMZN",
                "logo_url": "https://pngimg.com/d/amazon_PNG15.png",
                "title": "Strategic Partnership Announcement",
                "attachment_links": [
                    {"name": "Partnership Details PDF", "url": "https://example.com/amzn_partnership.pdf"},
                    {"name": "Press Release", "url": "https://example.com/amzn_press_release.pdf"}
                ]
            },
            {
                "stock_name": "Microsoft Corp.",
                "symbol": "MSFT",
                "logo_url": "https://cdn-icons-png.flaticon.com/512/732/732221.png",
                "title": "Upcoming Product Updates",
                "attachment_links": [
                    {"name": "Product Roadmap PDF", "url": "https://example.com/msft_product_roadmap.pdf"}
                ]
            },
            {
                "stock_name": "Alphabet Inc.",
                "symbol": "GOOGL",
                "logo_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6HMrE7xvKu5-UahOPBs3GcE4AZJk8LsX7tg&s",
                "title": "Annual Shareholder Meeting Agenda",
                "attachment_links": [
                    {"name": "Agenda PDF", "url": "https://example.com/googl_agenda.pdf"},
                    {"name": "Meeting Details", "url": "https://example.com/googl_meeting_details.pdf"}
                ]
            },
        ],
        "sender_name": "Alice Smith",
        "sender_position": "Financial Analyst",
        "sender_company": "XYZ Investments"
    }

    # Create a Jinja2 template object
    template = Template(email_template)

    # Render the template with data
    rendered_email = template.render(data)
    return rendered_email
