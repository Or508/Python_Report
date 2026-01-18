import argparse
import sys
from datetime import datetime

class FinancialReportGenerator:
    def __init__(self, name, income, expenses):
        self.name = name
        self.income = float(income)
        self.expenses = float(expenses)
        self.savings = 0.0
        self.savings_percentage = 0.0

    def calculate_metrics(self):
        """Calculates savings and percentage based on income and expenses."""
        self.savings = self.income - self.expenses
        
        if self.income <= 0:
            self.savings_percentage = 0.0
        else:
            self.savings_percentage = (self.savings / self.income) * 100

    def generate_html(self, output_file="report.html"):
        """Generates a professional HTML dashboard."""
        
        savings_color = "#28a745" if self.savings >= 0 else "#dc3545"
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Financial Report - {self.name}</title>
            <style>
                body {{ font-family: 'Segoe UI', sans-serif; background-color: #f4f6f9; display: flex; justify-content: center; padding: 20px; }}
                .container {{ background-color: #fff; width: 100%; max-width: 600px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); overflow: hidden; }}
                .header {{ background-color: #0056b3; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 30px; }}
                .metric-row {{ display: flex; justify-content: space-between; margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
                .highlight-box {{ background-color: #f8f9fa; border-radius: 8px; padding: 20px; text-align: center; margin-top: 20px; border: 1px solid #ddd; }}
                .savings-amount {{ font-size: 32px; color: {savings_color}; margin: 10px 0; }}
                .footer {{ text-align: center; padding: 15px; background-color: #f1f1f1; font-size: 12px; color: #777; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Financial Report</h1>
                    <p>Generated for: {self.name}</p>
                </div>
                <div class="content">
                    <div class="metric-row">
                        <span>Monthly Income:</span> <strong>${self.income:,.2f}</strong>
                    </div>
                    <div class="metric-row">
                        <span>Monthly Expenses:</span> <strong>${self.expenses:,.2f}</strong>
                    </div>
                    <div class="highlight-box">
                        <div>Net Savings</div>
                        <div class="savings-amount">${self.savings:,.2f}</div>
                        <div>Savings Rate: <strong>{self.savings_percentage:.1f}%</strong></div>
                    </div>
                </div>
                <div class="footer">Generated automatically by DevOps Pipeline | {current_date}</div>
            </div>
        </body>
        </html>
        """

        try:
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(html_content)
            print(f"SUCCESS: Report generated successfully at '{output_file}'")
        except Exception as e:
            print(f"ERROR: Failed to write HTML file. Reason: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--income", type=float, required=True)
    parser.add_argument("--expenses", type=float, required=True)
    args = parser.parse_args()

    report = FinancialReportGenerator(args.name, args.income, args.expenses)
    report.calculate_metrics()
    report.generate_html()

if __name__ == "__main__":
    main()