import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, shutil

if os.path.exists('./extract'):
   shutil.rmtree('./extract')

os.makedirs('./extract')

df1 = pd.read_excel('Assignment2\Assiggnment2\OrderData.xlsx')
df2 = pd.read_excel('Assignment2\Assiggnment2\Restaurant.xlsx')
df3 = df1.merge(df2, how='inner', on='Restaurant ID')

# Data Cleaning
df3.drop_duplicates(inplace = True)
df3 = df3.sort_values(by=['Order ID'])

# 1.Detailed Cost Analysis:

# Profitability Evaluation
df3['Profit'] = df3['Commission Fee'] - df3[['Delivery Fee', 'Payment Processing Fee', 'Refunds/Chargebacks']].sum(axis = 1)
df3['cost_per_order'] = df3[['Delivery Fee', 'Payment Processing Fee', 'Refunds/Chargebacks']].sum(axis = 1)
total_Expenses = sum(df3['cost_per_order'])
Total_Profitability = sum(df3['Commission Fee'] - df3[['Delivery Fee', 'Payment Processing Fee', 'Refunds/Chargebacks']].sum(axis = 1))
# print(Total_Profitability)      #40238

# Total Customers
customer_count = len(pd.unique(df3['Customer ID']))
print(customer_count)           #947

# Total Revenue Generated
# Hint :- profit-> Commision Fee- (Delivery Fee +Payment Processing Fee+Refunds/Chargebacks)

Total_Revenue_Generated = sum(df3[['Commission Fee', 'Delivery Fee', 'Payment Processing Fee', 'Refunds/Chargebacks']].sum(axis = 1))
print(Total_Revenue_Generated) #213742

# Total Commission
Total_Commission = df3['Commission Fee'].sum()
# print(Total_Commission)         #126990

# High Level Summary Data
high_level_summary_data = pd.DataFrame([{'customer_count' : customer_count, 'Total_Revenue_Generated' : Total_Revenue_Generated, 'Total_Commission' : Total_Commission, 'Total Expense' : total_Expenses, 'Total Profit' : Total_Profitability}])
print(high_level_summary_data)
high_level_summary_data.to_excel('./extract/high_level_summary_data.xlsx', index=False)
print('high_level_summary_data loaded to excel')

# Delivery Time/calendar month/week
df3['Delivery Time'] = (df3['Delivery Date and Time'] - df3['Order Date and Time'])
df3['Delivery Time (In hours)'] = (df3['Delivery Date and Time'] - df3['Order Date and Time']) / pd.Timedelta(hours=1)
df3.insert(3, 'Month', df3['Order Date and Time'].dt.month_name())
df3.insert(4, 'Week', df3['Order Date and Time'].dt.isocalendar().week)
print(df3.head(7))
df3 = df3.reset_index(drop=True)
df3 = df3.sort_values(by=['Order ID'])

#Data Loading
df3.to_excel('./extract/merged_dataset.xlsx', index=False)
print('merged_dataset loaded to excel')

# City with corresponding order count and revenue generated 
df4 = df3.groupby(['Location']).agg({'Order ID' : 'size', 'Delivery Time' : 'mean', 'Delivery Time (In hours)' : 'mean', 'Commission Fee' : 'sum', 'Profit' : 'sum'})
df4['Delivery Time'] = df4['Delivery Time'].round('1s')
df4.rename(columns={"Order ID": "Order Count", 'Delivery Time' : 'Avg Delivery Time', 'Delivery Time (In hours)' : 'Avg Delivery Time (In Hrs)', "Commission Fee": "Revenue Generated"}, inplace=True)
df4.reset_index(inplace=True)
print(df4)
df4.to_excel('./extract/City with corresponding order count and revenue generated.xlsx', index=False)
print('City with corresponding order count and revenue generated data loaded')


# Revenue/commision trend on monthly basis\

df5 = df3.groupby(['Month']).agg({'Commission Fee' : 'sum'})
df5.rename(columns={'Commission Fee' : 'Revenue'}, inplace=True)
df5.reset_index(inplace=True)
df5=df5.iloc[::-1]
print(df5)
df5.to_excel('./extract/commision trend on monthly basis.xlsx', index=False)
print('commision trend on monthly basis data loaded')

# Most/least profitable resturant
df6 = df3.groupby(['Restaurant ID']).agg({'Profit' : 'sum', 'Delivery Time' : 'mean', 'Customer ID' : 'size'})

most_profitable_restaurant = df6[df6['Profit'] == max(df6['Profit'])]
least_profitable_restaurant = df6[df6['Profit'] == min(df6['Profit'])]
profitable_restaurant_overview = pd.concat([most_profitable_restaurant,least_profitable_restaurant])
profitable_restaurant_overview.rename(columns={'Customer ID' : 'Customer Count', 'Delivery Time' : 'Avg Delivery Time'}, inplace=True)
profitable_restaurant_overview.reset_index(inplace=True)
print(profitable_restaurant_overview)
profitable_restaurant_overview.to_excel('./extract/profitable_restaurant_overview.xlsx', index=False)
print('profitable_restaurant_overview data loaded')


# Most popular & most profitable discount offer

utilization_count_discount_offer = df3.groupby(['Discounts and Offers']).agg({'Discounts and Offers' : 'size', 'Profit' : 'sum'})
utilization_count_discount_offer.rename(columns={'Discounts and Offers' : 'Discounts and Offers', 'Discounts and Offers' : 'Applied'}, inplace=True)

utilization_count_discount_offer['Popular Discount Offer'] = np.where(utilization_count_discount_offer['Applied'] == max(utilization_count_discount_offer['Applied']), 'Most Popular','')
utilization_count_discount_offer['Profitable Discount Offer'] = np.where(utilization_count_discount_offer['Profit'] == max(utilization_count_discount_offer['Profit']), 'Most profitable', '')
utilization_count_discount_offer.reset_index(inplace=True)
print(utilization_count_discount_offer)
# Discounts and Offers    Applied  Profit Popular Discount Offer Profitable Discount Offer

# 0.1                       233   10460           Most Popular           Most profitable
# 15% New User              198    7118
# 5% on App                 183    8159
# 50 off Promo              201    8527
with pd.ExcelWriter("./extract/discount_offer_analysis.xlsx", engine="openpyxl") as writer:
    utilization_count_discount_offer.to_excel(writer, sheet_name="discount_offer_analysis", startrow=0 , startcol=0, index=True)   
    print('Most popular & most profitable discount offer Data Loaded To Excel') 

# Most/least profitable discount offer resturant wise
restaurant_discount_offer_analysis = df3.groupby(['Restaurant ID','Discounts and Offers']).agg({'Discounts and Offers' : 'size', 'Profit' : 'sum'}).sort_values(by=['Restaurant ID'])
restaurant_discount_offer_analysis.rename(columns={'Discounts and Offers' : 'Count of Discounts and Offers Used'}, inplace = True)

restaurant_discount_offer_analysis2 = restaurant_discount_offer_analysis.groupby(['Restaurant ID']).agg({'Profit' : 'max'})
restaurant_discount_offer_analysis2['Min Profit'] = restaurant_discount_offer_analysis.groupby(['Restaurant ID']).agg({'Profit' : 'min'})
restaurant_discount_offer_analysis2.reset_index(inplace = True)
print(restaurant_discount_offer_analysis2)

restaurant_discount_offer_analysis.reset_index(inplace=True)

check = restaurant_discount_offer_analysis.groupby(['Restaurant ID'])
datafrm_ = pd.DataFrame()
datafrm = pd.DataFrame(columns = ['Restaurant ID','Most Profitable Discount and Offers', 'Least Profitable Discount and Offers'])
print(datafrm)
for rec, rec_data in check:
    max_ = rec_data['Profit'].max()
    min_ = rec_data['Profit'].min()
    datafrm['Restaurant ID'] = rec
    for i,k in rec_data['Profit'].items():
        if k == max_:
            max_pro = rec_data.loc[((rec_data['Profit'] == k) & (rec_data['Restaurant ID'] == rec[0]))]['Discounts and Offers']
            datafrm['Most Profitable Discount and Offers'] = max_pro.values[0]
        elif k == min_:
            max_pro = rec_data.loc[((rec_data['Profit'] == k) & (rec_data['Restaurant ID'] == rec[0]))]['Discounts and Offers']
            datafrm['Least Profitable Discount and Offers'] = max_pro.values[0]

    datafrm_ = datafrm_._append(datafrm, ignore_index=True)

print(datafrm_)
with pd.ExcelWriter("./extract/restaurant_discount_offer_analysis.xlsx", engine="openpyxl") as writer:
    restaurant_discount_offer_analysis.to_excel(writer, sheet_name = "restaurant_disc_offers_analysis", startrow=0 , startcol=0, index=False)
    datafrm_.to_excel(writer, sheet_name = "Most-Least", startrow=0 , startcol=0, index=False)   
    print('restaurant_discount_offer_analysis Data Inserted To Excel') 

# Popular payment method resturant wise
popular_payment_method = df3.groupby(['Restaurant ID', 'Payment Method']).agg({'Payment Method' : 'size'})
popular_payment_method.rename(columns={'Payment Method' : 'payment_method_count'}, inplace=True)
popular_payment_method.reset_index(inplace=True)
print(popular_payment_method)

check_ = popular_payment_method.groupby(['Restaurant ID'])
datafrmm_, datafrmm = pd.DataFrame(), pd.DataFrame()
for rec, rec_data in check_:
    max_ = rec_data['payment_method_count'].max()
    datafrmm['Restaurant ID'] = rec
    for i,k in rec_data['payment_method_count'].items():
        if k == max_:
            max_pro = rec_data.loc[((rec_data['payment_method_count'] == k) & (rec_data['Restaurant ID'] == rec[0]))]['Payment Method']
            datafrmm['Popular payment method'] = max_pro.values[0]

    datafrmm_ = datafrmm_._append(datafrmm, ignore_index=True)

print(datafrmm_)
with pd.ExcelWriter("./extract/popular_payment_method.xlsx", engine="openpyxl") as writer:
    popular_payment_method.to_excel(writer, sheet_name = "payment_method_count", startrow=0 , startcol=0, index=False)
    datafrmm_.to_excel(writer, sheet_name = "popular_payment_method", startrow=0 , startcol=0, index=False)   
    print('popular_payment_method Data Inserted To Excel') 


# Time variant analysis on the order..like avg cost , no of orders per month, week.
avg_cost_per_month = df3.groupby(['Month']).agg({'cost_per_order' : 'mean', 'Order ID' : 'size'})
avg_cost_per_month.rename(columns={'cost_per_order' : 'Avg cost/month', 'Order ID' : 'Total orders/month'}, inplace=True)
avg_cost_per_month=avg_cost_per_month.iloc[::-1]
avg_cost_per_month.reset_index(inplace=True)
print(avg_cost_per_month)

avg_cost_per_week = df3.groupby(['Week']).agg({'cost_per_order' : 'mean', 'Order ID' : 'size'})
avg_cost_per_week.rename(columns={'cost_per_order' : 'Avg cost/week', 'Order ID' : 'Total orders/week'}, inplace=True)
avg_cost_per_week.reset_index(inplace=True)
print(avg_cost_per_week)

with pd.ExcelWriter("./extract/Time variant analysis on the order.xlsx", engine="openpyxl") as writer:
    avg_cost_per_month.to_excel(writer, sheet_name = "Time variant analysis", startrow=0 , startcol=0, index=False)
    avg_cost_per_week.to_excel(writer, sheet_name = "Time variant analysis", startrow=5 , startcol=0, index=False)   
    print('Time variant analysis on the order Data Inserted To Excel') 

ax = avg_cost_per_month.plot(x="Month", y="Avg cost/month", kind="bar", color=['pink'], title='Average Cost Per Month', grid = False)
for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))

# plt.show()
# avg_cost_per_month.plot(x="Month", y="Avg cost/month", kind="bar", title='Average Cost Per Month')
# plt.savefig('myfile.png', bbox_inches='tight')
# # avg_cost_per_month.plot(x="Week", y="Avg cost/week", kind="bar") 
