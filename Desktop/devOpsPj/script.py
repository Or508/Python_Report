#!/usr/bin/env python3
"""
Simple chat session report generator
Generates log.txt and result.html based on manually entered data
"""

import sys
import argparse
from datetime import datetime


def validate_inputs(user_messages, ai_responses, validation_errors, cta_left, session_time):
    """
    Validate all input parameters
    Returns (is_valid, error_message)
    """
    # Check all numbers are integers (not floats)
    if not isinstance(user_messages, int):
        return False, "user_messages must be an integer"
    
    if not isinstance(ai_responses, int):
        return False, "ai_responses must be an integer"
    
    if not isinstance(validation_errors, int):
        return False, "validation_errors must be an integer"
    
    if not isinstance(session_time, int):
        return False, "session_time must be an integer"
    
    # Check all numbers are >= 0
    if user_messages < 0:
        return False, "user_messages must be >= 0"
    
    if ai_responses < 0:
        return False, "ai_responses must be >= 0"
    
    if validation_errors < 0:
        return False, "validation_errors must be >= 0"
    
    # Check reasonable maximum values (prevent unrealistic inputs)
    MAX_REASONABLE = 1000000  # 1 million
    if user_messages > MAX_REASONABLE:
        return False, f"user_messages must be <= {MAX_REASONABLE}"
    
    if ai_responses > MAX_REASONABLE:
        return False, f"ai_responses must be <= {MAX_REASONABLE}"
    
    if validation_errors > MAX_REASONABLE:
        return False, f"validation_errors must be <= {MAX_REASONABLE}"
    
    if session_time > MAX_REASONABLE:
        return False, f"session_time must be <= {MAX_REASONABLE}"
    
    # Check ai_responses <= user_messages
    if ai_responses > user_messages:
        return False, "ai_responses must be <= user_messages"
    
    # Check validation_errors <= user_messages (logical constraint)
    if validation_errors > user_messages:
        return False, "validation_errors must be <= user_messages"
    
    # Check session_time > 0
    if session_time <= 0:
        return False, "session_time must be > 0"
    
    # Check cta_left is boolean
    if cta_left not in [True, False]:
        return False, "cta_left must be true or false"
    
    return True, ""


def calculate_error_rate(validation_errors, user_messages):
    """
    Calculate error rate as a ratio of validation errors to user messages.
    
    Args:
        validation_errors: Number of validation errors
        user_messages: Total number of user messages
        
    Returns:
        float: Error rate (0.0 to 1.0)
    """
    if user_messages == 0:
        return 0.0
    return validation_errors / user_messages


def determine_status(error_rate, cta_left):
    """
    Determine session status based on error rate and CTA completion.
    
    Args:
        error_rate: Calculated error rate
        cta_left: Boolean indicating if CTA was left
        
    Returns:
        str: Status string (e.g., "OK", "OK (CTA left)", "Problematic")
    """
    if error_rate > 0.3:
        status = "Problematic"
    else:
        status = "OK"
    
    # Add CTA note if applicable
    if cta_left:
        status += " (CTA left)"
    
    return status


def create_log_file(user_messages, ai_responses, validation_errors, cta_left, 
                    session_time, error_rate, status):
    """
    Create log.txt file with all session data and calculations.
    
    Args:
        user_messages: Number of user messages
        ai_responses: Number of AI responses
        validation_errors: Number of validation errors
        cta_left: Boolean indicating if CTA was left
        session_time: Session time in minutes
        error_rate: Calculated error rate
        status: Session status string
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_content = f"""Chat Session Report
Generated: {timestamp}

Input Values:
- User Messages: {user_messages}
- AI Responses: {ai_responses}
- Validation Errors: {validation_errors}
- CTA Left: {cta_left}
- Session Time: {session_time} minutes

Calculations:
- Error Rate: {error_rate:.2%} ({validation_errors}/{user_messages})

Final Status: {status}
"""
    
    with open("log.txt", "w", encoding="utf-8") as f:
        f.write(log_content)


def create_html_file(user_messages, ai_responses, validation_errors, cta_left,
                     session_time, error_rate, status):
    """
    Create result.html file with professional dashboard design.
    Generates a styled HTML report with KPI cards, status banner, and details table.
    All styling is inline CSS to work with Jenkins CSP restrictions.
    
    Args:
        user_messages: Number of user messages
        ai_responses: Number of AI responses
        validation_errors: Number of validation errors
        cta_left: Boolean indicating if CTA was left
        session_time: Session time in minutes
        error_rate: Calculated error rate
        status: Session status string
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Determine status color based on status type
    status_color = "#e74c3c" if "Problematic" in status else "#2ecc71"
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Session Execution Report</title>
    <style>
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes slideUp {{
            from {{ opacity: 0; transform: translateY(40px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes shine {{
            0% {{ background-position: -200% center; }}
            100% {{ background-position: 200% center; }}
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #0f0f1a;
            color: #e0e0e0;
            line-height: 1.6;
            padding: 2rem;
            min-height: 100vh;
            margin: 0;
            overflow-x: hidden;
        }}
        
        .container {{
            max-width: 1100px;
            margin: 0 auto;
            animation: fadeIn 0.8s ease-out forwards;
        }}
        
        .status-banner {{
            background: linear-gradient(90deg, #2ecc71, #27ae60);
            color: #ffffff;
            padding: 0.8rem 2rem;
            text-align: center;
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: 2rem;
            border-radius: 50px;
            box-shadow: 0 4px 15px rgba(46, 204, 113, 0.2);
            display: inline-block;
            position: relative;
            left: 50%;
            transform: translateX(-50%);
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 4rem;
            padding: 3rem;
            background: linear-gradient(135deg, #6b21a8, #4c1d95, #7e22ce);
            background-size: 200% auto;
            border-radius: 24px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }}

        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 50%;
            height: 100%;
            background: linear-gradient(
                to right,
                transparent,
                rgba(255, 255, 255, 0.1),
                transparent
            );
            transform: skewX(-25deg);
            animation: shine 4s infinite;
        }}
        
        .header h1 {{
            font-size: 3rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 1rem;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
            letter-spacing: -1px;
        }}
        
        .header p {{
            color: rgba(255, 255, 255, 0.8);
            font-size: 1.1rem;
            font-weight: 500;
        }}
        
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 4rem;
        }}
        
        .kpi-card {{
            background: rgba(42, 42, 58, 0.5);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2.5rem;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            animation: slideUp 0.6s ease-out both;
        }}

        .kpi-card:nth-child(1) {{ animation-delay: 0.2s; }}
        .kpi-card:nth-child(2) {{ animation-delay: 0.3s; }}
        .kpi-card:nth-child(3) {{ animation-delay: 0.4s; }}
        
        .kpi-card:hover {{
            transform: translateY(-10px) scale(1.02);
            border-color: rgba(255, 255, 255, 0.1);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
            background: rgba(42, 42, 58, 0.8);
        }}
        
        .kpi-card.user-messages {{
            border-top: 5px solid #3b82f6;
        }}
        
        .kpi-card.ai-responses {{
            border-top: 5px solid #a855f7;
        }}
        
        .kpi-card.validation-errors {{
            border-top: 5px solid #f97316;
        }}
        
        .kpi-card h3 {{
            font-size: 0.85rem;
            font-weight: 600;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 1.5rem;
        }}
        
        .kpi-card .value {{
            font-size: 3.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            background: linear-gradient(to bottom, #fff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .kpi-card.user-messages .value {{
            background: linear-gradient(135deg, #60a5fa, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .kpi-card.ai-responses .value {{
            background: linear-gradient(135deg, #c084fc, #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .kpi-card.validation-errors .value {{
            background: linear-gradient(135deg, #fb923c, #f97316);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .kpi-card .description {{
            color: #64748b;
            font-size: 0.9rem;
            font-weight: 500;
        }}
        
        .details-section {{
            background: rgba(42, 42, 58, 0.3);
            border-radius: 24px;
            padding: 3rem;
            margin-bottom: 4rem;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }}
        
        .details-section h2 {{
            font-size: 1.8rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .details-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
        }}
        
        .details-table th {{
            color: #94a3b8;
            font-weight: 600;
            padding: 1.2rem 1.5rem;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .details-table td {{
            padding: 1.2rem 1.5rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            color: #cbd5e1;
            font-size: 1rem;
        }}
        
        .details-table tbody tr:hover td {{
            background-color: rgba(255, 255, 255, 0.02);
            color: #fff;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 0.4rem 1.2rem;
            border-radius: 100px;
            font-weight: 700;
            font-size: 0.85rem;
            background-color: {status_color};
            color: #ffffff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            text-transform: uppercase;
        }}
        
        .jenkins-banner {{
            text-align: center;
            padding: 2rem;
            color: #475569;
            font-size: 0.9rem;
            font-weight: 500;
        }}
        
        @media (max-width: 768px) {{
            body {{ padding: 1rem; }}
            .header {{ padding: 2rem; }}
            .header h1 {{ font-size: 2rem; }}
            .kpi-grid {{ grid-template-columns: 1fr; }}
            .details-section {{ padding: 1.5rem; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="status-banner">
            ✓ Build Verified by Jenkins
        </div>
        
        <div class="header">
            <h1>Chat Analytics</h1>
            <p>Report Generated: {timestamp}</p>
        </div>
        
        <div class="kpi-grid">
            <div class="kpi-card user-messages">
                <h3>User Messages</h3>
                <div class="value">{user_messages}</div>
                <p class="description">Active engagement metrics</p>
            </div>
            
            <div class="kpi-card ai-responses">
                <h3>AI Responses</h3>
                <div class="value">{ai_responses}</div>
                <p class="description">Automated intelligence flow</p>
            </div>
            
            <div class="kpi-card validation-errors">
                <h3>Validation Errors</h3>
                <div class="value">{validation_errors}</div>
                <p class="description">System integrity checks</p>
            </div>
        </div>
        
        <div class="details-section">
            <h2>Session Intelligence</h2>
            <table class="details-table">
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th>Analysis</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Total Conversations</strong></td>
                        <td>{user_messages} manual messages</td>
                    </tr>
                    <tr>
                        <td><strong>AI Participation</strong></td>
                        <td>{ai_responses} generated replies</td>
                    </tr>
                    <tr>
                        <td><strong>System Validation</strong></td>
                        <td>{validation_errors} exceptions caught</td>
                    </tr>
                    <tr>
                        <td><strong>Call to Action</strong></td>
                        <td>{'Completed' if not cta_left else 'Pending Action'}</td>
                    </tr>
                    <tr>
                        <td><strong>Interaction Time</strong></td>
                        <td>{session_time} minutes active</td>
                    </tr>
                    <tr>
                        <td><strong>Performance Ratio</strong></td>
                        <td>{error_rate:.2%} error rate</td>
                    </tr>
                    <tr>
                        <td><strong>Final Health Score</strong></td>
                        <td><span class="status-badge">{status}</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
    
        <div class="jenkins-banner">
            Securely processed on Jenkins Build Node
        </div>
    </div>
</body>
</html>
"""
    
    with open("result.html", "w", encoding="utf-8") as f:
        f.write(html_content)


def main():
    """
    Main function - parse arguments, validate, calculate, generate reports
    """
    parser = argparse.ArgumentParser(description="Generate chat session report")
    parser.add_argument("--user_messages", type=int, required=True,
                       help="Number of messages sent by user")
    parser.add_argument("--ai_responses", type=int, required=True,
                       help="Number of AI responses in chatbot")
    parser.add_argument("--validation_errors", type=int, required=True,
                       help="Number of validation errors in session")
    parser.add_argument("--cta_left", type=str, required=True,
                       choices=["true", "false"],
                       help="Whether user left details in CTA message (true/false)")
    parser.add_argument("--session_time", type=int, required=True,
                       help="Session time in minutes")
    
    args = parser.parse_args()
    
    # Convert cta_left string to boolean
    cta_left_bool = args.cta_left.lower() == "true"
    
    # Validate inputs
    is_valid, error_msg = validate_inputs(
        args.user_messages,
        args.ai_responses,
        args.validation_errors,
        cta_left_bool,
        args.session_time
    )
    
    if not is_valid:
        print(f"ERROR: {error_msg}", file=sys.stderr)
        sys.exit(1)
    
    # Calculate error rate
    error_rate = calculate_error_rate(args.validation_errors, args.user_messages)
    
    # Determine status
    status = determine_status(error_rate, cta_left_bool)
    
    # Generate log.txt
    create_log_file(
        args.user_messages,
        args.ai_responses,
        args.validation_errors,
        cta_left_bool,
        args.session_time,
        error_rate,
        status
    )
    
    # Generate result.html
    create_html_file(
        args.user_messages,
        args.ai_responses,
        args.validation_errors,
        cta_left_bool,
        args.session_time,
        error_rate,
        status
    )
    
    print("Report generated successfully:")
    print("  - log.txt")
    print("  - result.html")


if __name__ == "__main__":
    main()
