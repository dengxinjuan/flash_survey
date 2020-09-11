from flask import Flask
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey 

app = Flask(__name__)

app.debug = True

app.config['SECRET_KEY'] = 'iamthesecretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

#I dont understand this response_key, why not responses=[]
RESPONSES_KEY = "responses"


@app.route('/')
def home():
    title = satisfaction_survey.title
    instruction=satisfaction_survey.instructions
    session[RESPONSES_KEY] = []
    return render_template('start.html',title=title,instruction=instruction)

@app.route('/begin',methods=["POST"])
def changetoquestions():
    return redirect("/questions/0")



@app.route('/questions/<int:question_id>')
def show_question(question_id):
    """show question with given questionid"""
    questions=satisfaction_survey.questions
    q=questions[question_id].question
    choices=questions[question_id].choices


    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # trying to access question page too soon
        flash("You didnt answer the question!")
        return redirect("/")

    if (len(responses) == len(questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != question_id):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {question_id}.")
        return redirect(f"/questions/{len(responses)}")




    return render_template('question.html',q=q,choices=choices)


@app.route('/answer',methods=["POST"])
def answer_question():
    answer=request.form["answer"]

    #I dont understand this session
    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses
    # why session[respon>key]??

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/complete')
def complete_survey():
    return render_template('complete.html')

