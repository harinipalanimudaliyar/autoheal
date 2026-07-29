import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer


def cluster_alerts(alerts_list):
  """Clusters raw alert dictionaries using TF-IDF and DBSCAN."""
  if not alerts_list:
    return []

  df = pd.DataFrame(alerts_list)

  # Text vectorization (converts error message strings into TF-IDF math vectors)
  vectorizer = TfidfVectorizer(stop_words="english")
  X = vectorizer.fit_transform(df["message"])

  # DBSCAN Clustering (groups similar text patterns together)
  dbscan = DBSCAN(eps=0.4, min_samples=2, metric="cosine")
  df["cluster_id"] = dbscan.fit_predict(X)

  return df