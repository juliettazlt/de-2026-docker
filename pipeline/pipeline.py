import sys
import pandas as pd
print(sys.argv)
month = sys.argv[1]
print(f"Month is {month}")


df = pd.DataFrame({"day": [1, 2], "num_passengers": [3, 4]})
print(df.head())
df['month'] = month
df.to_parquet(f"output_day_{sys.argv[1]}.parquet")
#parquet is a binary format designed for efficient data storage and retrieval
