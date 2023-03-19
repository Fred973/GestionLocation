import datetime
from flask_login import login_required, current_user, login_user
from soft import app, db
from flask import render_template, session, redirect, request, url_for, flash, send_from_directory

from soft.constant import questions_path
from soft.func.pdf_func import create_questions_pdf
from soft.saab.questions.forms import QuestionsListForm
from soft.saab.questions.model import QuestionsList

@app.route('/SAAB/questions_list', methods=['GET', 'POST'])
@login_required
def questions_list():
    req_questions_list = QuestionsList.query.all()
    return render_template(
        'saab/questions_list/questions_list.html',
        questions=req_questions_list
    )

@app.route('/SAAB/add_questions_list', methods=['GET', 'POST'])
@login_required
def add_questions_list():
    form = QuestionsListForm()
    if request.method == 'POST':
        question_req = QuestionsList(
            name=current_user.name,
            creation_date=datetime.date.today(),
            question=form.question.data,
            answer=form.answer.data,
            remark=form.remark.data
        )
        db.session.add(question_req)
        db.session.commit()
        flash('The question is saved successfully !', category='success')
        return redirect(url_for('questions_list'))

    return render_template(
        'saab/questions_list/form_questions_list.html',
        title="Add question",
        form=form
    )

@app.route('/SAAB/edit_questions_list<int:id_question>', methods=['GET', 'POST'])
@login_required
def edit_questions_list(id_question):
    form = QuestionsListForm()
    question_to_edit = QuestionsList.query.get_or_404(id_question)

    if request.method == 'POST':
        question_to_edit.question = form.question.data
        question_to_edit.answer = form.answer.data
        question_to_edit.remark = form.remark.data
        db.session.commit()

        flash('The question was edited successfully !', category='success')
        return redirect(url_for('questions_list'))

    form.question.data = question_to_edit.question
    form.answer.data = question_to_edit.answer
    form.remark.data = question_to_edit.remark

    return render_template(
        'saab/questions_list/form_questions_list.html',
        title='Edit Question',
        form=form
    )

@app.route('/SAAB/delete_questions_list<int:id_to_delete>', methods=['GET', 'POST'])
@login_required
def delete_questions_list(id_to_delete):
    question_to_delete = QuestionsList.query.get_or_404(id_to_delete)
    db.session.delete(question_to_delete)
    db.session.commit()

    flash('The question was deleted successfully !', category='success')
    return redirect(request.referrer)

@app.route('/SAAB/download_questions', methods=['GET', 'POST'])
@login_required
def download():
    questions_req = QuestionsList.query.all()
    _questions_list = []
    counter = 1
    i_list = 0

    for i in questions_req:
        list_tmp = [counter, i.question, i.answer, i.remark]
        _questions_list.append(list_tmp)
        counter += 1
        i_list += 1

    filename = create_questions_pdf(_questions_list)
    return send_from_directory(
        questions_path,
        filename
    )