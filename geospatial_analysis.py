import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point

print("🌍 Initializing Geospatial Expansion Analysis...")
print("-" * 65)

# --- 1. GENERATE LOCATION-BASED DEMAND & SALES DATA ---
# Simulating regional cities with coordinate boundaries (Latitude and Longitude)
np.random.seed(42)
num_locations = 100

data = {
    "LocationID": [f"LOC_{1000 + i}" for i in range(num_locations)],
    "Latitude": np.random.uniform(34.0, 36.0, size=num_locations),
    "Longitude": np.random.uniform(-118.5, -116.5, size=num_locations),
    # Demand Index scale 1-100 (Based on search traffic / population density)
    "DemandIndex": np.random.randint(20, 100, size=num_locations),
    # Existing Store Presence (Number of operating competitors or internal branches)
    "ExistingStores": np.random.choice([0, 1, 2, 3], size=num_locations, p=[0.6, 0.2, 0.1, 0.1])
}

df = pd.DataFrame(data)

# --- 2. CONVERT TO GEOPANDAS DATAFRAME (Vector Point Data) ---
# Transforming coordinates into spatial geometries as explained in the video
geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

print(f"✅ Successfully converted raw coordinates into vector spatial points.")
print(f"📍 Total regional coordinates indexed: {len(gdf)}")

# --- 3. SPATIAL RELATIONSHIP & EXPANSION CRITERIA ---
# Goal: Find high demand (Demand > 70) but ZERO existing presence
high_demand_low_presence = gdf[(gdf["DemandIndex"] >= 70) & (gdf["ExistingStores"] == 0)]

print("\n🔍 EVALUATING REGIONAL EXPANSION OPPORTUNITIES:")
print(f"• Total high-demand zones evaluated: {len(gdf[gdf['DemandIndex'] >= 70])}")
print(f"• Optimal expansion zones discovered (High Demand + No Presence): {len(high_demand_low_presence)}")

# --- 4. TOP 5 OPTIMAL AREAS FOR BUSINESS EXPANSION ---
print("\n📌 TOP 5 SUGGESTED COORDINATES FOR SITE SELECTION:")
top_expansion_zones = high_demand_low_presence.sort_values(by="DemandIndex", ascending=False).head(5)

print(top_expansion_zones[["LocationID", "Latitude", "Longitude", "DemandIndex", "ExistingStores"]])

# --- 5. STRATEGIC EXPANSION RECOMMENDATIONS ---
print("\n" + "="*21 + " SITE SELECTION INSIGHTS " + "="*21)
print("> MARKET GAP DETECTED: The locations listed above represent massive untapped market value.")
print("  Action: Deploy spatial buffer zoning around these coordinates to clear priority lease options.")
print("> RESOURCE ALLOCATION: Redirect capital away from zones with an existing store footprint >= 2,")
print("  as cannibalization risks outweigh market share gains in those sectors.")
print("=" * 67)

# Export spatial analytics ledger
gdf.to_csv("geospatial_business_expansion.csv", index=False)
print("\n✅ Spatial analysis complete! Master ledger saved to 'geospatial_business_expansion.csv'.")
