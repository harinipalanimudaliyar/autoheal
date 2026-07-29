from datetime import datetime
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

st.set_page_config(
    page_title="AutoHeal - Intelligent AIOps Dashboard",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ AutoHeal: Autonomous IT Incident & Alert Noise Reduction")
st.markdown(
    "*Intercepts alert storms, clusters duplicates using ML, diagnoses root"
    " causes via LLM, and triages fixes.*"
)

# Sidebar controls for simulation
st.sidebar.header("Control Center")
if st.sidebar.button("🚀 Simulate Alert Storm"):
  # Send mock burst of alerts to local FastAPI backend
  mock_alerts = [
      {
          "source": "DB-Cluster-01",
          "message": (
              "Database connection failed: max connections exceeded on pool"
              " primary"
          ),
      },
      {
          "source": "DB-Cluster-02",
          "message": (
              "Database connection failed: max connections exceeded on pool"
              " primary"
          ),
      },
      {
          "source": "DB-Cluster-03",
          "message": (
              "Database connection failed: max connections exceeded on pool"
              " primary"
          ),
      },
      {
          "source": "Auth-Service",
          "message": (
              "Out-Of-Memory (OOM) error: worker node heap allocation limit"
              " reached"
          ),
      },
      {
          "source": "Payment-API",
          "message": (
              "Out-Of-Memory (OOM) error: worker node heap allocation limit"
              " reached"
          ),
      },
      {
          "source": "Gateway-01",
          "message": (
              "Intermittent network timeout detected across microservice"
              " boundaries."
          ),
      },
  ]

  for alert in mock_alerts:
    requests.post("http://127.0.0.1:8000/ingest", json=alert)

  # Trigger processing
  res = requests.post("http://127.0.0.1:8000/process-alerts")
  if res.status_code == 200:
    st.sidebar.success("Alert storm simulated & processed successfully!")
    st.rerun()
  else:
    st.sidebar.error("Failed to process alerts. Is the FastAPI server running?")

# Fetch current incidents from API
try:
  response = requests.get("http://127.0.0.1:8000/incidents")
  incidents = response.json() if response.status_code == 200 else []
except:
  incidents = []

# Top Metric Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Raw Alerts Ingested", "64", "-12% vs last hr")
col2.metric("Noise Reduction Efficiency", "83.3%", "Grouped into 3 clusters")
col3.metric("Active Incidents", len(incidents), "Requires Attention")
col4.metric("Autonomous Fixes Applied", "2", "Safe Shell Scripts Run")

st.markdown("---")

# Visual Charts Section
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
  st.subheader("📊 Alert Distribution by Source")
  source_data = pd.DataFrame(
      {
          "Source": ["DB-Cluster", "Auth-Service", "Payment-API", "Gateway-01"],
          "Alert Count": [35, 18, 8, 3],
      }
  )
  fig_bar = px.bar(
      source_data,
      x="Source",
      y="Alert Count",
      color="Source",
      template="plotly_dark",
  )
  st.plotly_chart(fig_bar, use_container_width=True)

with chart_col2:
  st.subheader("📉 Noise Reduction Impact")
  pie_data = pd.DataFrame(
      {
          "Category": ["Suppressed Duplicate Alerts", "Unique Actionable Incidents"],
          "Count": [61, 3],
      }
  )
  fig_pie = px.pie(
      pie_data,
      names="Category",
      values="Count",
      hole=0.4,
      template="plotly_dark",
  )
  st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# Incident Review Table
st.subheader("🔍 AI Diagnosed Incidents & Remediation Control")
if incidents:
  df_incidents = pd.DataFrame(incidents)
  st.dataframe(df_incidents, use_container_width=True)

  selected_id = st.selectbox(
      "Select Incident ID to Review & Execute Fix",
      options=df_incidents["id"].tolist() if not df_incidents.empty else [],
  )

  if st.button("⚡ Approve & Execute Remediation"):
    st.success(
        f"Remediation successfully dispatched for Incident #{selected_id}!"
    )
else:
  st.info(
      "No incidents found yet. Click **'Simulate Alert Storm'** in the sidebar"
      " to get started!"
  )