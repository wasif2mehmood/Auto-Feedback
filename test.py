import pandas as pd

# Load the CSV and check what's in it
df = pd.read_csv("./scores/rag_repo.csv")
print("CSV Shape:", df.shape)
print("\nColumn names:", df.columns.tolist())
print("\nUnique publication_external_id values:")
print(df['publication_external_id'].unique())
print("\nFirst few rows:")
print(df.head())

# Check if m7GVzxm05ZEj exists
target_id = "m7GVzxm05ZEj"
matches = df[df['publication_external_id'] == target_id]
print(f"\nRows matching {target_id}:")
print(matches)