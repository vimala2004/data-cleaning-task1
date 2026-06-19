import pandas as pd
import numpy as np

# --- 1. GENERATE SYNTHETIC WEB TRAFFIC LOGS ---
np.random.seed(42)
num_sessions = 500

# Simulating standard user journeys: Home -> Pricing -> Checkout -> Confirmation
stages = ["Home", "Pricing", "Checkout", "Confirmation"]

data = {
    "SessionID": [f"SESS_{1000 + i}" for i in range(num_sessions)],
    "Device": np.random.choice(["Desktop", "Mobile", "Tablet"], size=num_sessions, p=[0.5, 0.4, 0.1]),
    "Source": np.random.choice(["Organic Search", "Direct", "Paid Ads", "Social Media"], size=num_sessions),
    "PageViews": np.random.randint(1, 12, size=num_sessions),
    "SessionDuration_Sec": np.random.randint(10, 600, size=num_sessions),
}

df = pd.DataFrame(data)

# Simulate user progression through the funnel (Drop-off analysis)
# Every user hits Home, but fewer make it to subsequent steps
df["Reached_Home"] = True
df["Reached_Pricing"] = np.random.choice([True, False], size=num_sessions, p=[0.75, 0.25])
df["Reached_Checkout"] = np.where(df["Reached_Pricing"], np.random.choice([True, False], size=num_sessions, p=[0.40, 0.60]), False)
df["Reached_Confirmation"] = np.where(df["Reached_Checkout"], np.random.choice([True, False], size=num_sessions, p=[0.65, 0.35]), False)

print("🚀 Web Traffic Log Loaded. Total Sessions Tracked:", len(df))
print("-" * 65)

# --- 2. KEY PERFORMANCE METRICS ---
print("\n📊 1. OVERALL TRAFFIC METRICS:")
print(f"• Total Page Views: {df['PageViews'].sum()}")
print(f"• Average Page Views per Session: {df['PageViews'].mean().round(2)}")
print(f"• Average Session Duration: {df['SessionDuration_Sec'].mean().round(2)} seconds")

# --- 3. ACQUISITION LAYER (Traffic Sources) ---
print("\n🌐 2. ACQUISITION BY SOURCE (Avg Engagement):")
source_analysis = df.groupby("Source")[["PageViews", "SessionDuration_Sec"]].mean().round(2)
print(source_analysis)

# --- 4. FUNNEL EXPLORATION & DROP-OFF POINTS (As seen in GA4 Funnel Reports) ---
print("\n📉 3. FUNNEL CONVERSION & DROP-OFF POINTS:")
total_users = len(df)
home_users = df["Reached_Home"].sum()
pricing_users = df["Reached_Pricing"].sum()
checkout_users = df["Reached_Checkout"].sum()
confirmation_users = df["Reached_Confirmation"].sum()

funnel_stages = ["1. Home", "2. Pricing", "3. Checkout", "4. Purchase Confirmation"]
user_counts = [home_users, pricing_users, checkout_users, confirmation_users]

for i in range(len(funnel_stages)):
    pct_of_total = (user_counts[i] / total_users) * 100
    dropoff = ""
    if i > 0:
        drop_rate = ((user_counts[i-1] - user_counts[i]) / user_counts[i-1]) * 100
        dropoff = f" | Drop-off from previous step: {drop_rate:.1f}%"
    print(f"  {funnel_stages[i]}: {user_counts[i]} users ({pct_of_total:.1f}% of traffic){dropoff}")

# --- 5. DATA INSIGHTS & ENGAGEMENT SOLUTIONS ---
print("\n" + "="*21 + " OPTIMIZATION INSIGHTS " + "="*21)
print("> CRITICAL DROP-OFF: The largest leakage occurs between 'Pricing' and 'Checkout'.")
print("  Action: Simplify the pricing tier breakdown and inject prominent Trust Badges/FAQs.")
print("> CHANNEL PERFORMANCE: Analyze sources with high bounce rates / low page views.")
print("  Action: Optimize landing page relevance for underperforming Paid or Social ads.")
print("=" * 65)

# Export analytics table
df.to_csv("web_traffic_analysis.csv", index=False)
print("\n✅ Analytics pipeline complete! Results exported to 'web_traffic_analysis.csv'.")
