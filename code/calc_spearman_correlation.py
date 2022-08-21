import pandas as pd
import os
import numpy as np
from scipy import stats

from calc_Krippendorf_alpha import column_types, binary_list, factual_list, likert_list, read_data_valid
from collections import Counter

def test_spearman(variable_1_list, variable_2_list, name1, name2):
	correlation, pvalue = stats.spearmanr(variable_1_list, variable_2_list)
	# print(correlation, pvalue)
	print("Variable {} and variable {} have spearman correlation {:.3f} and pvalue {:.3f}".format(name1, name2, correlation, pvalue))

def calc_mean_std_factual():
	data_folder = "../data/"
	filenames = ["Analogy_evaluation_expert - E1.csv", "Analogy_evaluation_expert - E2.csv", "Analogy_evaluation_expert - E3.csv", "Analogy_evaluation_expert - E4.csv", "Analogy_evaluation_expert - E5.csv"]
	all_data_dict = {}
	factual_correct_dict = {}
	facutal_incorrect_dict = {}
	for col_name in column_types:
		all_data_dict[col_name] = []
		factual_correct_dict[col_name] = []
		facutal_incorrect_dict[col_name] = []
	number_invalid = 0
	number_total = 0
	invalid_analogy_dict = {}
	# syntactic_correctness_annotation = {}
	# factual_correctness_annotation = {}
	for filename in filenames:
		annotation_dict, annotation_key_set, invalid_analogy_set, invalid_dict = read_data_valid(data_folder, filename)
		for participant_id, task_id in annotation_dict:
			tp_key = (participant_id, task_id)
			# if tp_key not in syntactic_correctness_annotation:
			# 	syntactic_correctness_annotation[tp_key] = {}
			# if tp_key not in factual_correctness_annotation:
			# 	factual_correctness_annotation[tp_key] = {}
			if tp_key not in invalid_analogy_dict:
				invalid_analogy_dict[tp_key] = 0
			tp_data = annotation_dict[(participant_id, task_id)]
			number_total += 1
			facutal_correctness = tp_data["Factual Correctness"]
			if tp_data["Valid"] == "No":
				number_invalid += 1
				invalid_analogy_dict[tp_key] += 1
			else:
				for col_name in column_types:
					tp_type = column_types[col_name]
					if tp_type == "likert":
						if tp_data[col_name] == "#REF!" or pd.isna(tp_data[col_name]):
							# Garrett hasn't finished this part
							assert filename == "Analogy_evaluation_expert - Garrett.csv"
							continue
						all_data_dict[col_name].append(int(tp_data[col_name]))
						tp_cat = "No" if facutal_correctness == "No" else "Yes"
						if facutal_correctness == "No":
							facutal_incorrect_dict[col_name].append(int(tp_data[col_name]))
						else:
							factual_correct_dict[col_name].append(int(tp_data[col_name]))
					else:
						if pd.isna(tp_data[col_name]):
							assert filename == "Analogy_evaluation_expert - Garrett.csv"
							continue
						all_data_dict[col_name].append(tp_data[col_name])
						if facutal_correctness == "No":
							facutal_incorrect_dict[col_name].append(tp_data[col_name])
						else:
							factual_correct_dict[col_name].append(tp_data[col_name])
	print("In total, {} rows among {} rows are invalid".format(number_invalid, number_total))
	print("-" * 17)
	helpfulness_list = factual_correct_dict["Helpfulness"]
	for col_name in all_data_dict:
		if col_name == "Helpfulness":
			continue
		tp_type = column_types[col_name]
		print(col_name, len(factual_correct_dict[col_name]), len(facutal_incorrect_dict[col_name]), len(all_data_dict[col_name]))
		if tp_type == "likert":
			tp_list = factual_correct_dict[col_name]
			test_spearman(tp_list, helpfulness_list, col_name, "Helpfulness")
			print("Factually correct, mean:{:.2f} std:{:.2f}".format(np.mean(factual_correct_dict[col_name]), np.std(factual_correct_dict[col_name], ddof=1) ))
			# print("Factually incorrect, mean:{:.2f} std:{:.2f}".format(np.mean(facutal_incorrect_dict[col_name]), np.std(facutal_incorrect_dict[col_name], ddof=1) ))
			print("-" * 17)

calc_mean_std_factual()