from flask import Flask, render_template, request
from sympy import symbols, diff, simplify, sin, cos, tan, log, sqrt, exp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
import base64
from sympy import lambdify

x = symbols("x")
app = Flask(__name__)
transformations = standard_transformations + (implicit_multiplication_application,)

local_dict = {
    "x": x,
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "ln": log,
    "log": log,
    "sqrt": sqrt,
    "exp": exp
}
def make_plot(expr, result):
    try:
        f = lambdify(x, expr, "numpy")
        df = lambdify(x, result, "numpy")

        xs = np.linspace(-10, 10, 400)
        y1 = f(xs)
        y2 = df(xs)

        plt.figure(figsize=(7, 4))
        plt.axhline(0, linewidth=1)
        plt.axvline(0, linewidth=1)
        plt.grid(True)

        plt.plot(xs, y1, label="f(x)")
        plt.plot(xs, y2, label="f'(x)")

        plt.ylim(-20, 20)
        plt.legend()
        plt.title("График функции и производной")

        img = io.BytesIO()
        plt.savefig(img, format="png", bbox_inches="tight")
        img.seek(0)

        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()

        return plot_url

    except:
        return None

def page_start(title):
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{
            margin: 0;
            font-family: Arial, sans-serif;
            color: white;
            text-align: center;
            min-height: 100vh;
            overflow: auto;
            background: linear-gradient(135deg, #08001f, #24104f, #4b0b68, #ff4fd8);
            background-size: 300% 300%;
            animation: bgMove 10s ease infinite;
        }}

        @keyframes bgMove {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        .decor {{
            position: fixed;
            inset: 0;
            pointer-events: none;
            opacity: 0.22;
            font-size: 34px;
            z-index: 0;
        }}

        .decor span {{
            position: absolute;
            animation: float 6s ease-in-out infinite;
        }}

        @keyframes float {{
            0% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-18px); }}
            100% {{ transform: translateY(0); }}
        }}

        .content {{
            position: relative;
            z-index: 2;
            padding: 45px 20px;
        }}

        h1 {{
            font-size: 48px;
            text-shadow: 0 0 22px #ff9af0;
        }}

        .card {{
            background: rgba(255,255,255,0.13);
            border: 1px solid rgba(255,255,255,0.28);
            border-radius: 26px;
            padding: 28px;
            box-shadow: 0 0 22px rgba(255,79,216,0.25);
            transition: 0.3s;
        }}

        .card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 0 32px rgba(255,79,216,0.55);
        }}

        .btn {{
            padding: 14px 32px;
            font-size: 19px;
            border: none;
            border-radius: 16px;
            color: white;
            background: linear-gradient(90deg, #ff2ec4, #6c5cff);
            cursor: pointer;
        }}

        input {{
            padding: 17px;
            font-size: 21px;
            width: 420px;
            border: none;
            border-radius: 14px;
            outline: none;
        }}
    </style>
</head>

<body>
<div class="decor">
    <span style="top:10%; left:8%;">f'(x)</span>
    <span style="top:18%; left:82%;">∫</span>
    <span style="top:55%; left:8%;">π</span>
    <span style="top:75%; left:78%;">√x</span>
    <span style="top:38%; left:48%;">sin x</span>
</div>

<div class="content">
"""


def page_end():
    return """
</div>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/examples")
def examples():
    return page_start("Примеры производной") + """
<h1>Примеры нахождения производной</h1>
<p style="font-size:22px;">Формулы и правила дифференцирования</p>

<div class="card" style="max-width:900px; margin:35px auto;">
    <div style="display:flex; justify-content:center; gap:25px; flex-wrap:wrap;">

        <div style="background:white; color:#1d1230; padding:25px; border-radius:20px; width:330px;">
            <h2 style="color:#8a2be2;">Правила</h2>
            <p>(u ± v)' = u' ± v'</p>
            <p>(uv)' = u'v + uv'</p>
            <p>(u / v)' = (u'v − uv') / v²</p>
            <p>(f(g(x)))' = f'(g(x)) · g'(x)</p>
        </div>

        <div style="background:white; color:#1d1230; padding:25px; border-radius:20px; width:330px;">
            <h2 style="color:#8a2be2;">Формулы</h2>
            <p>(C)' = 0</p>
            <p>(xⁿ)' = nxⁿ⁻¹</p>
            <p>(sin x)' = cos x</p>
            <p>(cos x)' = −sin x</p>
            <p>(eˣ)' = eˣ</p>
            <p>(ln x)' = 1 / x</p>
        </div>

    </div>

    <h2 style="margin-top:30px;">Пример:</h2>
    <p style="font-size:34px;">f(x) = x² + 3x</p>
    <p style="font-size:28px;">↓</p>
    <p style="font-size:36px; color:#ff63b8; font-weight:bold;">f'(x) = 2x + 3</p>
</div>

<a href="/"><button class="btn">← Назад</button></a>
""" + page_end()


@app.route("/graph")
def graph():
    return page_start("Графики") + """
<h1>Графики функций</h1>
<p style="font-size:22px;">Графики построены автоматически по формулам</p>

<div style="display:flex; justify-content:center; gap:30px; flex-wrap:wrap; margin-top:35px;">

    <div class="card" style="width:330px;">
        <h2>f(x)=x²</h2>
        <canvas id="g1" width="280" height="220" style="background:white; border-radius:18px;"></canvas>
    </div>

    <div class="card" style="width:330px;">
        <h2>f(x)=sin(x)</h2>
        <canvas id="g2" width="280" height="220" style="background:white; border-radius:18px;"></canvas>
    </div>

    <div class="card" style="width:330px;">
        <h2>f(x)=√x</h2>
        <canvas id="g3" width="280" height="220" style="background:white; border-radius:18px;"></canvas>
    </div>

    <div class="card" style="width:330px;">
        <h2>f(x)=|x|</h2>
        <canvas id="g4" width="280" height="220" style="background:white; border-radius:18px;"></canvas>
    </div>

</div>

<br><br>
<a href="/"><button class="btn">← Назад</button></a>

<script>
function drawGraph(canvasId, func, xmin, xmax, ymin, ymax) {
    let canvas = document.getElementById(canvasId);
    let ctx = canvas.getContext("2d");
    let w = canvas.width;
    let h = canvas.height;

    ctx.clearRect(0, 0, w, h);

    function X(x) {
        return (x - xmin) / (xmax - xmin) * w;
    }

    function Y(y) {
        return h - (y - ymin) / (ymax - ymin) * h;
    }

    ctx.strokeStyle = "#dddddd";
    ctx.lineWidth = 1;

    for (let i = Math.ceil(xmin); i <= xmax; i++) {
        ctx.beginPath();
        ctx.moveTo(X(i), 0);
        ctx.lineTo(X(i), h);
        ctx.stroke();
    }

    for (let i = Math.ceil(ymin); i <= ymax; i++) {
        ctx.beginPath();
        ctx.moveTo(0, Y(i));
        ctx.lineTo(w, Y(i));
        ctx.stroke();
    }

    ctx.strokeStyle = "#333333";
    ctx.lineWidth = 2;

    ctx.beginPath();
    ctx.moveTo(X(xmin), Y(0));
    ctx.lineTo(X(xmax), Y(0));
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(X(0), Y(ymin));
    ctx.lineTo(X(0), Y(ymax));
    ctx.stroke();

    ctx.strokeStyle = "#ff2ec4";
    ctx.lineWidth = 4;
    ctx.beginPath();

    let started = false;

    for (let px = 0; px <= w; px++) {
        let x = xmin + (px / w) * (xmax - xmin);
        let y = func(x);

        if (!isFinite(y) || y < ymin || y > ymax) {
            started = false;
            continue;
        }

        let cy = Y(y);

        if (!started) {
            ctx.moveTo(px, cy);
            started = true;
        } else {
            ctx.lineTo(px, cy);
        }
    }

    ctx.stroke();
}

drawGraph("g1", x => x * x, -5, 5, -1, 10);
drawGraph("g2", x => Math.sin(x), -7, 7, -2, 2);
drawGraph("g3", x => x >= 0 ? Math.sqrt(x) : NaN, -1, 10, -1, 4);
drawGraph("g4", x => Math.abs(x), -5, 5, -1, 6);
</script>
""" + page_end()


@app.route("/test", methods=["GET", "POST"])
def test():
    steps = ""

    if request.method == "POST":
        func = request.form["func"]

        try:
            func_clean = func.replace("^", "**")

            expr = parse_expr(
                func_clean,
                local_dict=local_dict,
                transformations=transformations
            )

            result = simplify(diff(expr, x))
            pretty_result = str(result).replace("**", "^").replace("*", "")
            plot_url = make_plot(expr, result)

            steps = f"""
            <div class="card" style="background:white; color:#1d1230; max-width:650px; margin:35px auto;">
                <h2 style="color:#ff2ec4;">Пошаговое объяснение</h2>
                <p><b>1 шаг:</b> Дана функция:</p>
                <p style="color:#6c5cff; font-size:26px;">f(x) = {func}</p>
                <p><b>2 шаг:</b> Находим производную по переменной x.</p>
                <p><b>3 шаг:</b> Применяем правила дифференцирования.</p>
                <p><b>4 шаг:</b> Получаем ответ:</p>
                <p style="font-size:34px; color:#ff1493; font-weight:bold;">f'(x) = {pretty_result}</p>

<h2 style="color:#6c5cff;">График функции и производной</h2>
<img src="data:image/png;base64,{plot_url}" style="max-width:100%; border-radius:18px;">
            </div>
            """

        except Exception as e:
            steps = f"""
            <h2 style='color:red;'>Ошибка! Напиши пример правильно.</h2>
            <p>Например: x^2 + 3x, sin(x), ln(x), sqrt(x)</p>
            """

    return page_start("Решение производной") + f"""
<h1>Калькулятор производной</h1>
<p style="font-size:22px;">Введите функцию, сайт найдёт её производную</p>

<div class="card" style="max-width:650px; margin:35px auto;">
    <h2>Введите функцию</h2>

    <form method="POST">
        <input name="func" placeholder="Например: x^2 + 3x">
        <br><br>
        <button class="btn">Решить</button>
    </form>

    <p style="color:#ddd;">Пиши так: x^2, 3x, sin(x), cos(x), ln(x), sqrt(x)</p>
</div>

{steps}

<a href="/"><button class="btn">← Назад</button></a>
""" + page_end()

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    result = ""

    questions = [
        {
            "q": "1. Найдите производную f(x)=x²",
            "options": ["x", "2x", "x³", "2"],
            "answer": "2x"
        },
        {
            "q": "2. Найдите производную f(x)=3x",
            "options": ["3", "x", "3x²", "0"],
            "answer": "3"
        },
        {
            "q": "3. Производная постоянного числа равна:",
            "options": ["1", "x", "0", "числу"],
            "answer": "0"
        },
        {
            "q": "4. Найдите производную f(x)=sin(x)",
            "options": ["cos(x)", "-sin(x)", "tg(x)", "1/x"],
            "answer": "cos(x)"
        },
        {
            "q": "5. Найдите производную f(x)=cos(x)",
            "options": ["sin(x)", "-sin(x)", "cos(x)", "-cos(x)"],
            "answer": "-sin(x)"
        }
    ]

    if request.method == "POST":
        score = 0

        for i, question in enumerate(questions):
            user_answer = request.form.get(f"q{i}")
            if user_answer == question["answer"]:
                score += 1

        if score == 5:
            level = "Отличный результат ⭐"
        elif score >= 3:
            level = "Хороший результат 👍"
        else:
            level = "Нужно повторить тему 📘"

        result = f"""
        <div class="card" style="background:white; color:#1d1230; max-width:650px; margin:35px auto;">
            <h2 style="color:#ff2ec4;">Ваш результат</h2>
            <p style="font-size:34px; color:#6c5cff;"><b>{score} / 5</b></p>
            <p style="font-size:24px;">{level}</p>
        </div>
        """

    quiz_html = ""

    for i, question in enumerate(questions):
        quiz_html += f"""
        <div class="card" style="background:white; color:#1d1230; max-width:750px; margin:25px auto; text-align:left;">
            <h2 style="color:#8a2be2;">{question["q"]}</h2>
        """

        for option in question["options"]:
            quiz_html += f"""
            <label style="font-size:20px; display:block; margin:12px;">
                <input type="radio" name="q{i}" value="{option}" required style="width:auto;">
                {option}
            </label>
            """

        quiz_html += "</div>"

    return page_start("Мини-тест") + f"""
    <h1>Мини-тест по производным</h1>
    <p style="font-size:22px;">Ответьте на 5 вопросов</p>

    <form method="POST">
        {quiz_html}
        <br>
        <button class="btn">Проверить ответы</button>
    </form>

    {result}

    <br>
    <a href="/"><button class="btn">← Назад</button></a>
    """ + page_end()

if __name__ == "__main__":
    app.run()