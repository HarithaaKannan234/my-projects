ML Project 

Overview

    This project aimed to build a machine learning model to predict
    whether a patient will be readmitted to the hospital using Python,
    Jupyter Notebooks, and Excel. The dataset consisted of various features 
    including patient ID, age, gender, admission type, diagnosis, number of lab 
    procedures, number of medications, number of outpatient visits, number of 
    inpatient visits, number of emergency visits, number of diagnoses, A1C result, and readmission status.

Project Steps

Data Cleaning:

    The initial step involved cleaning the dataset, handling missing values,
    and ensuring data consistency.

Exploratory Data Analysis (EDA):

    EDA was performed to gain insights into the dataset's distribution, correlations, 
    and trends. Visualizations and statistical summaries were utilized to understand the data better.

Model Building:
    
    A Decision Tree Classifier was chosen as the predictive model due to its interpretability 
    and ability to handle categorical data. The model was trained using the cleaned dataset.

Model Evaluation:

Train F1 Score: 0.692

Train Precision Score: 0.762

Train Recall Score: 0.634

Train ROC_AUC Score: 0.834

Test Accuracy Score: 0.520

Files

Conclusion:

    Although the Decision Tree Classifier achieved decent performance on the training set, 
    its performance on the test set indicates potential overfitting. Further optimization 
    and exploration of different models could improve predictive accuracy. Additionally, 
    gathering more data or refining feature engineering might enhance model performance.






