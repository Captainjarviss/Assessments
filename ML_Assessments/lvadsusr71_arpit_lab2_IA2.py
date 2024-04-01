# -*- coding: utf-8 -*-
"""LVADSUSR71_Arpit_LAB2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1i6iQ306LW1GXmYjDxg07drK0eMpVJceT
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

customers_data=pd.read_csv("/content/sample_data/Mall_Customers.csv")

customers_data.info()
customers_data.head()

customers_data['Annual Income (k$)'].fillna(customers_data['Annual Income (k$)'].median(), inplace=True)

customers_data.info()

le = LabelEncoder()
customers_data['Gender'] = le.fit_transform(customers_data['Gender'])
customers_data

customers_data['Spending to Income Ratio'] = customers_data['Spending Score (1-100)'] / customers_data['Annual Income (k$)']
customers_data

scaler = StandardScaler()
scaled_features = scaler.fit_transform(customers_data[['Age', 'Annual Income (k$)', 'Spending Score (1-100)', 'Spending to Income Ratio']])

scaled_customers_data = pd.DataFrame(scaled_features, columns=['Age', 'Annual Income', 'Spending Score', 'Spending to Income Ratio'])
scaled_customers_data['Gender'] = customers_data['Gender']
scaled_customers_data.head()

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

wcss = []
silhouette_scores = []
for i in range(2, 11):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(scaled_customers_data)
    wcss.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(scaled_customers_data, kmeans.labels_))

import matplotlib.pyplot as plt

fig, ax1 = plt.subplots()

#used twin plot using subplot and twinx
ax1.set_xlabel('Number of Clusters')
ax1.set_ylabel('WCSS', color='red')
ax1.plot(range(2, 11), wcss, color='red')
ax1.tick_params(axis='y', labelcolor='red')

ax2 = ax1.twinx()
ax2.set_ylabel('Silhouette Score', color='blue')
ax2.plot(range(2, 11), silhouette_scores, color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

fig.tight_layout()
plt.title('Elbow Method vs Silhouette Score for Cluster Number')
plt.show()

kmeans = KMeans(n_clusters=5, random_state=42) #can also take 6 as n_clusters
clusters = kmeans.fit_predict(scaled_customers_data)

scaled_customers_data['Cluster'] = clusters
cluster_analysis = scaled_customers_data.groupby('Cluster').mean()
print(cluster_analysis)

