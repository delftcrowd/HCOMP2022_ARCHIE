import pandas as pd
import os
import numpy as np


from calc_Krippendorf_alpha import column_types, binary_list, factual_list, likert_list, read_data_valid
from collections import Counter


def compare_domains():
	data_folder = "../data/"
	filenames = ["Analogy_evaluation_expert - E1.csv", "Analogy_evaluation_expert - E2.csv", "Analogy_evaluation_expert - E3.csv", "Analogy_evaluation_expert - E4.csv", "Analogy_evaluation_expert - E5.csv"]
	place_data_dict = {}
	calorie_data_dict = {}
	for col_name in column_types:
		place_data_dict[col_name] = []
		calorie_data_dict[col_name] = []
	number_invalid = 0
	number_total = 0
	invalid_analogy_dict = {}
	all_ct = {}
	for filename in filenames:
		annotation_dict, annotation_key_set, invalid_analogy_set, invalid_dict = read_data_valid(data_folder, filename)
		for participant_id, task_id in annotation_dict:
			tp_key = (participant_id, task_id)
			if task_id.startswith("P"):
				current_task = "Place"
			else:
				current_task = "Calorie"
			if current_task not in all_ct:
				all_ct[current_task] = 0
			all_ct[current_task] += 1
			if tp_key not in invalid_analogy_dict:
				invalid_analogy_dict[tp_key] = 0
			tp_data = annotation_dict[(participant_id, task_id)]
			number_total += 1
			if tp_data["Valid"] == "No":
				number_invalid += 1
				invalid_analogy_dict[tp_key] += 1
			else:
				if tp_data["Factual Correctness"] == "No":
					# ignore all factual incorrect cases
					continue
				for col_name in column_types:
					tp_type = column_types[col_name]
					if tp_type == "likert":
						if tp_data[col_name] == "#REF!" or pd.isna(tp_data[col_name]):
							# Garrett hasn't finished this part
							# assert filename == "Analogy_evaluation_expert - Garrett.csv"
							raise NotImplementedError
							continue
						# all_data_dict[col_name].append(int(tp_data[col_name]))
						if current_task == "Place":
							place_data_dict[col_name].append(int(tp_data[col_name]))
						else:
							calorie_data_dict[col_name].append(int(tp_data[col_name]))
					else:
						if pd.isna(tp_data[col_name]):
							# assert filename == "Analogy_evaluation_expert - Garrett.csv"
							raise NotImplementedError
							continue
						# all_data_dict[col_name].append(tp_data[col_name])
						if current_task == "Place":
							place_data_dict[col_name].append(tp_data[col_name])
						else:
							calorie_data_dict[col_name].append(tp_data[col_name])
	print("-" * 17)
	print("In total, {} rows among {} rows are invalid".format(number_invalid, number_total))
	print(all_ct)
	print("For the reserved part, {} rows valid and factually correct for calorie domain, {} rows valid and factually correct for place domain".format(len(calorie_data_dict["structural correspondence"]), len(place_data_dict["structural correspondence"]) ))
	from scipy import stats
	print("-" * 17)
	for col_name in column_types:
		tp_type = column_types[col_name]
		if tp_type == "likert":
			statistic, pvalue = stats.kruskal(place_data_dict[col_name], calorie_data_dict[col_name])
			print(col_name)
			print("kruskal test result: H:{:.3f}, p:{:.3f}".format(statistic, pvalue))
			print("mean for place:{:.2f}".format(np.mean(place_data_dict[col_name])))
			print("mean for calorie:{:.2f}".format(np.mean(calorie_data_dict[col_name])))
			print("-" * 17)
			if pvalue < 0.05:
				statistic, pvalue = stats.mannwhitneyu(place_data_dict[col_name], calorie_data_dict[col_name], alternative='two-sided')
				print("place <> calorie,", "pvalue %.4f"%pvalue, "statistic %.4f"%statistic)
				statistic, pvalue = stats.mannwhitneyu(place_data_dict[col_name], calorie_data_dict[col_name], alternative='greater')
				print("place > calorie,", "pvalue %.4f"%pvalue, "statistic %.4f"%statistic)
				statistic, pvalue = stats.mannwhitneyu(place_data_dict[col_name], calorie_data_dict[col_name], alternative='less')
				print("place < calorie,", "pvalue %.4f"%pvalue, "statistic %.4f"%statistic)
				print("-" * 17)
	print("Domain")
	print("Place Task:")
	print(Counter(place_data_dict["Domain"]))
	print("Calorie Task:")
	print(Counter(calorie_data_dict["Domain"]))
	print("-" * 17)
	print("Relation")
	print("Place Task:")
	print(Counter(place_data_dict['Relation Type']))
	print("Calorie Task:")
	print(Counter(calorie_data_dict['Relation Type']))

compare_domains()