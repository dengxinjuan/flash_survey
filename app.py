from flask import Flask
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey,surveys,personality_quiz


app = Flask(__name__)

app.debug = True

app.config['SECRET_KEY'] = 'iamthesecretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

#I dont understand this response_key, why not responses=[]
RESPONSES_KEY = "responses"
CURRENT_SURVEY_KEY = 'current_survey'


@app.route('/')
def home():
    
    return render_template('base.html')


@app.route('/',methods=["POST"])
def changetoquestions():
    session[RESPONSES_KEY] = []
    return redirect("/choose")


@app.route("/choose")
def choose():
    return render_template('choose.html',surveys=surveys)


@app.route("/choose",methods=["POST"])
def pick_survey():
    survey_id = request.form['survey_code']
    survey = surveys[survey_id]
    session[CURRENT_SURVEY_KEY] = survey_id
    return render_template('start.html',survey=survey)

@app.route("/begin",methods=['POST'])
def start():
    session[RESPONSES_KEY] = []

    return redirect("/questions/0")



@app.route('/questions/<int:question_id>')
def show_question(question_id):
    """show question with given questionid"""
    responses = session.get(RESPONSES_KEY)
    survey_code = session[CURRENT_SURVEY_KEY]
    survey = surveys[survey_code]

    questions = survey.questions
    q=questions[question_id].question
    choices=questions[question_id].choices
    t = questions[question_id].allow_text


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

    return render_template('question.html',q=q,choices=choices,t=t)


@app.route('/answer',methods=["POST"])
def answer_question():
    answer=request.form["answer"]
    text=request.form.get('text',"")

    #I dont understand this session
    responses = session[RESPONSES_KEY]
    responses.append({"choice": answer, "text": text})
    session[RESPONSES_KEY] = responses
    # why session[respon>key]??

    session[RESPONSES_KEY] = responses
    survey_code = session[CURRENT_SURVEY_KEY]
    survey = surveys[survey_code]

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/complete')
def complete_survey():
    survey_id = session[CURRENT_SURVEY_KEY]
    survey = surveys[survey_id]
    responses = session[RESPONSES_KEY]
    return render_template('complete.html',survey=survey,responses=responses)

