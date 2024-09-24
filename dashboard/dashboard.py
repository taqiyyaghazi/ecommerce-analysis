import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def create_late_orders_df(df):
    late_orders_df = df[df["is_delivery_late"]]
    late_orders_df = late_orders_df.reset_index()
    return late_orders_df

# Load cleaned data
all_df = pd.read_csv("all_data.csv")

datetime_columns = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    st.image("https://storage.googleapis.com/kaggle-datasets-images/55151/105464/d59245a7014a35a35cc7f7b721de4dae/dataset-cover.png")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

late_orders_df = create_late_orders_df(main_df)

st.header('Olist Ecommerce Dashboard :sparkles:')

col1, col2 = st.columns(2)

with col1:
    total_orders = main_df.shape[0]
    st.metric("Total orders", value=total_orders)

with col2:
    total_late_orders = late_orders_df.shape[0]
    st.metric("Total late orders", value=total_late_orders)

late_counts = main_df['is_delivery_late'].value_counts()

labels = ['On Time', 'Late']
sizes = [late_counts[False], late_counts[True]]

colors = plt.get_cmap('coolwarm')([0.2, 0.8])

fig, ax = plt.subplots(figsize=(8, 6), facecolor='none')
ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', textprops={'color': 'white'})  # Mengatur warna label menjadi putih

st.subheader('Proportion of On-Time vs Late Deliveries')
st.pyplot(fig)


correlations = late_orders_df[['purchase_to_approve_time', 'approve_to_delivered_carrier', 'delivered_carrier_to_delivered_customer', 'delivery_late_time']].corr()

fig, ax = plt.subplots(figsize=(8, 8), facecolor='none')
sns.heatmap(correlations, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, ax=ax)

new_labels = {
    'purchase_to_approve_time': 'Purchase to Approval Time',
    'approve_to_delivered_carrier': 'Approval to Carrier Date',
    'delivered_carrier_to_delivered_customer': 'Carrier to Customer Date',
    'delivery_late_time': 'Delivery Late Time'
}

ax.set_xticklabels([new_labels[label.get_text()] for label in ax.get_xticklabels()], rotation=45, color='white')
ax.set_yticklabels([new_labels[label.get_text()] for label in ax.get_yticklabels()], color='white')

st.subheader('Delivery Time Correlation Heatmap') 
st.pyplot(fig)