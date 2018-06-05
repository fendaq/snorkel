from flask import current_app, Blueprint, Flask, flash, redirect, render_template, request, session
import os
import sys
sys.path.append('/Users/Stephaniewang/Documents/snorkel')
from snorkel import SnorkelSession
from snorkel.contrib.pipelines import merge_configs
from snorkel.models import candidate_subclass
from snorkel.contrib.babble import ExplanationIO
from experiments.babble.spouse import SpousePipeline
from snorkel.viewer import SentenceNgramViewer
from snorkel.contrib.babble import Explanation
from snorkel.contrib.babble import Babbler
from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField
from wtforms.fields import RadioField, SubmitField, BooleanField
from flask_bootstrap import Bootstrap
from snorkel.contrib.babble import BabbleStream
from snorkel.lf_helpers import *
from experiments.babble.spouse.spouse_examples import get_explanations, get_user_lists
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')


class ExplanationForm(FlaskForm):
	explanation = TextAreaField('Explanation', [validators.DataRequired()])

class LabelingFunctionForm(FlaskForm):
	pass

def restart():
	session = current_app.config['session']
	Spouse = candidate_subclass('Spouse', ['person1', 'person2'])
	current_app.config['babble_stream_object'] = BabbleStream(session, candidate_class=Spouse, balanced=True, seed=123, soft_start=True)
	current_app.config['metrics'] = {'lf_stats': '', 'coverage': 0, 'num_labels': 0, 'num_examples': 0, 'num_labels_equiv': 0, 'f1': 0}
	current_app.config['candidate'] = current_app.config['babble_stream_object'].next()

def candidate_html(c):
	chunks = get_text_splits(c)
	div_tmpl = u'''<div style="border: 1px #858585; box-shadow:0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    background-color:#FDFDFD; padding:5pt 10pt 5pt 10pt; width: 80%; margin: auto; margin-top: 2%">	
    {}</div>'''
	arg_tmpl = u'<b style="background-color:#ffd77c;padding:1pt 5pt 1pt 5pt;">{}</b>'
	sent_tmpl = u'<p style="font-size:12pt;">{}</p>'
	text = u""
	for s in chunks[0:]:
	    if s in [u"{{A}}", u"{{B}}"]:
	        span = c[0].get_span() if s == u"{{A}}" else c[1].get_span()
	        text += arg_tmpl.format(span)
	    else:
	        text += s.replace(u"\n", u"<BR/>")
	html = div_tmpl.format(sent_tmpl.format(text.strip()))
	return html

def sentence_html(c):
	chunks = get_text_splits(c)
	arg_tmpl = u'<b style="padding:1pt 5pt 1pt 5pt;">{}</b>'
	sent_tmpl = u'<p style="font-size:10pt;">{}</p>'
	text = u""
	for s in chunks[0:]:
	    if s in [u"{{A}}", u"{{B}}"]:
	        span = c[0].get_span() if s == u"{{A}}" else c[1].get_span()
	        text += arg_tmpl.format(span)
	    else:
	        text += s.replace(u"\n", u"<BR/>")
	html = sent_tmpl.format(text.strip())
	return html

def apply_filtered_analysis(filtered_parses, translator):
	row_tmpl = u'<dl class="row">{}</dl>'
	dt_header_tmpl = u'<dt class="col-sm-12">{}</dt>'
	dt_tmpl = u'<dt class = "col-sm-3">{}</dt>'
	dd_tmpl = u'<dd class= "col-sm-9">{}</dd><br/>'
	text = u""

	if not any(filtered_parses.values()):
		return None
	num_filtered = 0
	filter_names = [
	'UnparseableExplanations',
	'DuplicateSemanticsFilter',
	'ConsistencyFilter',
	'UniformSignatureFilter',
	'DuplicateSignatureFilter']
	for filter_name in filter_names:
		parses = filtered_parses.get(filter_name, [])
		for filtered_parse in parses:
			num_filtered += 1

			if filtered_parse.reason == 'Unparseable':
			    parse_str = filtered_parse.parse.condition
			else:
			    parse_str = translator(filtered_parse.parse.semantics)

			if filter_name == 'UnparseableExplanations':
			    filter_str = "Unparseable Explanation"
			    reason_str = "This explanation couldn't be parsed."

			elif filter_name == 'DuplicateSemanticsFilter':
			    filter_str = "Duplicate Semantics"
			    reason_str = 'This parse is identical to one produced by the following explanation:\n\t"{}"'.format(filtered_parse.reason.explanation.condition)
			    
			elif filter_name == 'ConsistencyFilter':
			    candidate = filtered_parse.reason
			    filter_str = "Inconsistency with Example"
			    reason_str = "This parse did not agree with the candidate ({}, {})".format(candidate[0].get_span(), candidate[1].get_span())
			    
			elif filter_name == 'UniformSignatureFilter':
				filter_str = "Uniform Signature"
				bs = current_app.config['babble_stream_object']
				reason_str = "This parse labeled {} of the {} development examples".format(
			        filtered_parse.reason, bs.num_dev_total)
			    
			elif filter_name == 'DuplicateSignatureFilter':
			    filter_str = "Duplicate Signature"
			    reason_str = "This parse labeled identically to the following existing parse:\n\t{}".format(
			        translator(filtered_parse.reason.explanation))

			text += '<br/>'
			text += dt_header_tmpl.format("#{}: {}".format(num_filtered, filter_str))
			if filtered_parse.reason == 'Unparseable':
			    text += dt_tmpl.format("Explanation:")
			    text += dd_tmpl.format(parse_str)
			else:
			    text += dt_tmpl.format("Parse:") 
			    text += dd_tmpl.format(parse_str)
			text += dt_tmpl.format("Reason:")
			text +=  dd_tmpl.format(reason_str)
			text += '<br/>'
	html = row_tmpl.format(text.strip())
	return html

def get_metrics(bs):
	# get the metrics to display
	metrics = current_app.config['metrics']
	num_examples = len(bs.get_explanations())
	if num_examples < 1:
		return metrics
	metrics['num_examples'] = num_examples
	metrics['lf_stats'] = bs.get_lf_stats().to_html(columns=['Coverage', 'Overlaps', 'TP', 'FP', 'FN', 'TN', 'Empirical Acc.'])
	metrics['coverage'] = bs.get_global_coverage().numer/float(bs.get_global_coverage().denom) * 100
	metrics['num_labels'] = len(bs.get_lfs())
	return metrics

def finish_pipeline(bs):
		pipe = current_app.config['pipe']
		pipe.set_babbler_matrices(bs)
		pipe.supervise()
		pipe.classify()

main_page = Blueprint('main_page', __name__, template_folder='templates')

@main_page.route("/", methods=['GET', 'POST'])
def index():
	bs = current_app.config['babble_stream_object']
	form1 = ExplanationForm(request.form)
	form2 = LabelingFunctionForm(request.form)

	metrics = get_metrics(bs)

	suggested_explanations = None
	candidate_id = current_app.config['candidate'].get_stable_id()
	if candidate_id in current_app.config['priority_ids'].keys():
		priority_ids_dict = current_app.config['priority_ids']
		suggested_explanations = priority_ids_dict[candidate_id]


	# CASE 1: SKIP THE CURRENT SAMPLE
	if request.method == 'POST' and "skip" in request.form:
		current_app.config['candidate'] = bs.next() # GET THE NEXT CANDIDATE
		candidate = candidate_html(current_app.config['candidate'])
		return redirect('/')

	# CASE 2: SUBMIT AN EXPLANATION
	print request.form
	if request.method == 'POST' and form1.validate_on_submit() and ("pos" in request.form or "neg" in request.form):
		candidate = candidate_html(current_app.config['candidate'])
		if "pos" in request.form: label = True
		elif "neg" in request.form: label = False
		condition = form1.explanation.data
		num_explanations = len(bs.get_explanations())
		explanation = Explanation(
			condition, 
			label, 
			candidate=current_app.config['candidate'],
			name='Exp{}:{}...'.format(num_explanations,condition[:25])
		)

		###### for debugging purposes ######
		print current_app.config['priority_ids']
		print current_app.config['candidate']
		print label
		print condition
		print explanation
		###################################

		parse_results = bs.apply(explanation)
		print len(parse_results)
		if len(parse_results[0]) > 0:
			parse_list, filtered_parses, conf_matrix_list, stats_list = parse_results
			parse_list = [bs.semparser.grammar.translate(parse.semantics) for parse in parse_list]
			correct_incorrect_sentences = []
			for idx in range(len(conf_matrix_list)):
				tf_sentence_dict = {}
				tf_sentence_dict["correct"] = [sentence_html(sentence) for sentence in conf_matrix_list[idx].correct]
				tf_sentence_dict["incorrect"] = [sentence_html(sentence) for sentence in conf_matrix_list[idx].incorrect]
				tf_sentence_dict["abstain"] = [sentence_html(sentence) for sentence in conf_matrix_list[idx].abstained]
				correct_incorrect_sentences.append(tf_sentence_dict)

			filtered_analysis = apply_filtered_analysis(filtered_parses, bs.semparser.grammar.translate)

			displayed_stats = zip(parse_list, correct_incorrect_sentences, stats_list)

			return render_template('index.html', candidate=candidate, form=form1, stats=displayed_stats, filtered_analysis=filtered_analysis, form2=form2, metrics=metrics, suggested_explanations=suggested_explanations)
		else:
			# generated no new parses
			filtered_parses = parse_results[1]
			filtered_analysis = apply_filtered_analysis(filtered_parses, bs.semparser.grammar.translate)
			return render_template('index.html', candidate=candidate, form=form1, no_parse_error = "True", filtered_analysis=filtered_analysis, metrics=metrics, suggested_explanations=suggested_explanations)

	# CASE 3: COMMIT THE LFS 
	elif request.method == 'POST' and "commit" in request.form:
		bs.commit()

		# update the metrics
		(f1, pr, re) = bs.get_majority_quality(split=1)
		metrics = current_app.config['metrics']
		metrics['f1'] = f1
		metrics['num_labels_equiv'] = bs.get_labeled_equivalent(f1)

		# get the next candidate
		current_app.config['candidate'] = bs.next()
		flash('You\'ve successfully committed your explanation', 'success')
		return redirect('/')

	# CASE 4: FINISH THE PIPELINE -- LABEL DATASET AND TRAIN MODEL
	elif request.method == 'POST' and "restart" in request.form:
		# finish_pipeline(bs)
		restart()
		return redirect('/')
		
	candidate = candidate_html(current_app.config['candidate'])

	return render_template('index.html', candidate=candidate, form=form1, metrics=metrics, suggested_explanations=suggested_explanations)

