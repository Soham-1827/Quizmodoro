
from flask import Flask, render_template, request, redirect, url_for, session
import os
from file_processing import extract_text
from quiz_generation import generate_questions
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.before_request
def check_for_redirect():
    if request.endpoint == 'results' and 'questions' not in session:
        return redirect(url_for('pomodoro_timer'))

@app.route('/')
@app.route('/pomodoro', methods=['GET', 'POST'])
def pomodoro_timer():
    session.clear()  # Clear the session data when accessing the home page
    if request.method == 'POST':
        session['duration'] = int(request.form['duration']) * 60
        return redirect(url_for('upload'))
    return render_template('pomodoro_timer.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        file = secure_filename(f.filename)
        f.save(file)
        if file == '':
            return "No file selected"
        text = extract_text(file)
        if text is None:
            return "Error extracting text from file"
        questions = generate_questions(text)
        session['questions'] = [(q.prompt, q.options, q.answer) for q in questions]
        session['current_question'] = 0
        session['responses'] = []
        session['feedback'] = []
        return redirect(url_for('quiz'))
    return render_template('upload.html')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        selected_option = request.form.get('option')
        current_question_index = session.get('current_question', 0)
        questions = session.get('questions', [])
        correct_answer = questions[current_question_index][2]

        session['responses'].append(selected_option)
        feedback = "Correct" if int(
            selected_option) == correct_answer else f"Incorrect. The correct answer is:- {questions[current_question_index][1][correct_answer]}"
        session['feedback'].append(feedback)

        session['current_question'] += 1

    current_question_index = session.get('current_question', 0)
    questions = session.get('questions', [])

    if current_question_index >= len(questions):
        return redirect(url_for('results'))

    question = questions[current_question_index]
    feedback = session['feedback'][current_question_index - 1] if current_question_index > 0 else ""
    return render_template('quiz.html', question=question, index=current_question_index, total=len(questions),
                           feedback=feedback)


@app.route('/results')
def results():
    questions = session.get('questions', [])
    responses = session.get('responses', [])
    score = sum(1 for i in range(len(questions)) if int(responses[i]) == questions[i][2])
    return render_template('results.html', score=score, total=len(questions))


if __name__ == '__main__':
    app.run(debug=True)