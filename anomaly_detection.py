import pandas as pd

df = pd.read_csv("support_tickets.csv")

def detect_anomalies():

    anomalies = []

    unresolved = df[
        (df["priority"].isin(["High", "Critical"])) &
        (df["status"] != "Resolved")
    ]

    for _, row in unresolved.iterrows():
        anomalies.append({
            "ticket_id": str(row["ticket_id"]),
            "issue": "Unresolved high-priority ticket"
        })

    df_clean = df.dropna(
        subset=["resolution_time_hrs"]
    )

    threshold = (
        df_clean["resolution_time_hrs"].mean()
        +
        2 * df_clean["resolution_time_hrs"].std()
    )

    long_resolution = df_clean[
        df_clean["resolution_time_hrs"] > threshold
    ]

    for _, row in long_resolution.iterrows():
        anomalies.append({
            "ticket_id": str(row["ticket_id"]),
            "issue": "Abnormally long resolution time"
        })

    return anomalies