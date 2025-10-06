import mysql.connector
import pandas as pd
import streamlit as st
import altair as alt 

try:
    conn = mysql.connector.connect(
        host=st.secrets["connections"]["mysql"]["host"],
        user=st.secrets["connections"]["mysql"]["username"],
        password=st.secrets["connections"]["mysql"]["password"],
        database=st.secrets["connections"]["mysql"]["database"]
    )
    
    if conn.is_connected():
        st.success("Database connection successful!")
        
except Exception as e:
    st.error(f"Error connecting to database: {e}")
    st.stop()


st.set_page_config(
    page_title="SaaS KPI Dashboard",
    layout="wide"
)
st.title("SaaS KPI Dashboard 📊")
st.markdown("---") 

#  MRR
query1 = """
SELECT 
    SUM(AMOUNT) AS CURRENT_MRR
FROM 
    SAAS_TRANSACTIONS
WHERE
    DATE_FORMAT(BILLING_DATE, '%Y-%m') = (
    SELECT 
        DATE_FORMAT(MAX(BILLING_DATE), '%Y-%m') 
    FROM 
        SAAS_TRANSACTIONS);
"""
query2 = """
SELECT 
    SUM(AMOUNT) AS CURRENT_MRR
FROM 
    SAAS_TRANSACTIONS
WHERE 
    DATE_FORMAT(BILLING_DATE, '%Y-%m') = (
    SELECT 
         DATE_FORMAT(MAX(BILLING_DATE) - INTERVAL 1 MONTH, '%Y-%m') 
    FROM 
        SAAS_TRANSACTIONS);
"""
cursor = conn.cursor() 
cursor.execute(query1)
result = cursor.fetchone()
current_mrr = result[0] 
cursor.execute(query2)
result = cursor.fetchone()
prev_mrr = result[0]      

#Calculating Change
mrr_delta = current_mrr - prev_mrr
delta_string = "N/A"
if(prev_mrr > 0):
    mrr_delta_percent = (mrr_delta/prev_mrr) * 100
    delta_string = f"${mrr_delta:,.0f} ({mrr_delta_percent:+.1f}%)"
elif current_mrr > 0:
    delta_string = "New Revenue" 
    
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Current Month MRR", 
              value=f"${current_mrr:,.0f}",
              delta=delta_string)

# Line Plot

# Finding all Years
query3 = """
SELECT
    DISTINCT DATE_FORMAT(BILLING_DATE, '%Y') as YEARS  
FROM
    SAAS_TRANSACTIONS
ORDER BY YEARS DESC
"""

cursor = conn.cursor() 
cursor.execute(query3)
result = cursor.fetchall()
print(result)
cursor.close()         
years_list = [i[0] for i in result]


st.subheader("MRR Trend Over Time 📈")
filter_col, _ = st.columns([1, 4]) 
with filter_col:
        selected_year = st.selectbox(
        "Select Year to View:",
        options = years_list
    )

# Months for the selected year
query4 = f"""
SELECT  DATE_FORMAT(BILLING_DATE, '%Y-%m') as MONTH,
        SUM(AMOUNT) AS total_mrr 
FROM 
        SAAS_TRANSACTIONS
WHERE 
        DATE_FORMAT(BILLING_DATE, '%Y') = '{selected_year}'
GROUP BY MONTH
ORDER BY MONTH
"""

cursor = conn.cursor() 
cursor.execute(query4)
month = cursor.fetchall()
print(result)
cursor.close() 

#plotting
col_names = ["Month", "MRR"]
df_mrr = pd.DataFrame(month, columns=col_names)
df_mrr['MRR'] = pd.to_numeric(df_mrr['MRR'])
df_mrr['Sort_Key'] = pd.to_datetime(df_mrr["Month"])
df_mrr['Month'] = df_mrr['Sort_Key'].dt.strftime('%B %Y') 
df_mrr = df_mrr.sort_values(by='Sort_Key')

chart = alt.Chart(df_mrr).mark_line().encode(
    x=alt.X('Month', sort=None, axis=alt.Axis(
        labelAngle=0,
        title='Month'
    )),
    y='MRR',
    tooltip=['Month', 'MRR']
).properties(
    width='container'
)

st.altair_chart(chart, use_container_width=True)


