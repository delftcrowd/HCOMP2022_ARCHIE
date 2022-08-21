import krippendorff
import pandas as pd
import os
import numpy as np

choice_dict = {"Yes": 0, "No": 1, "Not Sure":2}
column_types = {
	"Valid": "binary",
	"Syntactic correctness": "binary",
	"Misunderstanding": "binary",
	"Factual Correctness": "three-level",
	"structural correspondence": "likert",
	"Relational similarity": "likert",
	"Familiarity": "likert",
	"Helpfulness": "likert",
	"Transferability": "likert",
	"Simplicity": "likert",
	"Domain": "string",
	"Relation Type": "string"
}

binary_list = ['Yes', 'No']
factual_list = ['Yes without switch', 'Yes with switch', 'No']
likert_list = [1, 2, 3, 4, 5]

def read_data_valid(data_folder, filename):
	df = pd.read_csv(os.path.join(data_folder, filename))
	# df = df.astype({"structural correspondence": int, "Relational similarity": int, "Familiarity":int, "Helpfulness":int, "Transferability":int, "Simplicity":int,})
	# df.fillna("None")
	# df.replace('#REF!', "None")
	data_records = df.to_dict('record')
	# print(tp_dict.keys())
	# print(tp_dict[0])
	invalid_dict = {}
	annotation_dict = {}
	invalid_analogy_set = set()
	annotation_key_set = set()
	for one_row in data_records:
		assert one_row['Valid'] in ['Yes', 'No']
		tp_key = (one_row['participant_id'], one_row['task_id'])
		annotation_dict[tp_key] = one_row
		annotation_key_set.add(tp_key)
		if one_row['Valid'] == 'No':
			invalid_analogy_set.add(tp_key)
			continue
		else:
			invalid_flag = False
			try:
				if one_row['Factual Correctness'] == 'No':
					assert int(one_row['Helpfulness']) == 1
					assert int(one_row['Transferability']) == 1
			except:
				print("Rule not followed", filename)
				print(one_row)
			for col_name in column_types:
				tp_type = column_types[col_name]
				tp_data = one_row[col_name]
				try:
					if tp_type == "binary":
						assert tp_data in binary_list
					elif tp_type == "three-level":
						assert tp_data in factual_list
					elif tp_type == "likert":
						assert int(tp_data) in likert_list
					elif tp_type == "string":
						assert len(tp_data) > 0
					else:
						raise NotImplementedError
				except:
					invalid_flag = True
					# print(col_name, tp_type, tp_data)
					if col_name not in invalid_dict:
						invalid_dict[col_name] = 0
					invalid_dict[col_name] += 1
			# if not invalid_flag:
			# annotation_dict[tp_key] = one_row
	# print("For file {}, we find {} invalid rows, and other invalid case: {}".format(filename, len(invalid_analogy_set), invalid_dict))
	# print("For file {}, we have {} keys in annotation_dict".format(filename, len(annotation_dict)))
	return annotation_dict, annotation_key_set, invalid_analogy_set, invalid_dict


def calc_krippendorff_alpha(annotation_list, used_keys, col_name):
	tp_type = column_types[col_name]
	if tp_type == "likert":
		data_length = len(likert_list)
	elif tp_type == "binary":
		data_length = len(binary_list)
	elif tp_type == "three-level":
		data_length = len(factual_list)
	else:
		raise NotImplementedError
	value_counts = []
	number_value_used = 0
	for tp_key in used_keys:
		cur_val_ct = [0] * data_length
		for annotation_dict in annotation_list:
			try:
				assert tp_key in annotation_dict
			except:
				print(tp_key, annotation_dict.keys())
				exit(-1)
			tp_data = annotation_dict[tp_key][col_name]
			if tp_type == "likert":
				tp_data_index = likert_list.index(int(tp_data))
			elif tp_type == "binary":
				tp_data_index = binary_list.index(tp_data)
			elif tp_type == "three-level":
				tp_data_index = factual_list.index(tp_data)
			else:
				raise NotImplementedError
			cur_val_ct[tp_data_index] += 1
			number_value_used += 1
		value_counts.append(cur_val_ct)
	value_counts = np.array(value_counts)
	# print("Shape of value_counts: {}, {} values used in total".format(value_counts.shape, number_value_used))
	# print(value_counts)
	print('alpha for {} is: {:.2f}'.format(col_name, krippendorff.alpha(value_counts=value_counts,level_of_measurement='nominal') ))

def calc_krippendorff_alpha_special(annotation_list, used_keys, col_name):
	tp_type = column_types[col_name]
	new_likert_list = [1, 2, 3]
	if tp_type == "likert":
		data_length = len(new_likert_list)
	elif tp_type == "binary":
		data_length = len(binary_list)
	elif tp_type == "three-level":
		data_length = len(factual_list)
	else:
		raise NotImplementedError
	value_counts = []
	number_value_used = 0
	for tp_key in used_keys:
		cur_val_ct = [0] * data_length
		for annotation_dict in annotation_list:
			try:
				assert tp_key in annotation_dict
			except:
				print(tp_key, annotation_dict.keys())
				exit(-1)
			tp_data = annotation_dict[tp_key][col_name]
			if tp_type == "likert":
				original_value = int(tp_data)
				transformed_value = 0
				if original_value <= 2:
					transformed_value = 1
				elif original_value == 3:
					transformed_value = 2
				else:
					transformed_value = 3
				tp_data_index = new_likert_list.index(transformed_value)
			elif tp_type == "binary":
				tp_data_index = binary_list.index(tp_data)
			elif tp_type == "three-level":
				tp_data_index = factual_list.index(tp_data)
			else:
				raise NotImplementedError
			cur_val_ct[tp_data_index] += 1
			number_value_used += 1
		value_counts.append(cur_val_ct)
	value_counts = np.array(value_counts)
	# print("Shape of value_counts: {}, {} values used in total".format(value_counts.shape, number_value_used))
	# print(value_counts)
	print('alpha for {} is: {:.2f}'.format(col_name, krippendorff.alpha(value_counts=value_counts,level_of_measurement='nominal') ))

def find_disagreement(annotation_list, used_keys):
	value_counts = []
	for tp_key in used_keys:
		print(tp_key, annotation_list[0][tp_key]["Factual Correctness"])
		for col_name in ["Syntactic correctness", "Factual Correctness", "Misunderstanding"]:
			tp_str = col_name
			for annotation_dict in annotation_list:
				tp_data = annotation_dict[tp_key][col_name]
				tp_str += "& " + tp_data
			tp_str += "&" + tp_data
			print(col_name, tp_str)
		for col_name in ["structural correspondence", "Relational similarity", "Familiarity", "Helpfulness", "Transferability", "Simplicity"]:
			# print(col_name)
			tp_str = col_name
			cur_val_ct = [0] * 5
			for annotation_dict in annotation_list:
				try:
					assert tp_key in annotation_dict
				except:
					print(tp_key, annotation_dict.keys())
					exit(-1)
				tp_data = annotation_dict[tp_key][col_name]
				tp_data_index = likert_list.index(int(tp_data))
				tp_str += "&" + str(int(tp_data))
				cur_val_ct[tp_data_index] += 1
			# print(col_name, cur_val_ct)
			print(col_name, tp_str)
		print("-" * 17)


def calc_common_coverage():
	data_folder = "../data/"
	filenames = ["Analogy_evaluation_expert - E1.csv", "Analogy_evaluation_expert - E2.csv", "Analogy_evaluation_expert - E3.csv", "Analogy_evaluation_expert - E4.csv", "Analogy_evaluation_expert - E5.csv"]
	user_data_dict = {}
	for filename in filenames:
		user_data_dict[filename] = {}
		# annotation_dict, annotation_key_set, invalid_analogy_set = read_data_valid(data_folder, filename)
		user_data_dict[filename] = read_data_valid(data_folder, filename)
	common_keys = user_data_dict[filenames[0]][1]
	for i in range(1, 5):
		common_keys = common_keys & user_data_dict[filenames[i]][1]
	print("There are {} rows overlap by each annotator".format(len(common_keys)))
	# for i in range(5):
	# 	if len(user_data_dict[filenames[i]][3]) > 0:
	# 		invalid_keys = user_data_dict[filenames[i]][3].keys()
	# 		print("Invlaid annotation: {} - {}".format(filenames[i], invalid_keys))
	invalid_ct = {}
	for filename in filenames:
		invalid_analogy_set = user_data_dict[filename][2]
		number_invalid = len(common_keys & invalid_analogy_set)
		for ckey_ in common_keys & invalid_analogy_set:
			if ckey_ not in invalid_ct:
				invalid_ct[ckey_] = []
			invalid_ct[ckey_].append(filename.split(" ")[2])
		# print("Among {} overlap case, {} think {} are invalid analogy".format(len(common_keys), filename.split(" ")[2], number_invalid ))
	annotation_list = [user_data_dict[filename][0] for filename in filenames]
	used_keys = common_keys - set(invalid_ct.keys())
	# calculate the agreement on valid with 29 overlap
	print('-' * 17)
	print("Calculate krippendorff_alpha for Valid, Based on 29 overlap rows")
	calc_krippendorff_alpha(annotation_list, common_keys, col_name= "Valid")
	print('-' * 17)

	print("Calculate krippendorff_alpha for other dimensions, Based on 22 valid rows, 5 annotators")
	# calculate the agreement on other dimensions with 22 valid rows
	calc_krippendorff_alpha(annotation_list, used_keys, col_name= "Syntactic correctness")
	calc_krippendorff_alpha(annotation_list, used_keys, col_name= "Factual Correctness")
	calc_krippendorff_alpha(annotation_list, used_keys, col_name= "Misunderstanding")
	# calc_krippendorff_alpha(annotation_list, used_keys, col_name= "structural correspondence")
	# calc_krippendorff_alpha(annotation_list, used_keys, col_name= "Relational similarity")
	# calc_krippendorff_alpha(annotation_list, used_keys, col_name= "Familiarity")
	# calc_krippendorff_alpha(annotation_list, used_keys, col_name= "Helpfulness")
	# print('-' * 17)

	# Garrett hasn't finished 'Transferability', 'Simplicity', 'Domain', 'Relation Type'
	# annotation_list = [user_data_dict[filename][0] for filename in filenames[1:]]
	# assert len(annotation_list) == 4
	# print("Calculate krippendorff_alpha for Transferability and Simplicity, Based on 22 valid rows, 4 annotators, Garrett will finish this part by Monday")
	# calc_krippendorff_alpha(annotation_list, used_keys, col_name= "Transferability")
	# calc_krippendorff_alpha(annotation_list, used_keys, col_name= "Simplicity")
	print('-' * 17)
	calc_krippendorff_alpha_special(annotation_list, used_keys, col_name= "structural correspondence")
	calc_krippendorff_alpha_special(annotation_list, used_keys, col_name= "Relational similarity")
	calc_krippendorff_alpha_special(annotation_list, used_keys, col_name= "Familiarity")
	calc_krippendorff_alpha_special(annotation_list, used_keys, col_name= "Helpfulness")
	calc_krippendorff_alpha_special(annotation_list, used_keys, col_name= "Transferability")
	calc_krippendorff_alpha_special(annotation_list, used_keys, col_name= "Simplicity")
	# print(used_keys)
	# find_disagreement(annotation_list, used_keys)


if __name__ == '__main__':
	calc_common_coverage()
	# calc_common_correctness()