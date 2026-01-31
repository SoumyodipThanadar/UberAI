import pandas as pd
from opportunity_rules import opportunity_rules

df = pd.read_csv("Dataset/growth_index.csv")
df['recommendation'] = df.apply(opportunity_rules, axis=1)

df.to_csv("Dataset/business_recommendations.csv", index=False)
