from datetime import datetime
from database import Alert, Incident, SessionLocal, init_db
from engine import cluster_alerts
from fastapi import FastAPI, HTTPException
from llm_service import diagnose_incident
from pydantic import BaseModel

app = FastAPI(title="AutoHeal API", version="1.0")

# Initialize DB on startup
init_db()


class AlertSchema(BaseModel):
  source: str
  message: str


@app.post("/ingest")
def ingest_alert(alert: AlertSchema):
  """Receives an individual alert and stores it in SQLite."""
  db = SessionLocal()
  db_alert = Alert(
      timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      source=alert.source,
      message=alert.message,
      status="Unprocessed",
  )
  db.add(db_alert)
  db.commit()
  db.refresh(db_alert)
  db.close()
  return {"status": "success", "alert_id": db_alert.id}


@app.post("/process-alerts")
def process_alerts():
  """Pulls unprocessed alerts, clusters them via ML, and diagnoses via LLM."""
  db = SessionLocal()
  alerts = db.query(Alert).filter(Alert.status == "Unprocessed").all()

  if not alerts:
    db.close()
    return {"message": "No new alerts to process."}

  # Format alerts for the engine
  alerts_data = [{
      "id": a.id,
      "source": a.source,
      "message": a.message,
      "timestamp": a.timestamp,
  } for a in alerts]

  # Run Clustering Engine
  clustered_df = cluster_alerts(alerts_data)

  incidents_created = 0
  for cluster_id, group in clustered_df.groupby("cluster_id"):
    messages = group["message"].tolist()

    # Call LLM Service for diagnosis
    diagnosis = diagnose_incident(messages)

    # Save Incident
    incident = Incident(
        cluster_id=int(cluster_id),
        root_cause=diagnosis["root_cause"],
        risk_level=diagnosis["risk_level"],
        remediation_status="Pending",
    )
    db.add(incident)
    incidents_created += 1

  # Mark alerts as processed
  for a in alerts:
    a.status = "Processed"

  db.commit()
  db.close()

  return {
      "status": "success",
      "alerts_processed": len(alerts),
      "incidents_created": incidents_created,
  }


@app.get("/incidents")
def get_incidents():
  """Retrieves all diagnosed incidents for the dashboard."""
  db = SessionLocal()
  incidents = db.query(Incident).all()
  db.close()
  return incidents