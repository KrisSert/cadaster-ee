from datetime import datetime
from typing import Dict, List

from tqdm import tqdm
import pandas as pd
from sqlalchemy import create_engine, text, update

from utils.logger import logger

def write_extract_to_csv(all_tables: Dict[str, List[dict]]) -> None:
    # write all data to separate csv files
    for table_name, table_data in all_tables.items():
        df = pd.DataFrame(table_data)
        df.to_csv(f'{table_name}.csv', index=False)


class Database:
    def __init__(self):
        self.engine = create_engine('postgresql://admin:admin@localhost:5432/db')

    def create_stg_target_table(self, df: pd.DataFrame, target_table_name: str) -> None:
        with tqdm(total=1, desc=f"Initializing target table {target_table_name}", unit="row") as pbar:
            df.head(n=0).to_sql(schema="stg_auction", name=target_table_name, con=self.engine, if_exists='replace', index=False)
            pbar.update(1)

    # metadata. interactions:
    def metadata_get_new_load_id(self) -> int:
        with self.engine.connect() as connection:
            query = text("SELECT MAX(load_id) FROM metadata.auction_load")
            result = connection.execute(query)
            current_max_load_id = result.scalar()
            # Increment the current maximum load_id by 1 to get a new load_id
            new_load_id = current_max_load_id + 1 if current_max_load_id is not None else 1
            return new_load_id
    
    def metadata_insert_new_load_id(self, load_id: int, data: Dict[str, List[dict]]) -> None: 

        def construct_load_type(data: Dict[str, List[dict]]) -> str:
            for key in data.keys():
                if "auction" in key.lower(): 
                    return "auction"
            return "unknown"
        
        def construct_tgt_tables_content(data: Dict[str, List[dict]]) -> List[str]:
            keys_list = list(data.keys())
            return keys_list
        
        # iterate over auction_ids in data and add row for each
        auction_ids = [item["id"] for item in data["auction"]]
        load_type = construct_load_type(data)
        tgt_tables_content = construct_tgt_tables_content(data)
        
        rows = []
        for auction_id in auction_ids:
            row = {
                'load_id': load_id,
                'timestamp': datetime.now(),
                'status': "OPEN",
                'auction_id': auction_id,
                'load_type': load_type,
                'tgt_tables_content': tgt_tables_content
            }
            rows.append(row)
        df = pd.DataFrame(rows)

        # insert metadata records to metadata.auction_load
        with tqdm(total=len(df), desc=f"Inserting load_id={load_id} into metadata.auction_load", unit="row") as pbar:
            df.to_sql(schema="metadata", name="auction_load", con=self.engine, if_exists='append', index=False)
            pbar.update(len(df))
        
        logger.info(f"Inserted new load_id: {load_id} into metadata.auction_load, auction_ids: {auction_ids}")
    
    def metadata_insert_success_status(self, load_id: int) -> None:
        try:
            with self.engine.connect() as connection:
                # Update the status to "SUCCESSFUL" for a specific load_id using a SQL query
                sql_query = """
                            UPDATE metadata.auction_load
                            SET status = 'SUCCESSFUL'
                            WHERE load_id = :load_id
                            AND timestamp = (
                                SELECT MAX(timestamp)
                                FROM metadata.auction_load
                                WHERE load_id = :load_id
                            )
                            """
                query = text(sql_query)
                result = connection.execute(query.bindparams(load_id=int(load_id)))
                connection.commit()
                logger.info(f"metadata_insert_success_status: load_id: {load_id} set to SUCCESSFUL, rowcount: {result.rowcount}")
        except Exception as e: 
            print(f"metadata_insert_success_status.Error updating status for load_id {load_id}: {e}")
            logger.error(f"metadata_insert_success_status.Error updating status for load_id {load_id}: {e}")

    # insert to staging in postgres
    def insert_tables_to_db_stg(self, load_id: int, data: Dict[str, List[dict]]) -> None:

        def cols_to_snake(data: pd.DataFrame) -> None:
            # Function to convert Camel Case to Snake Case
            def camel_mixed_to_snake(column_name):
                result = ''
                for i, char in enumerate(column_name):
                    if i > 0 and char.isupper() and not column_name[i - 1].isupper():
                        result += '_'
                    result += char.lower()
                return result

            original_column_names = data.columns.tolist()
            data.rename(columns=lambda x: camel_mixed_to_snake(x), inplace=True)

        def insert_stg_auction_data(load_id: int, df: pd.DataFrame, target_table_name: str) -> None:
            try:
                with tqdm(total=len(df), desc=f"Inserting into target table {target_table_name}", unit="row") as pbar:
                    # convert date_times
                    if 'auction_end_date_time' in df.columns:
                        df['auction_end_date_time'] = pd.to_datetime(df['auction_end_date_time'], utc=False, errors='coerce')
                    if 'decision_date' in df.columns:
                        df['decision_date'] = pd.to_datetime(df['decision_date'], format='%Y-%m-%d')
                    if 'publishing_date_time' in df.columns:
                        df['publishing_date_time'] = pd.to_datetime(df['publishing_date_time'], utc=True)
                    if 'official_announcement_date' in df.columns:
                        df['official_announcement_date'] = pd.to_datetime(df['official_announcement_date'], format='%Y-%m-%d')
                    if 'offer_deadline_date_time' in df.columns:
                        df['offer_deadline_date_time'] = pd.to_datetime(df['offer_deadline_date_time'], utc=True)
                    if 'contract_period' in df.columns:
                        df['contract_period'] = pd.to_datetime(df['contract_period'], format='%Y-%m-%d')
                    
                    # convert float
                    if 'area' in df.columns:
                        df['area'] = pd.to_numeric(df['area'], errors='coerce')
                    
                    # add load_timestamp col & insert to db
                    df.insert(0, 'load_id', load_id)
                    df.insert(1, 'load_timestamp', datetime.now())
                    df.to_sql(schema="stg_auction", name=target_table_name, con=self.engine, if_exists='append', index=False)
                    pbar.update(len(df))
            except Exception as e: 
                print(f"insert_stg_auction_data.Error inserting data into stagingtable: {target_table_name}, error: {e}")
                logger.error(f"insert_stg_auction_data.Error inserting data into stagingtable: {target_table_name}, error: {e}")
            
        self.metadata_insert_new_load_id(load_id, data)
        
        for table_name, dataset in data.items(): 
            
            try: 
                df = pd.DataFrame(dataset)
                cols_to_snake(df)
                insert_stg_auction_data(load_id, df, table_name)
                logger.info(f"Inserted {table_name} data into stg_auction.{table_name} with load_id: {load_id},"
                            f"nr of records: {len(df)}")
            
            except Exception as e: 
                logger.error(f"error inserting {table_name} data into stg_auction.{table_name}, errormessage: {e}")

        self.metadata_insert_success_status(load_id)

    # transform to base tables in postgres
    def insert_base_auction_data(self, load_id: int, data: Dict[str, List[dict]]) -> None:
        '''transformation between stg_auction -> base_auction.
        # takes data based on load_id
        # - cleans col names to snake case,
        # - join some easier constructs, 
        # - avoid duplication in base table,
        '''
        def get_dataset_base(table_name: str) -> List[dict]:
            '''
            Retrieves base table content in a DataFrame
            '''
            # TODO
            pass

        def insert_base_auction_data(load_id: int, df: pd.DataFrame, target_table_name: str) -> None:
            with tqdm(total=len(df), desc=f"Inserting into base table {target_table_name}", unit="row") as pbar:
                df.to_sql(schema="stg_auction", name=target_table_name, con=self.engine, if_exists='append', index=False)
                pbar.update(len(df))
        
        for table_name, dataset in data.items(): 
            df_new = pd.DataFrame(dataset)
            df_base = pd.DataFrame(get_dataset_base(table_name))
            
            # Identify new & updated rows w sql
            # TODO

            insert_base_auction_data(load_id, df_new, table_name)
            logger.info(f"Transformed data from staging to base_auction.{table_name} with load_id: {load_id},"
                        f"nr of new/updated records: {len(df_new)}")


    def get_conn_data(self) -> tuple:
        url = self.engine.url
        return url.username, url.host, url.port, url.database

    def close(self) -> None:
        # Close the database connection
        self.engine.dispose()

    def __del__(self) -> None:
        # Ensure that the close() method is called when the instance is about to be destroyed
        self.close()
        