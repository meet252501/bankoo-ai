
import json
import os
import glob
from datetime import datetime

class BrainDashboard:
    def __init__(self, trace_dir="logs/traces", output_file="logs/brain_dashboard.html"):
        self.trace_dir = trace_dir
        self.output_file = output_file
        if not os.path.exists(os.path.dirname(output_file)):
            os.makedirs(os.path.dirname(output_file))

    def generate_report(self):
        traces = []
        files = glob.glob(os.path.join(self.trace_dir, "*.jsonl"))
        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        traces.append(json.loads(line))
                    except:
                        continue
        
        if not traces:
            print("No traces found. Dashboard cannot be generated.")
            return

        # Sort by timestamp
        traces.sort(key=lambda x: x["timestamp"])

        # Simple aggregation
        total = len(traces)
        successes = sum(1 for t in traces if t.get("reward", 0) > 0)
        avg_latency = sum(t.get("metrics", {}).get("latency_sec", 0) for t in traces) / total
        
        # Prepare data for Chart.js
        labels = [datetime.fromisoformat(t["timestamp"]).strftime("%H:%M:%S") for t in traces][-20:] # Last 20
        rewards = [t.get("reward", 0) for t in traces][-20:]
        latencies = [t.get("metrics", {}).get("latency_sec", 0) for t in traces][-20:]

        # Extract Mistakes and Potential Fixes
        mistakes = [t for t in traces if t.get("reward", 0) < 0][-5:] # Last 5 mistakes
        correction_feed_html = ""
        
        for m in mistakes:
            user_input = m["messages"][1]["content"] if len(m["messages"]) > 1 else "Unknown"
            bad_response = m["messages"][2]["content"] if len(m["messages"]) > 2 else "Empty"
            
            # Look for a later successful interaction with same/similar input
            fix = next((t for t in traces if t.get("reward", 0) > 0 and t["timestamp"] > m["timestamp"] and t["messages"][1]["content"] == user_input), None)
            
            fix_html = f"""
            <div class="correction-card">
                <div class="mistake-header">❌ MISTAKE DETECTED</div>
                <div class="mistake-content">
                    <b>Input:</b> {user_input}<br>
                    <span style="color: #ef4444;"><b>Wrong Ans:</b> {bad_response}</span>
                </div>
            """
            
            if fix:
                good_response = fix["messages"][2]["content"]
                fix_html += f"""
                <div class="fix-header">✅ THE FIX (Learned)</div>
                <div class="fix-content" style="color: #10b981;">
                    <b>Optimized Ans:</b> {good_response}
                </div>
                """
            else:
                fix_html += f"""
                <div class="fix-header" style="background: rgba(251, 191, 36, 0.2); color: #fbbf24;">⏳ PENDING OPTIMIZATION</div>
                <div class="fix-content" style="color: #fbbf24; font-style: italic;">
                    Waiting for Agent-Lightning optimization cycle...
                </div>
                """
            
            fix_html += "</div>"
            correction_feed_html += fix_html

        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zenith Brain Growth Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;700&family=JetBrains+Mono&display=swap');
        
        body {{ 
            font-family: 'Outfit', sans-serif; 
            background: radial-gradient(circle at top right, #1e1b4b, #030712); 
            color: #f8fafc; 
            margin: 0; 
            padding: 40px; 
            overflow-x: hidden;
        }}
        
        .header {{ text-align: left; margin-bottom: 50px; border-left: 5px solid #38bdf8; padding-left: 20px; }}
        .header h1 {{ font-size: 2.5rem; margin: 0; letter-spacing: -1px; }}
        .header p {{ color: #94a3b8; margin-top: 5px; opacity: 0.8; }}
        
        .stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 40px; }}
        .stat-card {{ 
            background: rgba(30, 41, 59, 0.5); 
            backdrop-filter: blur(10px);
            padding: 30px; 
            border-radius: 20px; 
            border: 1px solid rgba(56, 189, 248, 0.2); 
            text-align: left;
            transition: 0.3s;
        }}
        .stat-card:hover {{ transform: translateY(-5px); border-color: #38bdf8; }}
        .stat-card h3 {{ margin: 0; color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; }}
        .stat-card p {{ margin: 15px 0 0; font-size: 2.2rem; font-weight: 700; color: #38bdf8; }}
        
        .grid-layout {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }}
        .section-box {{ 
            background: rgba(15, 23, 42, 0.8); 
            padding: 30px; 
            border-radius: 24px; 
            border: 1px solid rgba(255, 255, 255, 0.05); 
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        }}
        h2 {{ color: #e2e8f0; font-size: 1.2rem; margin-top: 0; margin-bottom: 25px; display: flex; align-items: center; gap: 10px; }}
        
        /* Correction Feed */
        .correction-feed {{ display: flex; flex-direction: column; gap: 20px; }}
        .correction-card {{ 
            background: rgba(255, 255, 255, 0.02); 
            border-radius: 16px; 
            overflow: hidden; 
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: 0.3s;
        }}
        .mistake-header {{ background: rgba(239, 68, 68, 0.15); color: #ef4444; padding: 8px 15px; font-size: 0.7rem; font-weight: 800; letter-spacing: 1px; }}
        .fix-header {{ background: rgba(16, 185, 129, 0.15); color: #10b981; padding: 8px 15px; font-size: 0.7rem; font-weight: 800; letter-spacing: 1px; }}
        .mistake-content, .fix-content {{ padding: 15px; font-size: 0.9rem; line-height: 1.5; font-family: 'Outfit', sans-serif; }}
        b {{ opacity: 0.7; font-weight: 400; }}
        
        canvas {{ width: 100% !important; height: 250px !important; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>ZENITH LABORATORY</h1>
        <p>Advanced AI Self-Correction & Intelligence Metrics</p>
    </div>

    <div class="stats">
        <div class="stat-card">
            <h3>Neural Connections</h3>
            <p>{total}</p>
        </div>
        <div class="stat-card">
            <h3>Accuracy Score</h3>
            <p>{round((successes/total)*100, 1)}%</p>
        </div>
        <div class="stat-card">
            <h3>Synaptic Speed</h3>
            <p>{round(avg_latency, 2)}s</p>
        </div>
    </div>

    <div class="grid-layout">
        <div class="section-box">
            <h2>📉 Performance Trend</h2>
            <canvas id="rewardChart"></canvas>
            <div style="margin-top: 30px;">
                <h2>⚡ Response Latency</h2>
                <canvas id="latencyChart"></canvas>
            </div>
        </div>
        
        <div class="section-box">
            <h2>🧪 Self-Correction Feed</h2>
            <div class="correction-feed">
                {correction_feed_html or '<div style="color: #64748b; text-align: center; padding: 40px;">No mistakes detected yet. Bankoo is performing flawlessly!</div>'}
            </div>
        </div>
    </div>

    <script>
        const labels = {json.dumps(labels)};
        
        new Chart(document.getElementById('rewardChart'), {{
            type: 'line',
            data: {{
                labels: labels,
                datasets: [{{
                    label: 'Intelligence Score',
                    data: {json.dumps(rewards)},
                    borderColor: '#38bdf8',
                    borderWidth: 3,
                    pointRadius: 4,
                    pointBackgroundColor: '#38bdf8',
                    backgroundColor: 'rgba(56, 189, 248, 0.1)',
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: {{ 
                responsive: true, 
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{ 
                    y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#64748b' }} }},
                    x: {{ grid: {{ display: false }}, ticks: {{ color: '#64748b' }} }}
                }} 
            }}
        }});

        new Chart(document.getElementById('latencyChart'), {{
            type: 'bar',
            data: {{
                labels: labels,
                datasets: [{{
                    label: 'Latency (ms)',
                    data: {json.dumps([l*1000 for l in latencies])},
                    backgroundColor: 'rgba(56, 189, 248, 0.3)',
                    borderRadius: 5
                }}]
            }},
            options: {{ 
                responsive: true, 
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{ 
                    y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#64748b' }} }},
                    x: {{ grid: {{ display: false }}, ticks: {{ color: '#64748b' }} }}
                }} 
            }}
        }});
    </script>
</body>
</html>
        """
        
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(html_template)
        
        print(f"✅ Dashboard generated: {os.path.abspath(self.output_file)}")

if __name__ == "__main__":
    db = BrainDashboard()
    db.generate_report()
