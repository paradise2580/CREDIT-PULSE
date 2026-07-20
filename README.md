# **Bank Churn Analysis and Prediction using Machine Learning Techniques**

<p align="center">
<img src="./Images/Customer_churn.webp" width="100%">
</p>

# Table of Contents


1. [Project Overview](#project-overview)
2. [Analytics Dashboard (Preview)](#analytics-dashboard-preview)
3. [Contributions](#contributions)
4. [Final Repository Structure](#final-repository-structure)
5. [Bank churn data Overview](#crime-dataset-overview)
6. [Target Audience](#target-audience)
7. [Visualisations](#visualisations)
8. [Launch](#launch)
9. [App Server Setup](#app-server-setup)

## Project Overview
The bank churn prediction project aims to utilize machine learning techniques to predict whether a bank customer is likely to churn (leave) or remain loyal. And also Tableau was utilized for data visualization to analyze patterns and trends within the dataset, providing valuable insights for model training and interpretation.

### The project encompasses several key components:

1. **Data Preparation:** The dataset containing relevant features such as credit score, age, tenure, balance, and more was obtained and cleaned using Python. The cleaned data was then stored in a PostgreSQL database on Neon Cloud services.

2. **Machine Learning Model:** Various machine learning models, including Logistic Regression, Random Forest, XGBoost, and Neural Network, were trained and evaluated using the dataset. Metrics such as accuracy were used to compare the models, and the best-performing model was selected for deployment.

3. **Flask App:** Flask App: A Flask web application was built to provide a user-friendly interface for inputting customer data and obtaining churn predictions, using the selected XGBoost model. Runs locally — see App Server Setup below.

4. **Visualization:** Tableau was utilized for data visualization to analyze patterns and trends within the dataset, providing valuable insights for model training and interpretation.

5. **API Endpoint:** An API endpoint was implemented to allow access to sample data from the Bank Churn database, facilitating further analysis or integration with other systems.

     
### Technologies used

- [Tensorflow](https://www.tensorflow.org/api_docs/python/tf)
- [RandomForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
- [XGBoost](https://xgboost.readthedocs.io/en/stable/)
- [Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)
- [Docker](https://docs.docker.com/)
- [Imblearn](https://imbalanced-learn.org/stable/)
- [Joblib](https://joblib.readthedocs.io/en/stable/)
  
## Analytics Dashboard (Preview)





## Final Repository Structure
```
├── README.md
├── .gitignore
├── .venv
├── 'Images' Folder
└── 'Machine learning Models' Folder
    ├── 'Neural_Networks' Folder
    ├── 'Random_Forest' Folder
    ├── 'Regression' Folder
    └── 'XGBoost' Folder
└── 'static' Folder
    ├── 'css' Folder
    ├── 'data' Folder
    ├── 'img' Folder
    └── 'js' Folder
└── 'templates' Folder
    ├── homepage.html
    ├── index.html
    ├── ml_model.html
    ├── neural_network_model.html
    ├── random_forest_model.html
    ├── regression_model.html
    ├── visualization.html
    └── xgboost.html
├── app.py
├── requirements.txt
└── XGBoost_model

```


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Bank Churn Dataset Overview

- `id`: A unique identifier for each entry.
- `CustomerId`: A unique identifier for each customer.
- `Surname`: The surname of the customer.
- `CreditScore`: The credit score of the customer.
- `Geography`: The geographical location of the customer.
- `Gender`: The gender of the customer.
- `Age`: The age of the customer.
- `Tenure`: Number of years the customer has been with the bank.
- `Balance`: The bank balance of the customer.
- `NumOfProducts`: The number of products the customer has with the bank.
- `HasCrCard`: Indicates if the customer has a credit card (1) or not (0).
- `IsActiveMember`: Indicates if the customer is an active member (1) or not (0).
- `EstimatedSalary`: The estimated salary of the customer.
- `Exited`: Indicates if the customer has exited (1) or not (0).

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Model Performance

Models evaluated on a held-out test set (n=33,007, ~21% churn rate).

| Model | Accuracy | F1 (Churn) | Precision (Churn) | Recall (Churn) |
|---|---|---|---|---|
| Logistic Regression | 0.827 | 0.470 | 0.67 | 0.36 |
| Random Forest | 0.858 | 0.615 | 0.72 | 0.54 |
| **XGBoost (selected)** | **0.866** | **0.640** | 0.75 | 0.56 |
| Neural Network | 0.864 | 0.635 | 0.73 | 0.56 |

XGBoost was selected based on highest accuracy and F1 on the churn class.

### ROC-AUC
XGBoost ROC-AUC: **0.890** — strong separability between churners and non-churners across thresholds.

### Confusion Matrix (XGBoost, threshold = 0.5)
|  | Predicted Retained | Predicted Churned |
|---|---|---|
| **Actual Retained** | 24,685 | 1,338 |
| **Actual Churned** | 3,071 | 3,913 |

At the default threshold, the model correctly flags 3,913 of 6,984 actual churners (56% recall) and misses 3,071 — the tradeoff explored below.

### Feature Importance (XGBoost)
| Feature | Importance |
|---|---|
| NumOfProducts | 0.425 |
| IsActiveMember | 0.175 |
| Age | 0.168 |
| Is_Germany | 0.086 |
| Is_Male | 0.071 |
| Balance | 0.031 |
| HasCrCard | 0.011 |
| CreditScore | 0.008 |
| Tenure | 0.007 |
| Is_Spain | 0.007 |

Number of products held and active-membership status are by far the strongest churn predictors — together accounting for 60% of the model's decision weight, more than demographic or balance features combined.

### Threshold Tuning
| Threshold | Precision | Recall | F1 |
|---|---|---|---|
| 0.3 | 0.620 | 0.713 | 0.663 |
| 0.4 | 0.689 | 0.633 | 0.660 |
| 0.5 (default) | 0.745 | 0.560 | 0.640 |
| 0.6 | 0.792 | 0.469 | 0.589 |
| 0.7 | 0.852 | 0.378 | 0.524 |

Lowering the threshold to 0.3 raises churn recall from 56% to 71% at the cost of more false positives — a tradeoff a bank would tune based on the relative cost of a missed churner vs. an unnecessary retention offer. F1 peaks near threshold 0.3–0.4, suggesting the default 0.5 cutoff is not optimal for this imbalanced problem.



### Notes on class imbalance
The churn class is a minority (~21% of customers), so accuracy alone is misleading — a model predicting "no churn" for everyone would score ~79% accuracy while catching zero at-risk customers. F1 and recall on the churn class are the metrics that matter here. Recall of 0.56 means the current model catches just over half of customers who will actually churn — a real limitation worth stating rather than hiding, and a natural next step (SMOTE, class weighting, or threshold tuning) for future work.
## Target Audience
1. **Banking Institutions:** This project is particularly useful for banking institutions seeking to reduce customer churn rates. Banks can utilize the machine learning model to predict which customers are at risk of leaving. By identifying at-risk customers early, banks can implement targeted retention strategies to retain valuable customers and improve overall customer satisfaction.

2. **Marketing and Customer Retention Teams**: Marketing and customer retention teams within banking institutions can benefit from the insights provided by this project. They can use the predictions generated by the machine learning model to tailor marketing campaigns and retention efforts towards customers identified as likely to churn. This targeted approach can lead to more effective and cost-efficient retention strategies.

3. **Data Analysts and Data Scientists:** Data analysts and data scientists who are interested in predictive analytics and machine learning can also find value in this project. They can explore the dataset, evaluate different machine learning models, and gain insights into feature importance and model performance. Additionally, they can leverage the Flask web application and API endpoint to interact with the machine learning model and explore its predictions.

4. **Business Decision Makers:** Business decision makers, such as executives and managers within banking institutions, can use the insights generated by this project to inform strategic decisions. By understanding customer churn patterns and predicting future churn behavior, decision makers can allocate resources more effectively, prioritize customer retention efforts, and ultimately drive business growth and profitability.


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Visualisation

## Interactive Visualisations
### ** Interactive Tableau Dashboard**
This Tableau Dashboard contains:
1)      An interactive histogram that shows the distribution of account balance of the dataset, as well as an interactive area chart that shows the Churn distribution across age range. The visualisations can be altered by clicking the slicer buttons to filter based on which country the user wants to see distribution for:
<p align="center">
  <img src="./Images/Histogramcountries.gif" width="70%">
</p>
This histogram and area chart can also be filtered based on whether the customer from the dataset ‘churned’ (left the bank), or didn’t churn:
<p align="center">
  <img src="./Images/Histogramexitnonexit.gif" width="70%">
</p>
Additionally, the histogram and area chart can be filtered on whether the customer had a credit card with the bank or not.
<p align="center">
  <img src="./Images/Histogramcc.gif" width="70%">
</p>
Whenever these filters are used, the dashboard updates to show the churn rate of the selected portion of the dataset
 
2)      Interactive bar charts that show the significance of gender, credit card ownership and active membership versus customer loyalty. These bar charts can also be filtered based on the country selected:
<p align="center">
  <img src="./Images/Barchartcountries.gif" width="70%">
</p>
 




---

## Launch

The link to the interactive dashboard is available on the repo's description. 

This repo also contains the necessary files to run the visualization and database locally. Installation is necessary to host the visualization through localhost.


---

## App Server Setup 

+ Add DB Password  
    You need to create dbpassword.txt in the project working directory and paste your database password there.  
    Note: make sure to NOT commit this file to Git.
+ (Once Only) Add New Virtual Environment
    * Open a new terminal and change directory to project working directory
    * Run below command in your project working directory  
      * On macOS and Linux:  
       ``` python3 -m venv .venv```
      * On Windows:   
       ``` python -m venv .venv```
+ Activate the virtual environment  
    * Run below command in your project working directory
      * On macOS and Linux:  
       ``` source .venv/bin/activate```
      * On Windows:   
      ``` .venv\Scripts\activate```
    * Verify Python is correctly configured.
      Run below command, it should shows path to your .venv directory
      ``` which python```  
+ Install Required Python Packages 
    * Run below command in your project working directory  
    ``` pip install -r requirements.txt```
