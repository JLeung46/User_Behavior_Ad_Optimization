import pandas as pd
import numpy as np

def split_data():
	'''
	Splits the data into training and test sets
	and saves each as a csv file.
	'''
	test_start_date = '2015-05-12'
	test_data_all = df[df['search_date'] > '2015-05-12']
	train_data_all = df[df['search_date'] <= '2015-05-12']

	test_sorted = test_data_all.sort_values(['user_id','search_date'],ascending=[True,True])
	user_last_sessions = test_sorted.drop_duplicates(subset='user_id',take_last=True)

	test = df[df['search_id'].isin(user_last_sessions['search_id'])]
	train = df[~df['search_id'].isin(user_last_sessions['search_id'])]

	train.to_csv('train.csv')
	test.to_csv('test.csv')

def make_user_features():
	'''
	Generates user level features using training set only. If user is found in test data,
	fill in appropriate values.
	'''
	
	# Engineer User Features
	train['user_clicks'] = df.groupby('user_id')['is_click'].transform("sum")
	train['user_impressions'] = df.groupby('user_id')['is_click'].transform("size")

	test = test.assign(user_clicks = test['user_id'].map(train.groupby('user_id')['is_click'].sum()).fillna(0).astype(int))
	test = test.assign(user_impressions = test['user_id'].map(train.groupby('user_id')['is_click'].size()).fillna(0).astype(int))