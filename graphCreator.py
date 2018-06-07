import matplotlib.pyplot as plt
import pandas as pd
import seaborn.apionly as sns


# Normal graph
data = pd.read_csv("mas_taxi_delivery_data1_runtime10000000.csv.csv", index_col = False)

# if there are configurations with same parameters keeping only the mean
data = data.groupby(['runTime', 'commRange', 'commReliability', 'numTaxis', 'numCustomers', 'newCustomerProb', 'seeRange', 'lazyProb'], as_index=False).mean()

data.plot(loglog=True, x='commRange', y='passengersDelivered')
data.to_csv('test.csv')
plt.show()

# Graph with two lines
data = pd.read_csv("mas_taxi_delivery_data3_runtime10000000.csv.csv", index_col = False)
ax = plt.gca()

# if there are configurations with same parameters keeping only the mean
data = data.groupby(['runTime', 'commRange', 'commReliability', 'numTaxis', 'numCustomers', 'newCustomerProb', 'seeRange', 'lazyProb'], as_index=False).mean()

# plot two lines with and without communication
data[data['commRange'] > 100].plot(loglog=True, x='seeRange', y='passengersDelivered', ax=ax)
data[data['commRange'] <= 100].plot(loglog=True, x='seeRange', y='passengersDelivered', ax=ax)
ax.legend(['data[\'commRange\'] > 100', 'data[\'commRange\'] <= 100'])
plt.show()

# Heatmap
data = pd.read_csv("mas_taxi_delivery_data3_runtime10000000.csv.csv", index_col = False)

# if there are configurations with same parameters keeping only the mean
data = data.groupby(['runTime', 'commRange', 'commReliability', 'numTaxis', 'numCustomers', 'newCustomerProb', 'seeRange', 'lazyProb'], as_index=False).mean()

piv = pd.pivot_table(data, values="passengersDelivered",index=["commRange"], columns=["seeRange"], fill_value=0)
ax = sns.heatmap(piv, square=True)
plt.setp( ax.xaxis.get_majorticklabels(), rotation=90 )
plt.tight_layout()
plt.show()
