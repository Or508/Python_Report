import argparse
import logging
import sys
from jinja2 import Template

# 1. Setup Logging
logging.basicConfig(
    filename='process.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def generate_html(name, date, salary, expenses, savings, savings_percentage):
    # HTML Template with Modern CSS
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Financial Report - {{ name }}</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            
            body { 
                font-family: 'Inter', sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0;
                padding: 20px;
                color: #333;
            }
            .card { 
                background: rgba(255, 255, 255, 0.95); 
                padding: 40px; 
                border-radius: 16px; 
                box-shadow: 0 10px 25px rgba(0,0,0,0.2); 
                max-width: 500px; 
                width: 100%;
                backdrop-filter: blur(10px);
            }
            h1 { 
                color: #1f2937; 
                margin-top: 0; 
                font-size: 24px;
                border-bottom: 2px solid #e5e7eb;
                padding-bottom: 15px;
                margin-bottom: 25px;
            }
            .stat-row { 
                display: flex; 
                justify-content: space-between; 
                margin-bottom: 15px; 
                font-size: 16px;
            }
            .label { color: #6b7280; font-weight: 600; }
            .value { font-weight: 600; color: #111827; }
            hr { border: 0; border-top: 1px solid #e5e7eb; margin: 20px 0; }
            .savings-section {
                background-color: #ecfdf5;
                padding: 15px;
                border-radius: 8px;
                border-left: 5px solid #10b981;
            }
            .savings-section .label { color: #065f46; }
            .savings-section .value { color: #059669; font-size: 1.1em; }
            .footer {
                margin-top: 25px;
                text-align: center;
                font-size: 12px;
                color: #9ca3af;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Financial Report</h1>
            
            <div class="stat-row">
                <span class="label">Name:</span>
                <span class="value">{{ name }}</span>
            </div>
            <div class="stat-row">
                <span class="label">Date:</span>
                <span class="value">{{ date }}</span>
            </div>
            
            <div class="stat-row">
                <span class="label">Income:</span>
                <span class="value">${{ "{:,.2f}".format(salary) }}</span>
            </div>
            <div class="stat-row">
                <span class="label">Expenses:</span>
                <span class="value">${{ "{:,.2f}".format(expenses) }}</span>
            </div>
            
            <hr>
            
            <div class="savings-section">
                <div class="stat-row">
                    <span class="label">Monthly Savings:</span>
                    <span class="value success">${{ "{:,.2f}".format(savings) }}</span>
                </div>
                 <div class="stat-row" style="margin-bottom: 0;">
                    <span class="label">Savings Percentage:</span>
                    <span class="value success">{{ "{:.1f}".format(savings_percentage) }}%</span>
                </div>
            </div>
            
            <div class="footer">
                Generated automatically via DevOps Pipeline
            </div>
        </div>
    </body>
    </html>
    """
    
    template = Template(html_template)
    html_content = template.render(
        name=name, 
        date=date, 
        salary=salary, 
        expenses=expenses, 
        savings=savings,
        savings_percentage=savings_percentage
    )
    
    output_file = "generated_report.html"
    with open(output_file, "w") as f:
        f.write(html_content)
    logging.info(f"HTML Report generated successfully at {output_file}.")
    print(f"HTML Report generated successfully: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a financial report.")
    parser.add_argument("--name", type=str, required=True, help="Name of the individual")
    parser.add_argument("--salary", type=float, required=True, help="Monthly salary")
    parser.add_argument("--expenses", type=float, required=True, help="Monthly expenses")
    parser.add_argument("--date", type=str, required=True, help="Date of the report (e.g., YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    logging.info(f"Starting process for user: {args.name}, date: {args.date}")
    
    try:
        if args.salary <= 0:
            raise ValueError("Salary must be a positive number.")
        if args.expenses < 0:
            raise ValueError("Expenses cannot be negative.")
            
        if args.salary < args.expenses:
            error_msg = f"Expenses (${args.expenses}) are higher than salary (${args.salary})!"
            logging.error(error_msg)
            raise ValueError(error_msg)
            
        savings = args.salary - args.expenses
        savings_percentage = (savings / args.salary) * 100
        
        logging.info(f"Calculation finished. Savings: {savings}, Percentage: {savings_percentage}%")
        
        generate_html(args.name, args.date, args.salary, args.expenses, savings, savings_percentage)
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)
