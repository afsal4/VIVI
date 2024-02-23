from django.shortcuts import render, redirect
from django.contrib import messages
from sklearn import base

from cs50 import SQL
from .score import Score
from .qna import Q_and_A


QNA = None
CANDIDATE_NAME = None
CANDIDATE_ID = None
COMPANY_ID = None
JOB_DESC = ""


# database
db = SQL("sqlite:////home/afsal/Desktop/Github/ml_frontend/home/database.db")


# company page [description and all]
def company(request):
    context = {"variable1": "this is send", "variable2": "new one"}

    return render(request, "index.html", context)


# post method for company
def company_post(request):
    id = None
    if request.method == "POST":
        company_name = request.POST.get("name")
        email = request.POST.get("email")
        job_description = request.POST.get("subject")

        db.execute(
            "INSERT INTO company(company_name, email_id, job_description) VALUES (?, ?, ?)",
            company_name,
            email,
            job_description,
        )

        answer = db.execute(
            "SELECT id from company where company_name = ? and email_id = ?",
            company_name,
            email,
        )
        id = answer[0]["id"]

        # messages.success(request, "Your Message Has Been Sent!")
    return render(request, "company.html", {"c_id": id})


# # candidate page
def candidate(request, id=None):
    print(id, "\n\n\n\n")
    company_id = id
    if request.method == "POST":
        company_id = request.POST["id"]
        candidate_name = request.POST["name"]
        email_id = request.POST["email"]

        db.execute(
            "INSERT INTO candidate(candidate_name, email, company_id) VALUES (?, ?, ?)",
            candidate_name,
            email_id,
            company_id,
        )

        job_description = db.execute(
            "SELECT job_description from company where id = ?", company_id
        )
        candidate_id = db.execute(
            "SELECT id from candidate where company_id = ? and candidate_name = ? and email = ?",
            company_id,
            candidate_name,
            email_id,
        )

        print(candidate_id, job_description, int(company_id))

        qna = Q_and_A(job_description)

        global QNA, COMPANY_ID, CANDIDATE_ID, JOB_DESC, CANDIDATE_NAME

        CANDIDATE_NAME = candidate_name
        QNA = qna
        COMPANY_ID = int(company_id)
        CANDIDATE_ID = candidate_id[0]["id"]
        JOB_DESC = job_description[0]["job_description"]
        return redirect("interview_page")

    # Initialize empty form

    success_message = request.session.get("success_message")
    # if success_message:
    #     del request.session['success_message']  # Remove the success message from session after displaying it

    context = {"success_message": success_message, "id": company_id}
    return render(request, "candidate.html", context)


def home(request):
    return render(request, "home1.html")


# def interview_candidates(request):
#     candidates = Cadidate.objects.all()
#     return render(request, 'candidate_details.html', {'candidates': candidates})


def interview_page(request):
    return render(request, "interview_page.html")


def about(request):
    return render(request, "about.html")


def stop(request):
    # get the scores from the data base
    company_id = COMPANY_ID
    candidate_id = CANDIDATE_ID
    candidate_name = CANDIDATE_NAME
    candidate_id = CANDIDATE_ID

    # consist of job desc, questions answers, companyid

    job_description = JOB_DESC

    print(
        "\n\n\n\n----------------------",
        QNA,
        COMPANY_ID,
        CANDIDATE_ID,
        JOB_DESC,
        CANDIDATE_NAME,
        "------------------------\n\n\n\n\n",
    )

    # calculate the total scores
    QNA.question_answer_score(data, job_description)

    scores_data = QNA.qna_data

    for row in scores_data:
        db.execute(
            "INSERT INTO qna(candidate_name, question, answer, company_id, candidate_id, score) values (?, ?, ?, ?, ?, ?) ",
            candidate_name,
            row["question"],
            row["answer"],
            company_id,
            candidate_id,
            row["q_a_score"],
        )
        
    company_interview_result = db.execute('select job_description, qna.candidate_name, email, score from qna join candidate on candidate.id = qna.candidate_id join company on company.id = qna.company_id where company.id = ?', COMPANY_ID)
    print(company_interview_result, '---------------------------\n\n\n\n\n')
    context = {'context': company_interview_result}
        
        

    return render(request, "company_interview_score.html", context)



# ---------------------------------------------------

# def start_recording(job_description):
#     qna = Q_and_A(job_description)

PLAY = False
data = []
answers = []


def play_button(request, value):
    global QNA, data
    company_id = COMPANY_ID
    candidate_id = CANDIDATE_ID
    job_description = JOB_DESC

    # ask question
    if value == 1:
        _, question = QNA.ask_quesiton()

    # repeat question
    if value == 2:
        _, question = QNA.ask_quesiton(repeat=1)

    answer = QNA.speak_answer()

    # save questions and answers
    data.append({"question": question, "answer": answer})

    print(question, answer)

    return redirect("interview_page")


def score(request):
    # company_interview_result = db.execute('select job_description, candidate_name, email, score from qna join candidate on candidate.id = qna.candidate_id join company on company.id = qna.company_id where company_id = ?', COMPANY_ID)

    # data = {'data': company_interview_result}

    data = [
        {
            "candidate_name": "John Doe",
            "job_description": "Software Developer",
            "email": "john.doe@example.com",
            "score": 85,
            "view_url": "/viewmore/1",  # assuming you need to pass an ID to the viewmore URL
        },
        {
            "candidate_name": "Jane Smith",
            "job_description": "Data Scientist",
            "email": "jane.smith@example.com",
            "score": 92,
            "view_url": "/viewmore/2",
        },
        # Add more entries as needed
    ]

    data = {"data": data}

    return render(request, "company_interview_score.html", data)
