from flask import Flask, render_template, request
import math

app = Flask(__name__)


def calculate_compound_interest(principal, rate, time, frequency):
    """
    Расчет сложного процента
    A = P * (1 + r/n)^(nt)
    где:
    P - начальная сумма (principal)
    r - годовая процентная ставка (rate / 100)
    n - частота начисления процентов в год (frequency)
    t - время в годах (time)
    A - итоговая сумма
    """
    if principal <= 0:
        return None, "Начальная сумма должна быть больше нуля"
    if rate < 0:
        return None, "Процентная ставка не может быть отрицательной"
    if time <= 0:
        return None, "Время должно быть больше нуля"
    if frequency <= 0:
        return None, "Частота начисления должна быть больше нуля"

    r = rate / 100
    n = frequency
    t = time

    amount = principal * math.pow((1 + r / n), n * t)
    interest = amount - principal

    return {
        'initial_amount': f"{principal:,.2f}".replace(",", "|").replace(".", ",").replace("|", "."),
        'final_amount': f"{amount:,.2f}".replace(",", "|").replace(".", ",").replace("|", "."),
        'interest_earned': f"{interest:,.2f}".replace(",", "|").replace(".", ",").replace("|", "."),
        'rate': rate,
        'time': time,
        'frequency': frequency
    }, None


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    result = None
    error = None

    if request.method == 'POST':
        try:
            principal = float(request.form.get('principal'))
            rate = float(request.form.get('rate'))
            time = float(request.form.get('time'))
            frequency = int(request.form.get('frequency'))

            result, error = calculate_compound_interest(principal, rate, time, frequency)

            if error:
                return render_template('index.html', error=error)

        except (ValueError, TypeError):
            error = "Пожалуйста, введите корректные числовые значения"
            return render_template('index.html', error=error)

    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
