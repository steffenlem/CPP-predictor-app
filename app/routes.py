#!flask/bin/python
from app import app
from app.scripts.parse_uniprot import parse_uniprot
from app.scripts.forms import SequenceForm, UniprotForm, IGEMForm
from app.scripts.parse_igem_registry import get_registry_info
from app.scripts.predictor import predict_sequence
from flask import render_template, redirect, url_for, flash
from c3pred.c3pred import *


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/fromsequence/', methods=['GET', 'POST'])
def fromsequence():
    form = SequenceForm()
    if form.validate_on_submit():
        results = predict_fasta(form.sequence.data)
        if results.error:
            flash('Error:\t' + results.error_type)
        else:
            flash('Sequence:\t' + results.sequence)
            flash('Activity:\t' + str(results.activity))
        return redirect(url_for('fromsequence'))
    return render_template('fromsequence.html', title='Prediction', form=form)


@app.route('/from_up/', methods=['GET', 'POST'])
def from_up():
    form = UniprotForm()
    if form.validate_on_submit():
        results = predict_uniprot(form.sequence.data)
        if results.error:
            flash('Error:\t' + results.error_type)
        else:
            flash('Description:\t' + results.description)
            flash('Sequence:\t' + results.sequence)
            flash('Activity:\t' + str(results.activity))
        return redirect(url_for('from_igem'))
    return render_template('from_up.html', title='Prediction', form=form)


@app.route('/from_igem/', methods=['GET', 'POST'])
def from_igem():
    form = IGEMForm()
    if form.validate_on_submit():
        results = predict_igem(form.sequence.data)
        if results.error:
            flash('Error:\t' + results.error_type)
        else:
            flash('Description:\t' + results.description)
            flash('Sequence:\t' + results.sequence)
            flash('Activity:\t' + str(results.activity))
        return redirect(url_for('from_igem'))
    return render_template('from_igem.html', title='Prediction', form=form)


if __name__ == '__main__':
    app.run(debug=True)
