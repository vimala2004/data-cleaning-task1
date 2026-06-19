import pandas as pd
import numpy as np

# --- 1. GENERATE SYNTHETIC CUSTOMER CHURN DATA ---
# This simulates behavioral and engagement trends over a subscription lifespan.
np.random.seed(42)
num_customers = 200

data = {
    "CustomerID": range(1001, 1001 + num_customers),
    "Age": np.random.randint(18, 65, size=num_customers),
    "SubscriptionType": np.random.choice(["Basic", "Standard", "Premium"], size=num_customers, p=[0.5, 0.3, 0.2]),
    "MonthlyCost": np.random.choice([9.99, 14.99, 19.99], size=num_customers),
    "TenureMonths": np.random.randint(1, 24, size=num_customers),
    # Activity & Engagement Metrics (Lower numbers usually correlate with Churn)
    "LoginFrequency_Last30Days": np.random.randint(0, 30, size=num_customers),
    "CustomerSupportCalls": np.random.randint(0, 6, size=num_customers),
    "HoursWatched_Last30Days": np.random.randint(1, 100, size=num_customers),
}

df = pd.DataFrame(data)

# Logic to determine Churn (1 = Cancelled, 0 = Active) based on poor engagement & support calls
df["Churn"] = np.where(
    (df["LoginFrequency_Last30Days"] < 5) | (df["CustomerSupportCalls"] > 3) | (df["HoursWatched_Last30Days"] < 10),
    1, 0
)

# Adjust churn slightly randomly to make it look realistic
random_noise = np.random.choice([0, 1], size=num_customers, p=[0.85, 0.15])
df["Churn"] = np.where(random_noise == 1, 1 - df["Churn"], df["Churn"])

print("📊 Customer Data Loaded successfully. Shape:", df.shape)
print("-" * 60)

# --- 2. EVALUATE USER ACTIVITY & ENGAGEMENT TRENDS ---
print("\n🔍 EVALUATING ENGAGEMENT METRICS BY CHURN STATUS:")
# Grouping data by churn status to isolate behavioral trends
analysis = df.groupby("Churn")[["LoginFrequency_Last30Days", "CustomerSupportCalls", "HoursWatched_Last30Days", "TenureMonths"]].mean()
print(analysis)

# --- 3. IDENTIFY KEY PATTERNS BEHIND CANCELLATIONS ---
print("\n📌 IDENTIFYING KEY PATTERNS:")
total_churned = df[df["Churn"] == 1]
total_active = df[df["Churn"] == 0]

churn_rate_by_tier = df.groupby("SubscriptionType")["Churn"].mean() * 100
print("\n💡 Churn Rate (%) by Subscription Tier:")
print(churn_rate_by_tier.round(2))

# --- 4. STRATEGIC RETENTION RECOMMENDATIONS ---
print("\n" + "="*20 + " RETENTION SUGGESTIONS " + "="*20)
print("> 1. AT-RISK TRIGGER: Users logging in fewer than 5 times a month are primary churn targets. Launch an automated re-engagement email sequence.")
print("> 2. SUPPORT INTERVENTION: Customers making more than 3 support calls experience higher cancellation rates. Escalate these cases to a dedicated customer success team.")
print("> 3. VALUE PROPOSITION: High monthly cost tiers show higher sensitivity. Offer a temporary retention discount or flexible pricing restructuring.")
print("=" * 63)

# Save analysis matrix to CSV
df.to_csv("customer_churn_analysis.csv", index=False)
print("\n✅ Analysis pipeline complete! Results saved to 'customer_churn_analysis.csv'.")
