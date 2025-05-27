from flask import Flask, render_template, request, session, redirect
from llm import generate_explanation, generate_critique, rewrite_explanation

app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/reset', methods=['GET'])
def reset():
    session.clear()
    return redirect('/')

@app.route('/', methods=['GET', 'POST'])
def chat():
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        if 'clause' in request.form:
            clause = request.form['clause']
            initial = generate_explanation(clause)
            critique_output = generate_critique(clause, initial)

            # Parse critique and improved explanation from output
            critique_text = ""
            improved_text = ""

            improved_text = critique_output.strip()

            session['clause'] = clause
            session['initial'] = initial
            session['critique'] = critique_text
            session['final'] = improved_text
            session['history'] = [
                {"role": "user", "text": clause},
                {"role": "assistant", "text": f"Initial Explanation:\n{initial}"},
                # {"role": "assistant", "text": f"Critique:\n{critique_text}"},
                {"role": "assistant", "text": f"Self-Corrected Explanation:\n{improved_text}"}
            ]

        elif 'user_critique' in request.form and request.form['user_critique'].strip():
            user_critique = request.form['user_critique']
            revised = rewrite_explanation(session['clause'], session['final'], user_critique)
            session['final'] = revised
            session['history'].append({"role": "user", "text": f"Feedback:\n{user_critique}"})
            session['history'].append({"role": "assistant", "text": f"Revised Explanation:\n{revised}"})

    return render_template('chat.html', history=session.get('history', []), final=session.get('final'))

if __name__ == '__main__':
    app.run(debug=True)
