"""


"""
# Import required python packages
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker


sns.set()
sns.set_style("white")
sns.despine(left=True, bottom=True)
superstore = pd.read_excel('Superstore.xls')
superstore.sort_values(by=['Order Date'], inplace=True)


# 1
superstore['Discount Amount'] = round(superstore['Sales'] * superstore['Discount'], 4)
fig1, ax1 = plt.subplots()
sns.scatterplot(ax=ax1, x="Discount Amount", y="Profit", data=superstore,
                marker='o', s=80, palette="magma", edgecolor="b", facecolors="none")
plt.setp(ax1, yticks=np.arange(-14000, 30000, 2000))
ax1.yaxis.set_major_formatter(ticker.EngFormatter())
ax1.grid(False)
print("*" * 60, "\n Scatter plot of profit and discount amount.\n")
plt.show()

# 2
fig2, ax2 = plt.subplots()
superstore['NoProfits'] = superstore['Profit'] > 0
sns.scatterplot(legend=False, hue="NoProfits", ax=ax2, x="Discount Amount", y="Profit", data=superstore,
                marker='o', s=80)
plt.setp(ax2, yticks=np.arange(-14000, 30000, 2000))
ax2.yaxis.set_major_formatter(ticker.EngFormatter())
ax2.grid(False)
print("*" * 60, "\n Scatter plot of profit and discount amount grouped by profitability.\n")
plt.show()

# 3
fig3, ax3 = plt.subplots()
superstore['Month of Order Date'] = superstore['Order Date'].dt.strftime('%m/%y')
month_order = superstore.groupby('Month of Order Date').sum()
sns.lineplot(ax=ax3, x=month_order.index.sort_values(), y=month_order["Sales"], markers=True)
# plt.setp(ax,yticks=np.arange(-14000, 30000, 2000))
ax3.yaxis.set_major_formatter(ticker.EngFormatter())
ax3.grid(False)
# Define the date format
#date_form = DateFormatter("%m/%y")
#ax3.xaxis.set_major_formatter(date_form)
ax3.set(xlabel="Month of Order Date", ylabel="Sales",
       title="Sales by Month of Order Date")
print("*" * 60, "\n Sales by order date.\n")
plt.show()

# 4
fig4, ax4 = plt.subplots()
fig5, ax5 = plt.subplots()
superstore['Month of Order Date'] = superstore['Order Date'].dt.strftime('%m/%y')
month_order = superstore.groupby('Month of Order Date').sum()
month_profit = superstore.groupby('Profit').sum()
month_order['NegProfits'] = month_order['Profit'] < 0
month_order['PosProfits'] = month_order['Profit'] > 0

sns.lineplot(ax=ax4, x=month_order.index.sort_values(), y=month_order["Profit"], hue=month_order['NegProfits'], markers=True)
sns.lineplot(ax=ax5, x=month_order.index.sort_values(), y=month_order["Profit"], hue=month_order['PosProfits'], markers=True)
ax4.yaxis.set_major_formatter(ticker.EngFormatter())
ax4.grid(False)
# Define the date format
ax4.set(xlabel="Month of Order Date", ylabel="Sales",
       title="Sales by Month of Order Date")
ax5.set(xlabel="Month of Order Date", ylabel="Sales",
       title="Sales by Month of Order Date")
print("*" * 60, "\n Sales by order date grouped by profitability.\n")
plt.show()

# 5
product_cat = superstore.groupby(['Product Category','Region']).size()
fig5, ax5 = plt.subplots(figsize=(12, 8))
sns.countplot(ax=ax5, x='Region', hue='Product Category', data=superstore)
plt.yticks([])
ax5.grid(False)
ax5.set(xlabel="Region", ylabel="Product Category Count")
print("*" * 60, "\n Percentage of products by region.\n")
plt.show()

# 6
fig6, ax6 = plt.subplots()
sns.scatterplot(ax=ax6, x="Sales", y="Profit", size='Shipping Cost', data=superstore,
                marker='o', s=100)
plt.setp(ax6, yticks=np.arange(-14000, 30000, 2000))
ax6.yaxis.set_major_formatter(ticker.EngFormatter())
ax6.xaxis.set_major_formatter(ticker.EngFormatter())
ax6.grid(False)
print("*" * 60, "\n Relationship between profit, sales, shipping cost.\n")
plt.show()

# 7
fig7, ax7 = plt.subplots()
sns.boxplot(ax=ax7, x="Ship Mode", y="Order Quantity", hue_order='Order Quantity', data=superstore)
ax7.grid(False)
print("*" * 60, "\n Order quantity by shipping mode.\n")
plt.show()
