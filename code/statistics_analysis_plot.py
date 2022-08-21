import pandas as pd
import os
import numpy as np


from calc_Krippendorf_alpha import column_types, binary_list, factual_list, likert_list, read_data_valid
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter


def draw_box_plot(data_dict, mean_dict, sd_dict, median_dict):
	df = pd.DataFrame(data_dict, dtype=float)
	# print(df.isnull().sum())
	# print(df)
	sns.set_theme(style="whitegrid")
	sns.set(font="Arial")
	# tips = sns.load_dataset("tips")
	# print(type(tips))
	# print(df)
	# print(type(df))
	# print(len(data[0]), len(data[1]), len(data[2]), len(data[3]))
	# ax = sns.boxplot(data=df, showmeans=True, meanprops={"marker":"o", "markerfacecolor":"white",  "markeredgecolor":"black", "markersize":"10"})
	ax = sns.boxplot(data=df)

	# Calculate number of obs per group & median to position labels
	# medians = df.groupby(['species'])['sepal_length'].median().values
	# nobs = df['species'].value_counts().values
	# nobs = [str(x) for x in nobs.tolist()]
	# nobs = ["n: " + i for i in nobs]
	key_list = list(data_dict.keys())
	mean_list = [mean_dict[tp_key] for tp_key in key_list]
	text_list = ["M: {:.2f}\nSD: {:.2f}".format(mean_dict[tp_key], sd_dict[tp_key]) for tp_key in key_list]
	 
	# Add it to the plot
	pos = range(len(text_list))
	for tick,label in zip(pos,ax.get_xticklabels()):
	    ax.text(pos[tick],
	            mean_list[tick] + 0.03,
	            text_list[tick],
	            horizontalalignment='center',
	            size=18,
	            color='w',
	            weight='semibold')

	# ax = sns.boxplot(x="day", y="total_bill", hue="smoker", data=tips, palette="Set3")
	ax.tick_params(labelsize=18)
	ax.set_xlabel("Dimension", fontsize = 24)
	ax.set_ylabel("Value", fontsize = 24)
	plt.margins(0.015, tight=True)
	plt.show()

def draw_bar_plot(data_dict):
	df = pd.DataFrame(data_dict, dtype=float)
	sns.set_theme(style="whitegrid")
	sns.set(font="Arial")
	# ax = sns.boxplot(data=df)
	ax = sns.barplot(x="Dimension", y="Value", hue="Facutal_Correctness", data=df)
	ax.tick_params(labelsize=18)
	ax.set_xlabel("Dimension", fontsize = 24)
	ax.set_ylabel("Value", fontsize = 24)
	plt.setp(ax.get_legend().get_texts(), fontsize='16') # for legend text
	plt.setp(ax.get_legend().get_title(), fontsize='16') # for legend title
	plt.margins(0.015, tight=True)
	# ax.legend(labels=["Yes","No"], fontsize = 18)
	plt.show()

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
	data_long_format = {}
	data_long_format["Dimension"] = []
	data_long_format["Value"] = []
	data_long_format["Facutal_Correctness"] = []
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
						if col_name == "Relational similarity":
							data_long_format["Dimension"].append("Relational\nSimilarity")
						elif col_name == "structural correspondence":
							data_long_format["Dimension"].append("Structural\nCorrespondence")
						else:
							data_long_format["Dimension"].append(col_name)
						# data_long_format["col_name"].append(col_name)
						data_long_format["Value"].append(int(tp_data[col_name]))
						tp_cat = "No" if facutal_correctness == "No" else "Yes"
						data_long_format["Facutal_Correctness"].append(tp_cat)
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
	plot_data_dict = {}
	mean_dict = {}
	median_dict = {}
	sd_dict = {}
	print("-" * 17)
	for col_name in all_data_dict:
		tp_type = column_types[col_name]
		print(col_name, len(factual_correct_dict[col_name]), len(facutal_incorrect_dict[col_name]), len(all_data_dict[col_name]))
		if tp_type == "likert":
			if col_name == "Relational similarity":
				# plot_data_dict["Relational\nSimilarity"] = factual_correct_dict[col_name]
				tp_name = "Relational\nSimilarity"
			elif col_name == "structural correspondence":
				# plot_data_dict["Structural\nCorrespondence"] = factual_correct_dict[col_name]
				tp_name = "Structural\nCorrespondence"
			else:
				# plot_data_dict[col_name] = factual_correct_dict[col_name]
				tp_name = col_name
			plot_data_dict[tp_name] = factual_correct_dict[col_name]
			print("Factually correct, mean:{:.2f} std:{:.2f}".format(np.mean(factual_correct_dict[col_name]), np.std(factual_correct_dict[col_name], ddof=1) ))
			mean_dict[tp_name] = np.mean(factual_correct_dict[col_name])
			sd_dict[tp_name] = np.std(factual_correct_dict[col_name], ddof=1)
			median_dict[tp_name] = np.median(factual_correct_dict[col_name])
			# print("Factually incorrect, mean:{:.2f} std:{:.2f}".format(np.mean(facutal_incorrect_dict[col_name]), np.std(facutal_incorrect_dict[col_name], ddof=1) ))
			print("-" * 17)
	# draw_bar_plot(data_long_format)
	draw_box_plot(plot_data_dict, mean_dict, sd_dict, median_dict)

def calc_mean_std():
	data_folder = "./"
	filenames = ["Analogy_evaluation_expert - Garrett.csv", "Analogy_evaluation_expert - Lorenzo.csv", "Analogy_evaluation_expert - Peide.csv", "Analogy_evaluation_expert - Philip.csv", "Analogy_evaluation_expert - Yao.csv"]
	all_data_dict = {}
	for col_name in column_types:
		all_data_dict[col_name] = []
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
			if tp_data["Valid"] == "No":
				number_invalid += 1
				invalid_analogy_dict[tp_key] += 1
			else:
				for col_name in column_types:
					tp_type = column_types[col_name]
					if tp_type == "likert":
						if tp_data[col_name] == "#REF!" or pd.isna(tp_data[col_name]):
							# Garrett hasn't finished this part
							# assert filename == "Analogy_evaluation_expert - Garrett.csv"
							print(tp_data)
							raise NotImplementedError
							continue
						all_data_dict[col_name].append(int(tp_data[col_name]))
					else:
						if pd.isna(tp_data[col_name]):
							# assert filename == "Analogy_evaluation_expert - Garrett.csv"
							# print(filename)
							# print(tp_data)
							raise NotImplementedError
							continue
						all_data_dict[col_name].append(tp_data[col_name])
	print("In total, {} rows among {} rows are invalid".format(number_invalid, number_total))
	number_all_valid = 0
	only_one = 0
	for tp_key in invalid_analogy_dict:
		if invalid_analogy_dict[tp_key] == 0:
			number_all_valid += 1
		elif invalid_analogy_dict[tp_key] <= 1:
			only_one += 1
		else:
			print(tp_key, invalid_analogy_dict[tp_key])
	print("Among {} rows, {} rows are recognized as valid by all experts, {} rows only receive 1 invalid".format(len(invalid_analogy_dict), number_all_valid, only_one))
	print(Counter(all_data_dict["Syntactic correctness"]))
	print(Counter(all_data_dict["Factual Correctness"]))
	print(Counter(all_data_dict["Misunderstanding"]))
	print(Counter(all_data_dict["Domain"]))
	print(Counter(all_data_dict['Relation Type']))
	# plot_data_dict = {}
	# for col_name in all_data_dict:
	# 	tp_type = column_types[col_name]
	# 	print(col_name, len(all_data_dict[col_name]))
	# 	if tp_type == "likert":
	# 		# if col_name != "Transferability" and col_name != "Simplicity":
	# 		if col_name == "Relational similarity":
	# 			plot_data_dict["Relational\nSimilarity"] = all_data_dict[col_name]
	# 		elif col_name == "structural correspondence":
	# 			plot_data_dict["Structural\nCorrespondence"] = all_data_dict[col_name]
	# 		else:
	# 			plot_data_dict[col_name] = all_data_dict[col_name]
	# 		print("mean:{:.2f}".format(np.mean(all_data_dict[col_name])))
	# 		print("std:{:.2f}".format(np.std(all_data_dict[col_name], ddof=1)))
	# draw_box_plot(plot_data_dict)

# calc_mean_std()
calc_mean_std_factual()