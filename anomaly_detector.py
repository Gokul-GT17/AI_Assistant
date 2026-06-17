class AnomalyDetector:

    def __init__(self, df):
        self.df = df

    def detect_anomalies(self):

        anomalies = []

        avg = self.df["resolution_time_hrs"].mean()
        std = self.df["resolution_time_hrs"].std()

        threshold = avg + (2 * std)

        long_resolution = self.df[
            self.df["resolution_time_hrs"] > threshold
        ]

        for _, row in long_resolution.iterrows():
            anomalies.append({
                "ticket_id": row["ticket_id"],
                "type": "Long Resolution Time"
            })

        return anomalies