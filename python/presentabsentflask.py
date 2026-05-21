from flask import Flask, request, redirect, url_for, session
import webbrowser
import threading
import io
import base64
import random

# Import matplotlib and configure it to run safely on background threads
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = 'attendance_elegant_secret_key_789'

# Expanded elegant student roster (10 Students)
STUDENTS = [
    "Alexander Wright", "Beatrice Vance", "Charles Mercer", 
    "Diana Sterling", "Ethan Caldwell", "Fiona Gallagher", 
    "Gabriel Hayes", "Helena Rosier", "Ian Montgomery", "Julian Brooks"
]

# ---------------- INITIAL TRACKER / RESET ----------------
@app.route('/')
def index():
    # Initialize or reset the attendance tracking session variables
    session['current_index'] = 0
    session['present_students'] = []
    session['absent_students'] = []
    
    # Initialize a dummy 5-day history tracker if it doesn't exist
    # to simulate previous daily data calculations cleanly.
    if 'history_present' not in session:
        # Generates realistic random historical attendance rates for the past 4 days
        session['history_present'] = [random.randint(6, 9) for _ in range(4)]
        session['history_absent'] = [10 - x for x in session['history_present']]
        
    return redirect(url_for('mark_attendance'))

# ---------------- ATTENDANCE MARKING CARD ----------------
@app.route('/mark', methods=['GET', 'POST'])
def mark_attendance():
    if 'current_index' not in session:
        return redirect(url_for('index'))
        
    idx = session['current_index']
    
    # If all 10 students have been processed, save to history and head to report
    if idx >= len(STUDENTS):
        # Commit today's finalized metrics to historical logs before viewing
        today_p = len(session['present_students'])
        today_a = len(session['absent_students'])
        
        # Keep only the last 5 days of metrics active
        if len(session['history_present']) >= 5:
            session['history_present'].pop(0)
            session['history_absent'].pop(0)
            
        session['history_present'].append(today_p)
        session['history_absent'].append(today_a)
        session.modified = True
        
        return redirect(url_for('report'))

    current_student = STUDENTS[idx]

    if request.method == 'POST':
        status = request.form.get('status')
        
        if status == 'P':
            session['present_students'].append(current_student)
        else:
            session['absent_students'].append(current_student)
            
        session['current_index'] = idx + 1
        session.modified = True
        return redirect(url_for('mark_attendance'))

    return f'''
    <html>
    <head>
        <title>Mark Attendance</title>
        <style>
            body {{
                background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
                font-family: 'SF Pro Display', -apple-system, 'Segoe UI', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                color: #f8fafc;
            }}
            .tracker-card {{
                background: rgba(30, 41, 59, 0.45);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                padding: 45px 40px;
                border-radius: 28px;
                width: 420px;
                box-shadow: 0px 25px 50px -12px rgba(0, 0, 0, 0.5);
                text-align: center;
            }}
            .header-tag {{ 
                color: #94a3b8; 
                font-size: 12px; 
                text-transform: uppercase; 
                letter-spacing: 2px; 
                margin-bottom: 12px; 
                font-weight: 600;
            }}
            h1 {{ 
                color: #fff; 
                margin: 0 0 35px 0; 
                font-size: 28px; 
                font-weight: 700;
                letter-spacing: -0.5px;
            }}
            .student-display {{
                background: rgba(15, 23, 42, 0.6);
                padding: 28px;
                border-radius: 20px;
                font-size: 22px;
                font-weight: 600;
                color: #6366f1;
                margin-bottom: 35px;
                border: 1px solid rgba(255, 255, 255, 0.04);
                box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
            }}
            .btn-container {{ display: flex; gap: 16px; justify-content: center; }}
            button {{
                flex: 1; border: none; padding: 18px; border-radius: 14px;
                font-size: 15px; font-weight: 600; cursor: pointer; transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            button.present {{
                background: linear-gradient(135deg, #4f46e5, #3730a3); color: white;
                box-shadow: 0 4px 20px rgba(79, 70, 229, 0.3);
            }}
            button.present:hover {{ 
                transform: translateY(-2px); 
                box-shadow: 0 6px 24px rgba(79, 70, 229, 0.45);
                background: linear-gradient(135deg, #6366f1, #4f46e5);
            }}
            button.absent {{
                background: rgba(255, 255, 255, 0.03); color: #cbd5e1;
                border: 1px solid rgba(255, 255, 255, 0.12);
            }}
            button.absent:hover {{ 
                background: rgba(239, 68, 68, 0.12); 
                color: #f87171; 
                border-color: rgba(248, 113, 113, 0.4); 
                transform: translateY(-2px); 
            }}
            .progress-bar {{
                background: rgba(255, 255, 255, 0.06); height: 5px; width: 100%;
                border-radius: 10px; margin-top: 40px; overflow: hidden;
            }}
            .progress-fill {{ 
                background: linear-gradient(90deg, #6366f1, #a855f7); 
                height: 100%; 
                transition: width 0.4s ease; 
            }}
        </style>
    </head>
    <body>
        <div class="tracker-card">
            <div class="header-tag">Roster Roll Call — {idx + 1} of {len(STUDENTS)}</div>
            <h1>Daily Attendance</h1>
            
            <div class="student-display">{current_student}</div>
            
            <form method="post" class="btn-container">
                <button type="submit" name="status" value="A" class="absent">Mark Absent</button>
                <button type="submit" name="status" value="P" class="present">Mark Present</button>
            </form>
            
            <div class="progress-bar">
                <div class="progress-fill" style="width: {(idx / len(STUDENTS)) * 100}%"></div>
            </div>
        </div>
    </body>
    </html>
    '''

# ---------------- FINAL ANALYTICS REPORT ----------------
@app.route('/report')
def report():
    if 'present_students' not in session:
        return redirect(url_for('index'))

    p_list = session['present_students']
    a_list = session['absent_students']
    
    total_present = len(p_list)
    total_absent = len(a_list)
    total_students = len(STUDENTS)

    chart_html = ""
    try:
        # Generate elegant 2-column comparative analytics plots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2))
        fig.patch.set_facecolor('#1e1b4b') 
        
        # --- PLOT 1: Present vs Absent Donut ---
        ax1.set_facecolor('#0f172a')
        labels = ['Present', 'Absent']
        sizes = [total_present, total_absent]
        pastel_colors = ['#818cf8', '#f87171'] # Sleek Indigo / Coral-Red pastels
        
        wedges, texts, autotexts = ax1.pie(
            sizes, labels=labels, colors=pastel_colors, autopct='%1.0f%%',
            startangle=140, pctdistance=0.70,
            wedgeprops=dict(width=0.35, edgecolor='#1e1b4b', linewidth=3)
        )
        for t in texts: t.set_color('#94a3b8'); t.set_fontsize(10); t.set_fontweight('bold')
        for at in autotexts: at.set_color('#ffffff'); at.set_fontsize(10); at.set_fontweight('bold')
        ax1.set_title("Today's Distribution Ratio", color='#ffffff', fontsize=12, fontweight='bold', pad=12)

        # --- PLOT 2: Historical 5-Day Trend ---
        ax2.set_facecolor('#111827')
        days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Today']
        hist_p = session.get('history_present', [total_present])
        hist_a = session.get('history_absent', [total_absent])
        
        # Match array lengths seamlessly if restarted
        if len(hist_p) < 5:
            days = days[-len(hist_p):]

        ax2.bar(days, hist_p, label='Present', color='#818cf8', alpha=0.85, width=0.4)
        ax2.bar(days, hist_a, bottom=hist_p, label='Absent', color='#f87171', alpha=0.4, width=0.4)
        
        ax2.tick_params(colors='#94a3b8', labelsize=9)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['left'].set_color('#374151')
        ax2.spines['bottom'].set_color('#374151')
        ax2.grid(axis='y', color='#374151', linestyle=':', alpha=0.6)
        ax2.legend(facecolor='#1e1b4b', edgecolor='none', labelcolor='#cbd5e1', loc='upper left', fontsize=8)
        ax2.set_title("5-Day Historical Performance Log", color='#ffffff', fontsize=12, fontweight='bold', pad=12)

        plt.tight_layout()

        # Stream save
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=130, facecolor=fig.get_facecolor(), edgecolor='none')
        img_buffer.seek(0)
        
        encoded_chart = base64.b64encode(img_buffer.read()).decode('utf-8')
        chart_html = f'<img src="data:image/png;base64,{encoded_chart}" alt="Attendance Metrics Chart" style="max-width:100%; height:auto; border-radius:12px;">'
        plt.close()
    except Exception as e:
        chart_html = f"<p style='color:#f87171;'>Visualization module skipped or engine offline: {e}</p>"

    # Formatting structural list outputs
    p_rows = "".join([f"<li><span class='dot present'></span>{s}</li>" for s in p_list]) if p_list else "<li><em style='color:#64748b'>No entries found</em></li>"
    a_rows = "".join([f"<li><span class='dot absent'></span>{s}</li>" for s in a_list]) if a_list else "<li><em style='color:#64748b'>No entries found</em></li>"

    return f'''
    <html>
    <head>
        <title>Attendance Dashboard Summary</title>
        <style>
            body {{ font-family: 'SF Pro Display', -apple-system, sans-serif; background: #0f172a; color: #f8fafc; text-align: center; margin: 0; padding: 40px 20px; }}
            h1 {{ font-size: 30px; margin-bottom: 4px; font-weight: 700; letter-spacing: -0.5px; }}
            .subtitle {{ color: #64748b; font-size: 14px; margin-bottom: 35px; text-transform: uppercase; letter-spacing: 1.5px; }}
            
            .dashboard-grid {{
                display: flex; justify-content: center; gap: 24px; max-width: 1100px; margin: 0 auto; flex-wrap: wrap;
            }}
            .panel {{
                background: #1e1b4b; padding: 32px; border-radius: 24px;
                border: 1px solid rgba(255,255,255,0.04); box-shadow: 0 20px 40px rgba(0,0,0,0.25);
                flex: 1; min-width: 320px; text-align: left;
            }}
            .panel.chart {{ 
                text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; 
                flex: 1.6; min-width: 450px; background: #1e1b4b;
            }}
            
            .metrics-summary {{ display: flex; justify-content: space-between; margin-bottom: 30px; background: rgba(15,23,42,0.4); padding: 18px 22px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.02); }}
            .metric {{ text-align: center; }}
            .metric .num {{ font-size: 24px; font-weight: 700; font-family: system-ui, monospace; }}
            .metric .lbl {{ font-size: 11px; color: #94a3b8; text-transform: uppercase; margin-top: 5px; letter-spacing: 0.5px; }}
            
            h3 {{ margin: 0 0 16px 0; color: #fff; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 10px; }}
            ul {{ list-style: none; padding: 0; margin: 0 0 30px 0; }}
            li {{ 
                display: flex; align-items: center; padding: 10px 14px; background: rgba(255,255,255,0.02); 
                margin-bottom: 8px; border-radius: 10px; font-size: 14px; color: #e2e8f0; 
                border: 1px solid rgba(255,255,255,0.01);
            }}
            .dot {{ width: 8px; height: 8px; border-radius: 50%; margin-right: 12px; display: inline-block; }}
            .dot.present {{ background-color: #818cf8; box-shadow: 0 0 8px #818cf8; }}
            .dot.absent {{ background-color: #f87171; box-shadow: 0 0 8px #f87171; }}
            
            a {{ 
                display: inline-block; margin-top: 40px; background: linear-gradient(135deg, #4f46e5, #4338ca); 
                color: white; border: none; padding: 14px 35px; border-radius: 12px; font-size: 14px;
                font-weight: 600; text-decoration: none; transition: 0.25s ease; box-shadow: 0 4px 15px rgba(79, 70, 229, 0.2);
            }}
            a:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4); background: linear-gradient(135deg, #6366f1, #4f46e5); }}
        </style>
    </head>
    <body>
        <h1>Attendance Dashboard</h1>
        <div class="subtitle">Daily Registry & Cumulative Multi-Day Matrix</div>
        
        <div class="dashboard-grid">
            <!-- Numerical Panel -->
            <div class="panel">
                <div class="metrics-summary">
                    <div class="metric"><div class="num" style="color: #ffffff;">{total_students}</div><div class="lbl">Total Pool</div></div>
                    <div class="metric"><div class="num" style="color: #818cf8;">{total_present}</div><div class="lbl">Present</div></div>
                    <div class="metric"><div class="num" style="color: #f87171;">{total_absent}</div><div class="lbl">Absent</div></div>
                </div>
                
                <h3>Active Present Roll</h3>
                <ul>{p_rows}</ul>
                
                <h3>Active Absent Roll</h3>
                <ul>{a_rows}</ul>
            </div>
            
            <!-- Graphic Matplotlib Dual Panel Chart -->
            <div class="panel chart">
                {chart_html}
            </div>
        </div>
        
        <a href="/">🔄 Start New Roll Session</a>
    </body>
    </html>
    '''

# ---------------- AUTO OPEN BROWSER ----------------
def open_browser():
    webbrowser.open_new('http://127.0.0.1:9090')

if __name__ == '__main__':
    threading.Timer(1.2, open_browser).start()
    app.run(host='0.0.0.0', port=9090)
