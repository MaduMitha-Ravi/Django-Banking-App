from pandas import read_csv
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import pandas as pd

class machinelearning:

	def machinelearning():

		final_df = pd.read_csv('Banker/datasets/final_df.csv')
		y1 = final_df['Loan_Status']
		X1 = final_df.drop(['Loan_Status'], axis = 1)
		X_balance,Y_balance = SMOTE().fit_sample(X1,y1)
		X_balance,Y_balance = SMOTE().fit_sample(X1,y1)
		X_train, X_test, y_train, y_test = train_test_split(X_balance,Y_balance, 
		                                                    stratify=Y_balance, test_size=0.25,
		                                                    random_state = 10086)

		model = RandomForestClassifier(max_depth = 20)
		model.fit(X_train, y_train)

		return model
		
