
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm # progress bar for loops


# parameters: 
# year = 2021
# month = 1
# pg_user = 'root'
# pg_pass = 'root'
# pg_host = 'localhost'
# pg_port = '5432' #default port
# pg_db = 'ny_taxi'

# chunksize = 100000
# target_table= 'yellow_taxi_data'

# #read a sample of the data

# prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
# url = f'{prefix}yellow_tripdata_{year:04d}-{month:02d}.csv.gz'


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
} #dict specifying the datatypes for each column

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
] #list of columns to parse as dates


def ingest_data(
            url: str, 
            engine, 
            target_table: str,
            chunksize: int = 100000,
) -> pd.DataFrame:
    df_iter = pd.read_csv(
        url,
        dtype = dtype,
        parse_dates = parse_dates,
        iterator=True,
        chunksize=chunksize      
        ) 
    # made a iterator that will yield dataframes of size chunksize

    first_chunk = next(df_iter) # the first time you call next, it will read the first chunk, 
    #the second time, it will read the second chunk...
    first_chunk[0:0].to_sql(name=target_table, con=engine, if_exists='replace')
    # what is con=engine? the connection to the database
    # con is a parameter that specifies the database connection to use
    # engine is a SQLAlchemy engine object that represents the connection to the database 
    # what is to_sql()? method that allows us to write a DataFrame to a SQL database from the pandas library
    # what is [0:0]? it means we want the schema only, no data
    # if_exists='replace': if the table already exists, replace it so that we can always start from scratch
    print(f"Table {target_table} created in the database.")

    first_chunk.to_sql(name=target_table, con=engine, if_exists='append')
    # name allows us to append data to the table we just created, which shares the same schema as first_chunk
    # if_exists='append': if the table already exists, append the data to it - what about the header?
    # the ingestion starts by creating the table with the schema of the first chunk, then append the data
    # the reason why we still create the schema seperately is that if we directly append, pandas will infer dtypes based on the first chunk data
    # if the first chunk has missing values, the inferred dtypes may noe be correct
    # we can eliminate the concern by specyfying the dtypes explicitly when reading the csv file
    # but it is still a good practice to create the schema first
    print(f"inserting first chunk: {len(first_chunk)}")

    for index, df_chunk in enumerate(tqdm(df_iter)):
        df_chunk.to_sql(
                name = target_table,
                con = engine,
                if_exists = 'append'
        )
        print(f"insterted chunk {index}: the chunk size is {len(df_chunk)}")

    print(f"ingestion for the {target_table} completed")

def main():
    #url parameters:
    pg_user = 'root'
    pg_pass = 'root'
    pg_host = 'localhost'
    pg_port = '5432' #default port
    pg_db = 'ny_taxi'
    year = 2021
    month = 1


    chunksize = 100000
    target_table = 'yellow_taxi_data'


    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    url_prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'

    url = f'{url_prefix}/yellow_tripdata_{year:04d}-{month:02d}.csv.gz'
    ingest_data (
        url = url,
        engine = engine, # the connection to a postgres database
        target_table = target_table,
        chunksize = chunksize
    )
        
    
if __name__ == '__main__':
    main()
