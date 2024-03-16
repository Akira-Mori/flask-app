from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTMLのテンプレート
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>料金シミュレーション</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 8px;
            border: 1px solid #dddddd;
            text-align: left;
        }
        .text-right {
            text-align: right;
        }
    </style>
</head>
<body>
    <h1>料金シミュレーション</h1>
    <form method="post">
        <table>
            <tr>
                <td>売上高</td>
                <td>
                    <select name="sales" id="sales">
                        <option value="0" {% if sales == 0 %}selected{% endif %}>3000万円未満</option>
                        <option value="30000000" {% if sales == 30000000 %}selected{% endif %}>3000万円以上5000万円未満</option>
                        <option value="50000000" {% if sales == 50000000 %}selected{% endif %}>5000万円以上10000万円未満</option>
                        <option value="100000000" {% if sales == 100000000 %}selected{% endif %}>10000万円以上30000万円未満</option>
                        <option value="300000000" {% if sales == 300000000 %}selected{% endif %}>30000万円以上50000万円未満</option>
                    </select>
                </td>
            </tr>
            <tr>
                <td>訪問頻度</td>
                <td>
                    <select name="frequency" id="frequency">
                        <option value="quarterly" {% if frequency == 'quarterly' %}selected{% endif %}>3か月ごと</option>
                        <option value="monthly" {% if frequency == 'monthly' %}selected{% endif %}>毎月</option>
                    </select>
                </td>
            </tr>
            <tr>
                <td>消費税申告</td>
                <td><input type="checkbox" id="tax_filing" name="tax_filing" {% if tax_filing %}checked{% endif %}></td>
            </tr>
            <tr>
                <td>月仕訳数</td>
                <td><input type="number" id="entries" name="entries" required value="{{ entries }}"></td>
            </tr>
        </table>
        <input type="submit" value="計算する">
    </form>
    {% if results is not none %}
        <h2>計算結果</h2>
        <table>
            <tr>
                <th>項目</th>
                <th class="text-right">月額料金</th>
                <th class="text-right">年間金額</th>
            </tr>
            <tr>
                <td>顧問料</td>
                <td class="text-right">{{ '{:,.0f}'.format(results['advisor_monthly']) }}円</td>
                <td class="text-right">{{ '{:,.0f}'.format(results['advisor_annual']) }}円</td>
            </tr>
            <tr>
                <td>記帳代行料</td>
                <td class="text-right">{{ '{:,.0f}'.format(results['bookkeeping_monthly']) }}円</td>
                <td class="text-right">{{ '{:,.0f}'.format(results['bookkeeping_annual']) }}円</td>
            </tr>
            <tr>
                <td>決算料</td>
                <td>-</td>
                <td class="text-right">{{ '{:,.0f}'.format(results['settlement_annual']) }}円</td>
            </tr>
            <tr>
                <td>合計</td>
                <td class="text-right">{{ '{:,.0f}'.format(results['total_monthly']) }}円</td>
                <td class="text-right">{{ '{:,.0f}'.format(results['total_annual']) }}円</td>
            </tr>
        </table>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def simulate_pricing():
    results = None
    sales = 0
    frequency = 'quarterly'
    tax_filing = False
    entries = 0

    if request.method == 'POST':
        sales = int(request.form['sales'])
        frequency = request.form['frequency']
        tax_filing = 'tax_filing' in request.form
        entries = int(request.form['entries'])

        advisor_monthly = get_advisor_fee(sales, frequency)
        bookkeeping_monthly = 7500 * (1 + (entries - 1) // 100)
        corporate_tax_annual = advisor_monthly * 5
        consumption_tax_annual = advisor_monthly if tax_filing else 0
        settlement_annual = corporate_tax_annual + consumption_tax_annual

        total_monthly = advisor_monthly + bookkeeping_monthly
        total_annual = (advisor_monthly * 12) + bookkeeping_monthly * 12 + settlement_annual

        results = {
            'advisor_monthly': advisor_monthly,
            'advisor_annual': advisor_monthly * 12,
            'bookkeeping_monthly': bookkeeping_monthly,
            'bookkeeping_annual': bookkeeping_monthly * 12,
            'settlement_annual': settlement_annual,
            'total_monthly': total_monthly,
            'total_annual': total_annual,
        }

    return render_template_string(HTML_TEMPLATE, results=results, sales=sales, frequency=frequency, tax_filing=tax_filing, entries=entries)

def get_advisor_fee(sales, frequency):
    if sales == 0:
        return 23000 if frequency == 'quarterly' else 29000
    elif sales == 30000000:
        return 25000 if frequency == 'quarterly' else 32000
    elif sales == 50000000:
        return 30000 if frequency == 'quarterly' else 38000
    elif sales == 100000000:
        return 35000 if frequency == 'quarterly' else 44000
    else:  # 30000万円以上50000万円未満
        return 43000 if frequency == 'quarterly' else 54000

if __name__ == '__main__':
    app.run(debug=True)