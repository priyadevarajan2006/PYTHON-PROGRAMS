from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'elegant_snack_secret_key_999'

# Snack Menu Data
SNACKS = [
    {"id": 1, "name": "Chips", "price": 20, "icon": "🥔"},
    {"id": 2, "name": "Chocolate", "price": 50, "icon": "🍫"},
    {"id": 3, "name": "Juice", "price": 30, "icon": "🧃"},
    {"id": 4, "name": "Biscuit", "price": 10, "icon": "🍪"},
    {"id": 5, "name": "Sandwich", "price": 70, "icon": "🥪"}
]

@app.route('/')
def index():
    # Initialize an empty cart if it doesn't exist in the session
    if 'cart' not in session:
        session['cart'] = []
    
    # Calculate totals
    total_items = len(session['cart'])
    total_amount = sum(item['price'] for item in session['cart'])
    
    return render_template_string(HTML_TEMPLATE, snacks=SNACKS, cart=session['cart'], total_items=total_items, total_amount=total_amount)

@app.route('/add/<int:snack_id>', methods=['POST'])
def add_to_cart(snack_id):
    if 'cart' not in session:
        session['cart'] = []
        
    # Find the snack matching the ID
    snack = next((s for s in SNACKS if s['id'] == snack_id), None)
    if snack:
        session['cart'].append(snack)
        session.modified = True # Tell Flask the session array changed
        
    return redirect(url_for('index'))

@app.route('/clear', methods=['POST'])
def clear_cart():
    session['cart'] = []
    session.modified = True
    return redirect(url_for('index'))

@app.route('/checkout', methods=['POST'])
def checkout():
    action = request.form.get('action')
    if action == 'confirm':
        # Flash message or pass a status to the template
        session['cart'] = [] # Empty cart after success
        return render_template_string(STATUS_TEMPLATE, success=True)
    else:
        session['cart'] = []
        return render_template_string(STATUS_TEMPLATE, success=False)

# ----------------- UI TEMPLATES -----------------

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Snack Bar</title>
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            --card-bg: rgba(255, 255, 255, 0.85);
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --shadow-sm: 0 10px 30px -5px rgba(0, 0, 0, 0.05);
            --shadow-md: 0 20px 40px -15px rgba(0, 0, 0, 0.1);
        }

        body {
            font-family: 'SF Pro Display', -apple-system, 'Segoe UI', sans-serif;
            background: var(--bg-gradient);
            color: var(--text-main);
            margin: 0;
            padding: 40px 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1100px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 40px;
        }

        header h1 {
            font-size: 36px;
            font-weight: 800;
            margin: 0 0 8px 0;
            letter-spacing: -1px;
            background: linear-gradient(90deg, #4f46e5, #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        header p {
            color: var(--text-muted);
            margin: 0;
            font-size: 16px;
        }

        .main-layout {
            display: grid;
            grid-template-columns: 1.6fr 1fr;
            gap: 30px;
        }

        @media (max-width: 768px) {
            .main-layout { grid-template-columns: 1fr; }
        }

        /* Menu Panel */
        .menu-section h2, .cart-section h2 {
            font-size: 20px;
            font-weight: 700;
            margin-top: 0;
            margin-bottom: 20px;
            color: var(--text-main);
        }

        .menu-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
        }

        .snack-card {
            background: var(--card-bg);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            border-radius: 20px;
            padding: 24px;
            text-align: center;
            box-shadow: var(--shadow-sm);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .snack-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-md);
            border-color: rgba(99, 102, 241, 0.2);
        }

        .snack-icon {
            font-size: 40px;
            margin-bottom: 12px;
            display: block;
        }

        .snack-name {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 4px;
        }

        .snack-price {
            color: var(--text-muted);
            font-weight: 500;
            margin-bottom: 16px;
            font-size: 15px;
        }

        .btn-add {
            background: var(--primary);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 12px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: background 0.2s;
        }

        .btn-add:hover { background: var(--primary-hover); }

        /* Cart Panel */
        .cart-card {
            background: var(--card-bg);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            border-radius: 24px;
            padding: 30px;
            box-shadow: var(--shadow-md);
            position: sticky;
            top: 40px;
        }

        .cart-list {
            list-style: none;
            padding: 0;
            margin: 0 0 24px 0;
            max-height: 240px;
            overflow-y: auto;
        }

        .cart-item {
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #e2e8f0;
            font-size: 15px;
        }

        .cart-item:last-child { border-bottom: none; }

        .empty-text {
            color: var(--text-muted);
            font-style: italic;
            text-align: center;
            padding: 20px 0;
        }

        .summary-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-size: 14px;
            color: var(--text-muted);
        }

        .summary-row.total {
            border-top: 2px dashed #cbd5e1;
            padding-top: 16px;
            margin-top: 16px;
            font-size: 18px;
            font-weight: 700;
            color: var(--text-main);
        }

        .action-container {
            display: flex;
            gap: 12px;
            margin-top: 24px;
        }

        .btn-action {
            flex: 1;
            border: none;
            padding: 14px;
            border-radius: 14px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            text-align: center;
            text-decoration: none;
        }

        .btn-action.confirm {
            background: linear-gradient(135deg, #4f46e5, #3730a3);
            color: white;
            box-shadow: 0 4px 14px rgba(79, 70, 229, 0.25);
        }
        .btn-action.confirm:hover { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(79, 70, 229, 0.35); }
        .btn-action.confirm:disabled { background: #cbd5e1; color: #94a3b8; cursor: not-allowed; box-shadow: none; }

        .btn-action.cancel {
            background: #f1f5f9;
            color: #64748b;
            border: 1px solid #e2e8f0;
        }
        .btn-action.cancel:hover { background: #fee2e2; color: #ef4444; border-color: #fca5a5; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>The Snack Bar</h1>
            <p>Fresh bites delivered straight to your workstation</p>
        </header>

        <div class="main-layout">
            <!-- Left Side: Roster Grid Menu -->
            <div class="menu-section">
                <h2>Menu Items</h2>
                <div class="menu-grid">
                    {% for snack in snacks %}
                    <div class="snack-card">
                        <span class="snack-icon">{{ snack.icon }}</span>
                        <div class="snack-name">{{ snack.name }}</div>
                        <div class="snack-price">Rs. {{ snack.price }}</div>
                        <form action="/add/{{ snack.id }}" method="POST">
                            <button type="submit" class="btn-add">Add to Cart</button>
                        </form>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <!-- Right Side: Beautiful Invoice Basket Summary -->
            <div class="cart-section">
                <h2>Your Bill Matrix</h2>
                <div class="cart-card">
                    <ul class="cart-list">
                        {% for item in cart %}
                        <li class="cart-item">
                            <span>{{ item.icon }} {{ item.name }}</span>
                            <strong>Rs. {{ item.price }}</strong>
                        </li>
                        {% else %}
                        <li class="empty-text">Your cart is currently empty.</li>
                        {% endfor %}
                    </ul>

                    <div class="summary-row">
                        <span>Total Items Added:</span>
                        <strong>{{ total_items }}</strong>
                    </div>
                    <div class="summary-row total">
                        <span>Total Payable Amount:</span>
                        <span>Rs. {{ total_amount }}</span>
                    </div>

                    <div class="action-container">
                        <form action="/clear" method="POST" style="flex: 1;">
                            <button type="submit" class="btn-action cancel" {% if total_items == 0 %}disabled{% endif %}>Clear</button>
                        </form>
                        <form action="/checkout" method="POST" style="flex: 1.5;">
                            <button type="submit" name="action" value="confirm" class="btn-action confirm" {% if total_items == 0 %}disabled{% endif %}>Confirm Order</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

STATUS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Order Summary Status</title>
    <style>
        body {
            font-family: system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;
        }
        .status-card {
            background: white; padding: 40px; border-radius: 24px; box-shadow: 0 20px 40px rgba(0,0,0,0.06);
            text-align: center; max-width: 400px; width: 100%; border: 1px solid #e2e8f0;
        }
        .icon { font-size: 64px; margin-bottom: 16px; display: block; }
        h1 { margin: 0 0 10px 0; font-size: 24px; color: #0f172a; }
        p { color: #64748b; font-size: 15px; margin: 0 0 30px 0; line-height: 1.5; }
        .back-btn {
            background: #6366f1; color: white; border: none; padding: 12px 30px; 
            border-radius: 12px; font-weight: 600; text-decoration: none; display: inline-block;
            transition: background 0.2s;
        }
        .back-btn:hover { background: #4f46e5; }
    </style>
</head>
<body>
    <div class="status-card">
        {% if success %}
            <span class="icon">😋</span>
            <h1>Order Placed Successfully!</h1>
            <p>Your payment went through and your tracking details will update shortly. Enjoy your snack break!</p>
        {% else %}
            <span class="icon">❌</span>
            <h1>Order Cancelled</h1>
            <p>The selection instance has been removed and your tray was safely emptied.</p>
        {% endif %}
        <a href="/" class="back-btn">Go Back to Menu</a>
    </div>
</body>
</html>
'''
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9999, debug=True)
