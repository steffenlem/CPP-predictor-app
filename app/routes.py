#!flask/bin/python
from app import app
from app.scripts.parse_uniprot import parse_uniprot
from app.scripts.forms import SequenceForm, UniprotForm, IGEMForm
from app.scripts.parse_igem_registry import get_registry_info
from app.scripts.predictor import predict_sequence
from flask import render_template, redirect, url_for, flash


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/fromsequence/', methods=['GET', 'POST'])
def fromsequence():
    form = SequenceForm()
    if form.validate_on_submit():
        flash('Activity of {} : {}'.format(
            form.sequence.data, predict_sequence(form.sequence.data)))
        return redirect(url_for('fromsequence'))
    return render_template('fromsequence.html', title='Prediction', form=form)


@app.route('/from_up/', methods=['GET', 'POST'])
def from_up():
    form = UniprotForm()
    if form.validate_on_submit():
        up_id = form.sequence.data
        unip_info = parse_uniprot(up_id)

        if unip_info.error:
            flash('Error: {}'.format(
                unip_info.error_type))
            flash('UniprotID :{}'.format(
                up_id))
            if unip_info.error_type == "sequence is too long":
                flash('Description: {}'.format(
                    unip_info.description))
            return redirect(url_for('from_up'))
        else:
            flash('UniprotID :{}'.format(
                up_id))
            flash('Description: {}'.format(
                unip_info.description))
            flash('AA sequence: {}'.format(
                unip_info.sequence))
            flash('Activity:{}'.format(
                predict_sequence(unip_info.sequence)))
            return redirect(url_for('from_igem'))

    return render_template('from_up.html', title='Prediction', form=form)


@app.route('/from_igem/', methods=['GET', 'POST'])
def from_igem():
    form = IGEMForm()
    if form.validate_on_submit():
        iGEM_id = form.sequence.data
        reg_info = get_registry_info(iGEM_id)

        if reg_info.error:
            flash('Error: {}'.format(
                reg_info.error_type))
            flash('RegistryID :{}'.format(
                iGEM_id))
            return redirect(url_for('from_igem'))
        else:
            flash('RegistryID :{}'.format(
                iGEM_id))
            flash('Description: {}'.format(
                reg_info.description))
            flash('AA sequence: {}'.format(
                reg_info.sequence))
            flash('Activity:{}'.format(
                predict_sequence(reg_info.sequence)))
            return redirect(url_for('from_igem'))
    return render_template('from_igem.html', title='Prediction', form=form)


if __name__ == '__main__':
    app.run(debug=True)
