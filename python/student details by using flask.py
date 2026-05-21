from flask import Flask, request, redirect, url_for, session
import webbrowser
import threading
import io
import base64

# Import matplotlib and configure it to run smoothly on background threads
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = 'student123'

# Core fixed subjects list
SUBJECTS = ['Tamil', 'English', 'Maths', 'Science', 'Social']

# Structure: { 'Student Name': { 'Tamil': 90, 'English': 85, ... } }
students = {}

# ---------------- LOGIN PAGE ----------------
@app.route('/', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin':
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid Username or Password'

    return f'''
    <html>
    <head>
        <title>Login</title>
        <style>
            body {{
                background: linear-gradient(135deg, #0f172a 0%, #2e1065 50%, #4c1d95 100%);
                font-family: 'Segoe UI', system-ui, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .box {{
                background: rgba(255, 255, 255, 0.06);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 40px;
                border-radius: 20px;
                width: 340px;
                box-shadow: 0px 20px 40px rgba(0,0,0,0.4);
                text-align: center;
            }}
            h1 {{ color: #f97316; margin-bottom: 25px; font-weight: 700; font-size: 28px; letter-spacing: -0.5px; }}
            input {{
                width: 100%;
                padding: 12px 16px;
                margin: 10px 0;
                border-radius: 10px;
                border: 1px solid rgba(255,255,255,0.1);
                background: rgba(15, 23, 42, 0.6);
                color: #fff;
                box-sizing: border-box;
                font-size: 15px;
            }}
            input::placeholder {{ color: #94a3b8; }}
            input:focus {{ outline: none; border-color: #f97316; }}
            button {{
                background: linear-gradient(90deg, #7c3aed, #6d28d9);
                color: white; border: none; width: 100%;
                padding: 14px; border-radius: 10px; cursor: pointer;
                font-size: 16px; font-weight: 600; margin-top: 15px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
            }}
            button:hover {{ background: linear-gradient(90deg, #6d28d9, #5b21b6); transform: translateY(-1px); }}
            p {{ color: #f87171; font-weight: 600; margin-top: 15px; }}
            .info {{ background: rgba(15, 23, 42, 0.4); padding: 12px; border-radius: 10px; margin-top: 20px; font-size: 13px; color: #cbd5e1; border: 1px solid rgba(255,255,255,0.05); }}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>Student Portal</h1>
            <form method="post">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Sign In</button>
            </form>
            {f'<p>⚠️ {error}</p>' if error else ''}
        </div>
    </body>
    </html>
    '''

# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    return '''
    <html>
    <head>
        <title>Dashboard</title>
        <style>
            body { 
                font-family: 'Segoe UI', system-ui, sans-serif; 
                background: #0f172a; 
                color: #f8fafc;
                margin: 0; 
                text-align: center; 
            }
            .container { margin-top: 100px; }
            h1 { color: #fff; margin-bottom: 10px; font-weight: 700; font-size: 32px; }
            .subtitle { color: #94a3b8; margin-bottom: 40px; font-size: 16px; }
            .menu-box {
                display: inline-block; 
                background: #1e1b4b; 
                padding: 40px;
                border-radius: 24px; 
                box-shadow: 0 20px 40px rgba(0,0,0,0.5);
                border: 1px solid rgba(255,255,255,0.05);
            }
            a {
                display: block; width: 300px; margin: 18px auto; padding: 16px;
                background: linear-gradient(135deg, #312e81 0%, #1e1b4b 100%);
                color: #f8fafc; text-decoration: none;
                border-radius: 12px; font-size: 16px; font-weight: 600; 
                transition: all 0.2s ease;
                border: 1px solid rgba(255,255,255,0.08);
            }
            a:hover { 
                background: linear-gradient(135deg, #4c1d95 0%, #3b0764 100%); 
                border-color: #f97316;
                transform: translateY(-2px); 
            }
            a.logout { 
                background: transparent;
                color: #94a3b8;
                border: 1px solid rgba(148, 163, 184, 0.3);
                margin-top: 30px;
            }
            a.logout:hover { background: rgba(220, 53, 69, 0.2); color: #f87171; border-color: #f87171; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="menu-box">
                <h1>Academic Management System</h1>
                <div class="subtitle">System Control Panel & Registry Gateway</div>
                <a href="/add">➕ Add Student Marks</a>
                <a href="/search">🔍 Search Student Summary</a>
                <a href="/students">📊 View Master Analytics Registry</a>
                <a href="/logout" class="logout">Logout Session</a>
            </div>
        </div>
    </body>
    </html>
    '''

# ---------------- ADD STUDENT ----------------
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if 'user' not in session:
        return redirect(url_for('login'))

    message = ''
    if request.method == 'POST':
        name = request.form['name'].strip()
        
        try:
            subject_marks = {}
            for sub in SUBJECTS:
                subject_marks[sub] = int(request.form[sub.lower()])
                
            students[name] = subject_marks
            message = f'✅ Academic records for "{name}" saved successfully!'
        except ValueError:
            message = '❌ Please enter valid numerical scores for all categories.'

    return f'''
    <html>
    <head>
        <title>Add Student Marks</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #f8fafc; text-align: center; }}
            .box {{
                background: #1e1b4b; width: 480px; margin: 50px auto; padding: 40px;
                border-radius: 20px; box-shadow: 0px 15px 30px rgba(0,0,0,0.4);
                border: 1px solid rgba(255,255,255,0.05);
            }}
            h1 {{ color: #fff; margin-bottom: 30px; font-size: 26px; }}
            input.stud-name {{ 
                width: 100%; padding: 12px 16px; margin-bottom: 25px; 
                border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); 
                background: #0f172a; color: #fff; font-size: 15px; box-sizing: border-box;
            }}
            input.stud-name:focus {{ outline: none; border-color: #f97316; }}
            .row {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }}
            label {{ font-weight: 600; color: #cbd5e1; width: 40%; text-align: left; padding-left: 5px; }}
            input.num {{ 
                width: 55%; padding: 10px 14px; border-radius: 8px; 
                border: 1px solid rgba(255,255,255,0.1); background: #0f172a; color: #fff; 
            }}
            input.num:focus {{ outline: none; border-color: #7c3aed; }}
            button {{
                background: linear-gradient(90deg, #f97316, #ea580c); color: white; border: none; padding: 14px;
                border-radius: 10px; font-size: 16px; cursor: pointer; font-weight: bold; margin-top: 20px; width: 100%;
                transition: 0.3s;
            }}
            button:hover {{ background: linear-gradient(90deg, #ea580c, #dd6b20); transform: translateY(-1px); }}
            a {{ display: inline-block; margin-top: 25px; color: #a78bfa; text-decoration: none; font-size: 14px; }}
            a:hover {{ color: #f97316; text-decoration: underline; }}
            h3 {{ color: #34d399; font-size: 15px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>Add Marks Entry</h1>
            <form method="post">
                <input type="text" name="name" class="stud-name" placeholder="Student Full Name" required>
                
                <div class="row"><label>Tamil</label><input type="number" name="tamil" class="num" min="0" max="100" required></div>
                <div class="row"><label>English</label><input type="number" name="english" class="num" min="0" max="100" required></div>
                <div class="row"><label>Maths</label><input type="number" name="maths" class="num" min="0" max="100" required></div>
                <div class="row"><label>Science</label><input type="number" name="science" class="num" min="0" max="100" required></div>
                <div class="row"><label>Social</label><input type="number" name="social" class="num" min="0" max="100" required></div>
                
                <button type="submit">Commit Record</button>
            </form>
            <h3>{message}</h3>
            <a href="/dashboard">← Back to Dashboard</a>
        </div>
    </body>
    </html>
    '''

# ---------------- SEARCH STUDENT ----------------
@app.route('/search', methods=['GET', 'POST'])
def search_student():
    if 'user' not in session:
        return redirect(url_for('login'))

    result = ''
    if request.method == 'POST':
        name = request.form['name'].strip()
        if name in students:
            sub_dict = students[name]
            marks = list(sub_dict.values())
            
            total = sum(marks)
            avg = total / len(marks)
            
            breakdown = "".join([f"<div style='margin: 8px 0; color:#cbd5e1;'><strong>{sub}:</strong> <span style='color:#f97316;'>{mk}</span></div>" for sub, mk in sub_dict.items()])
            
            result = f'''
            <div style="text-align: left; background: #0f172a; padding: 25px; border-radius: 12px; margin-top: 25px; border: 1px solid rgba(255,255,255,0.08);">
                <h3 style="margin-top:0; color:#fff; font-size: 18px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px;">Record: {name}</h3>
                {breakdown}
                <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.1); margin: 15px 0;">
                <div style="display:flex; justify-content:space-between; font-weight:600; color:#fff;">
                    <span>Total Score: <span style="color:#7c3aed;">{total}</span></span>
                    <span>Average: <span style="color:#7c3aed;">{avg:.2f}%</span></span>
                </div>
            </div>
            '''
        else:
            result = '<p style="color: #f87171; margin-top:20px; font-weight:600;">⚠️ Student Record Not Found</p>'

    return f'''
    <html>
    <head>
        <title>Search Student</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #f8fafc; text-align: center; }}
            .box {{
                background: #1e1b4b; width: 460px; margin: 80px auto; padding: 40px;
                border-radius: 20px; box-shadow: 0px 15px 30px rgba(0,0,0,0.4);
                border: 1px solid rgba(255,255,255,0.05);
            }}
            h1 {{ color: #fff; margin-bottom: 25px; font-size: 26px; }}
            input {{ 
                width: 100%; padding: 12px 16px; margin: 10px 0; border-radius: 8px; 
                border: 1px solid rgba(255,255,255,0.1); background: #0f172a; color: #fff; 
                box-sizing: border-box; font-size: 15px;
            }}
            input:focus {{ outline: none; border-color: #f97316; }}
            button {{
                background: linear-gradient(90deg, #7c3aed, #6d28d9); color: white; border: none; padding: 13px;
                border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; margin-top: 10px; transition: 0.3s;
            }}
            button:hover {{ background: linear-gradient(90deg, #6d28d9, #5b21b6); }}
            a {{ display: inline-block; margin-top: 25px; color: #a78bfa; text-decoration: none; font-size: 14px; }}
            a:hover {{ color: #f97316; }}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>Search Performance Profile</h1>
            <form method="post">
                <input type="text" name="name" placeholder="Enter Student Name" required>
                <button type="submit">Query Database</button>
            </form>
            {result}
            <br>
            <a href="/dashboard">← Back to Dashboard</a>
        </div>
    </body>
    </html>
    '''

# ---------------- SHOW ALL STUDENTS (LIGHT COLOURED CHART) ----------------
@app.route('/students')
def show_students():
    if 'user' not in session:
        return redirect(url_for('login'))

    table_rows = ''
    names_list = []
    averages_list = []

    for name, sub_dict in students.items():
        marks = list(sub_dict.values())
        total = sum(marks)
        avg = total / len(marks)
        
        names_list.append(name)
        averages_list.append(avg)
        
        table_rows += f'''
        <tr>
            <td class="student-name">{name}</td>
            <td class="metrics-value">{total}</td>
            <td class="metrics-value" style="color: #f97316; font-weight: 700;">{avg:.2f}%</td>
        </tr>
        '''

    chart_html = ""
    if names_list:
        try:
            plt.figure(figsize=(7.5, 4.2))
            plt.gcf().patch.set_facecolor('#1e1b4b')  
            ax = plt.gca()
            ax.set_facecolor('#0f172a')              
            
            # Light / pastel colors for the chart visual metrics
            light_colors = ['#a7f3d0', '#fef08a', '#c084fc', '#fed7aa', '#93c5fd', '#fca5a5']
            bar_colors = [light_colors[i % len(light_colors)] for i in range(len(names_list))]
            
            plt.bar(names_list, averages_list, color=bar_colors, edgecolor='#ffffff', linewidth=1, width=0.4)
            
            plt.title('Class Metrics - Comparative Performance', color='#ffffff', fontsize=13, fontweight='bold', pad=15)
            plt.xlabel('Student Profiles', color='#cbd5e1', fontsize=10, fontweight='bold')
            plt.ylabel('Grade Averages (%)', color='#cbd5e1', fontsize=10, fontweight='bold')
            
            ax.tick_params(colors='#94a3b8', labelsize=9)
            ax.spines['bottom'].set_color('rgba(255,255,255,0.1)')
            ax.spines['left'].set_color('rgba(255,255,255,0.1)')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            plt.ylim(0, 105)
            plt.grid(axis='y', linestyle=':', color='rgba(255,255,255,0.05)')
            plt.tight_layout()

            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=110, facecolor=plt.gcf().get_facecolor(), edgecolor='none')
            img_buffer.seek(0)
            
            encoded_chart = base64.b64encode(img_buffer.read()).decode('utf-8')
            chart_html = f'''
            <div class="chart-container">
                <h3>Visual Analytics Matrix</h3>
                <img src="data:image/png;base64,{encoded_chart}" alt="Performance Chart Matrix Mapping">
            </div>
            '''
            plt.close()
        except Exception as e:
            chart_html = f"<p style='color:#f87171;'>Failed to map visualization: {e}</p>"

    return f'''
    <html>
    <head>
        <title>Academic Registry</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #f8fafc; text-align: center; margin: 0; padding: 40px 20px; }}
            h1 {{ font-size: 28px; margin-bottom: 5px; font-weight: 700; }}
            .subtitle {{ color: #94a3b8; font-size: 14px; margin-bottom: 30px; }}
            table {{
                margin: 0 auto 40px auto; width: 65%; border-collapse: collapse;
                background: #1e1b4b; box-shadow: 0 15px 30px rgba(0,0,0,0.3); border-radius: 12px; overflow: hidden;
                border: 1px solid rgba(255,255,255,0.05);
            }}
            th, td {{ padding: 16px 20px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.05); }}
            th {{ background: #2e1065; color: #f8fafc; font-weight: 600; text-transform: uppercase; font-size: 12px; letter-spacing: 1px; }}
            tr:hover {{ background-color: rgba(255,255,255,0.02); }}
            .student-name {{ font-weight: 600; text-align: left; padding-left: 40px; color: #fff; }}
            .metrics-value {{ font-family: monospace; font-size: 15px; color: #cbd5e1; }}
            .chart-container {{
                background: #1e1b4b; display: inline-block; margin-top: 10px; padding: 25px;
                border-radius: 16px; box-shadow: 0 15px 30px rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.05);
            }}
            .chart-container h3 {{ margin-top: 0; color: #cbd5e1; font-size: 16px; margin-bottom: 15px; }}
            a {{ display: inline-block; margin-top: 30px; color: #a78bfa; text-decoration: none; font-weight: 600; font-size: 15px; }}
            a:hover {{ color: #f97316; }}
        </style>
    </head>
    <body>
        <h1>Master Performance Registry</h1>
        <div class="subtitle">Global Student Database Grade Summary Matrix</div>
        <table>
            <tr>
                <th style="width: 50%; text-align: left; padding-left: 40px;">Student Name</th>
                <th style="width: 25%;">Total Cumulative Score</th>
                <th style="width: 25%;">Grade Average Percentage</th>
            </tr>
            {table_rows if table_rows else '<tr><td colspan="3" style="color: #94a3b8; padding: 30px;">No operational records exist inside active cache memory logs. Add profiles to generate statistical views.</td></tr>'}
        </table>

        {chart_html}
        <br>
        <a href="/dashboard">← Back to Dashboard Control Center</a>
    </body>
    </html>
    '''

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# ---------------- AUTO OPEN BROWSER ----------------
def open_browser():
    webbrowser.open_new('http://127.0.0.1:9090')

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    # Host changed to 0.0.0.0 to allow shared accessibility on external host infrastructures
    app.run(host='0.0.0.0', port=9090)
