import java.io.FileWriter;
import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Main {
    public static void main(String[] args) {
        // ערכי ברירת מחדל
        int userMessages = 0;
        int aiResponses = 0;
        int validationErrors = 0;
        boolean ctaLeft = false;
        int sessionTime = 0;

        // קריאת הפרמטרים מהשורת פקודה (כמו שעשינו בפייתון)
        for (int i = 0; i < args.length; i++) {
            switch (args[i]) {
                case "--user_messages":
                    userMessages = Integer.parseInt(args[++i]);
                    break;
                case "--ai_responses":
                    aiResponses = Integer.parseInt(args[++i]);
                    break;
                case "--validation_errors":
                    validationErrors = Integer.parseInt(args[++i]);
                    break;
                case "--cta_left":
                    ctaLeft = Boolean.parseBoolean(args[++i]);
                    break;
                case "--session_time":
                    sessionTime = Integer.parseInt(args[++i]);
                    break;
            }
        }

        // יצירת ה-HTML
        String htmlContent = generateHtml(userMessages, aiResponses, validationErrors, ctaLeft, sessionTime);

        // שמירת הקובץ
        try (FileWriter writer = new FileWriter("result.html")) {
            writer.write(htmlContent);
            System.out.println("Report generated successfully: result.html");
        } catch (IOException e) {
            System.err.println("Error writing to file: " + e.getMessage());
        }
    }

    private static String generateHtml(int userMessages, int aiResponses, int validationErrors, boolean ctaLeft,
            int sessionTime) {
        String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));

        // כאן נכנס ה-CSS המושקע עם הסגול והאנימציות
        return "<!DOCTYPE html>\n" +
                "<html lang='en'>\n" +
                "<head>\n" +
                "    <meta charset='UTF-8'>\n" +
                "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n" +
                "    <title>Java Execution Report</title>\n" +
                "    <style>\n" +
                "        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #1a1a2e; color: #e0e0e0; margin: 0; padding: 20px; }\n"
                +
                "        .container { max-width: 900px; margin: 0 auto; background-color: #16213e; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); opacity: 0; animation: fadeIn 1.5s forwards; }\n"
                +
                "        \n" +
                "        .header { text-align: center; margin-bottom: 40px; position: relative; }\n" +
                "        h1 { font-size: 3em; margin: 0; background: linear-gradient(90deg, #ff00cc, #333399, #ff00cc); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: shine 3s linear infinite; }\n"
                +
                "        \n" +
                "        .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 40px; }\n"
                +
                "        .kpi-card { background-color: #0f3460; padding: 20px; border-radius: 10px; text-align: center; transition: transform 0.3s, box-shadow 0.3s; border: 1px solid rgba(255,255,255,0.1); opacity: 0; animation: slideUp 0.8s forwards; }\n"
                +
                "        .kpi-card:hover { transform: translateY(-10px) scale(1.02); box-shadow: 0 15px 30px rgba(0,0,0,0.4); }\n"
                +
                "        .kpi-value { font-size: 3em; font-weight: bold; margin: 10px 0; }\n" +
                "        .kpi-label { font-size: 1.1em; color: #a0a0a0; text-transform: uppercase; letter-spacing: 1px; }\n"
                +
                "        \n" +
                "        /* Specific Colors */\n" +
                "        .card-blue { border-bottom: 4px solid #00d4ff; } .card-blue .kpi-value { color: #00d4ff; }\n" +
                "        .card-purple { border-bottom: 4px solid #bf00ff; } .card-purple .kpi-value { color: #bf00ff; }\n"
                +
                "        .card-red { border-bottom: 4px solid #ff4d4d; } .card-red .kpi-value { color: #ff4d4d; }\n" +
                "        \n" +
                "        .status-section { background-color: #0f3460; padding: 20px; border-radius: 10px; border-left: 5px solid #00ff88; }\n"
                +
                "        .timestamp { color: #00ff88; font-family: monospace; font-size: 1.2em; }\n" +
                "        \n" +
                "        /* Animations */\n" +
                "        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }\n" +
                "        @keyframes slideUp { from { transform: translateY(50px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }\n"
                +
                "        @keyframes shine { to { background-position: 200% center; } }\n" +
                "        .kpi-card:nth-child(1) { animation-delay: 0.2s; }\n" +
                "        .kpi-card:nth-child(2) { animation-delay: 0.4s; }\n" +
                "        .kpi-card:nth-child(3) { animation-delay: 0.6s; }\n" +
                "    </style>\n" +
                "</head>\n" +
                "<body>\n" +
                "    <div class='container'>\n" +
                "        <div class='header'>\n" +
                "            <h1>JAVA AUTOMATION REPORT</h1>\n" +
                "            <p>Generated by Jenkins Slave (Linux)</p>\n" +
                "        </div>\n" +
                "\n" +
                "        <div class='kpi-grid'>\n" +
                "            <div class='kpi-card card-blue'>\n" +
                "                <div class='kpi-value'>" + userMessages + "</div>\n" +
                "                <div class='kpi-label'>User Messages</div>\n" +
                "            </div>\n" +
                "            <div class='kpi-card card-purple'>\n" +
                "                <div class='kpi-value'>" + aiResponses + "</div>\n" +
                "                <div class='kpi-label'>AI Responses</div>\n" +
                "            </div>\n" +
                "            <div class='kpi-card card-red'>\n" +
                "                <div class='kpi-value'>" + validationErrors + "</div>\n" +
                "                <div class='kpi-label'>Errors</div>\n" +
                "            </div>\n" +
                "        </div>\n" +
                "\n" +
                "        <div class='status-section'>\n" +
                "            <h3>System Status</h3>\n" +
                "            <p>Execution Time: <span class='timestamp'>" + timestamp + "</span></p>\n" +
                "            <p>Session Duration: " + sessionTime + " minutes</p>\n" +
                "            <p>CTA Clicked: " + (ctaLeft ? "Yes" : "No") + "</p>\n" +
                "        </div>\n" +
                "    </div>\n" +
                "</body>\n" +
                "</html>";
    }
}