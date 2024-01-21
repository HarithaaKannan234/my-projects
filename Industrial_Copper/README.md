
Industrial Copper Modeling
Introduction
Enhance your expertise in data analysis and machine learning with our "Industrial Copper Modeling" project. Tackling complex sales and pricing data challenges in the copper industry, this solution utilizes advanced machine learning techniques to provide regression models for accurate pricing predictions and lead classification for improved customer targeting. Gain hands-on experience in data preprocessing, feature engineering, and web application development using Streamlit, empowering you to address real-world problems in manufacturing.

Table of Contents
Key Technologies and Skills
Installation
Features
Key Technologies and Skills
Python
Numpy
Pandas
Scikit-Learn
Matplotlib
Seaborn
Pickle
Streamlit
Installation
To run this project, install the required packages:

bash
Copy code
pip install numpy
pip install pandas
pip install scikit-learn
pip install xgboost
pip install matplotlib
pip install seaborn
pip install streamlit
Usage
Data Preprocessing
Data Understanding
Before modeling, understand the dataset, identify variable types, and examine distributions. Handle unwanted values, like '00000.' in 'Material_Ref,' by converting them to null for better data integrity.

Handling Null Values
Address missing values based on data nature and feature importance, using mean, median, or mode imputation.

Encoding and Data Type Conversion
Prepare categorical features with ordinal encoding and ensure data types match modeling requirements.

Skewness - Feature Scaling
Mitigate skewness using log transformation for balanced and normally-distributed datasets.

Outliers Handling
Use Interquartile Range (IQR) to handle outliers for a more robust model.

Wrong Date Handling
Resolve delivery dates preceding item dates by calculating the difference and training a Random Forest Regressor for correction.

Exploratory Data Analysis (EDA) and Feature Engineering
Skewness Visualization
Visualize and correct skewness in continuous variables using Seaborn's Histplot and Violinplot.

Outlier Visualization
Identify and rectify outliers using Seaborn's Boxplot.

Feature Improvement
Create new features for deeper insights without dropping columns, ensuring data quality.

Classification
Success and Failure Classification
Use 'status' variable to classify 'Won' as Success and 'Lost' as Failure. Exclude other status values.

Handling Data Imbalance
Implement SMOTETomek oversampling method to address data imbalance for more accurate classification.

Algorithm Assessment
Divide dataset into training and testing subsets and assess various algorithms for classification.

Algorithm Selection
Select Random Forest Classifier for balanced interpretability and accuracy.

Hyperparameter Tuning with GridSearchCV and Cross-Validation
Fine-tune the model with GridSearchCV and cross-validation for optimal hyperparameters.

Model Accuracy and Metrics
Evaluate model accuracy, confusion matrix, precision, recall, F1-score, AUC, and ROC curve.

Model Persistence
Save the trained model to a pickle file for future predictions.

Regression
Algorithm Assessment
Split dataset and evaluate various regression algorithms based on R2 metric.

Algorithm Selection
Select Random Forest Regressor for balanced interpretability and accuracy.

Hyperparameter Tuning with GridSearchCV and Cross-Validation
Fine-tune the model with GridSearchCV and cross-validation for optimal hyperparameters.

Model Accuracy and Metrics
Evaluate model accuracy, mean absolute error, mean squared error, root mean squared error, and R-squared.

Model Persistence
Save the trained model to a pickle file for future predictions on selling prices.
