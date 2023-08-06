import logging
import time
import timeit
from typing import Optional, List, Tuple
from psycopg2._psycopg import connection
import traceback
import pandas.io.sql as sqlio

from transportlib.utils import get_from_env, get_postgres_conn
from transportlib.transport import BaseTransport


def get_table_columns(conn:connection,
                      fully_qualified_table_name: str,
                      ) -> List[str]:
    schema, table_name = fully_qualified_table_name.split('.')[0], fully_qualified_table_name.split('.')[1]

    sql = f"""
    select column_name from information_schema.columns where table_schema = '{schema}' and table_name  = '{table_name}'
    """
    logging.info('Running SQL')
    logging.info(sql)

    cur = conn.cursor()
    cur.execute(sql)
    cols = [col[0] for col in cur.fetchall()]
    logging.info(f"Below columns are detected in table {fully_qualified_table_name}")
    logging.info(cols)

    return cols

def get_df_from_sql(conn: connection,
                    sql_template,
                    params,
                    ):

    logging.info('Running SQL')
    logging.info(sql_template)

    dat = sqlio.read_sql_query(
        sql=sql_template,
        con=conn,
        params=params,
    )
    return dat

class PostgresTransport(BaseTransport):
    """
    Truncate Staging Table
    Load CSV to Staging Table.
    Run Custom SQL which loads from Staging to L0 Table(s).
    """

    def __init__(self,
                 # Load to staging + L0
                 staging_table_name: str,
                 staging_to_l0_sql: str,
                 staging_to_l0_args: Optional[Tuple],
                 # Credntials
                 host = None,
                 port = None,
                 user = None,
                 password = None,
                 database = None,
                 *args,
                 **kwargs,
                 ):
        super(PostgresTransport, self).__init__(*args, **kwargs)
        self.conn = get_postgres_conn(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
        )


        self.cur = self.conn.cursor()
        self.staging_table_name = staging_table_name
        self.staging_to_l0_sql = staging_to_l0_sql
        self.staging_l0_args = staging_to_l0_args

        self.source_to_staging_elapsed_seconds = None
        self.staging_to_l0_elapsed_seconds = None

    def run(self):
        # Truncate table
        self.truncate_staging_table()

        # Bulk load data to staging
        try:
            self.source_to_staging_elapsed_seconds = self.load_csv_file_to_staging()

        except Exception as e:
            logging.error("Something went wrong with loading csv data to staging!!!")
            logging.error(traceback.format_exc())
            return False

        # LOad from staging to l0
        try:
            self.staging_to_l0_elapsed_seconds = self.load_from_staging_to_l0()
            self.cur.close()
        except Exception as e:
            logging.error("Something went wrong with loading from staging to l0!!!")
            logging.error(traceback.format_exc())
            return False
        finally:
            logging.info("Closing connection....")
            if self.conn is not None:
                self.conn.close()

    def get_staging_table_columns(self) -> List[str]:
        return get_table_columns(conn=self.conn, fully_qualified_table_name=self.staging_table_name)

    def truncate_staging_table(self):
        logging.info(f"Now truncating {self.staging_table_name}...")

        truncate_table_sql = f"""
        TRUNCATE TABLE staging.{self.staging_table_name}
        """

        logging.info('Running SQL')
        logging.info(truncate_table_sql)

        self.cur.execute(truncate_table_sql)
        self.conn.commit()

    def load_csv_file_to_staging(
            self,
    ):
        start = timeit.default_timer()
        logging.info(f"Now loading file {self.csv_file_path} to staging")
        load_to_staging_sql = f"""
        -- COPY all data from csv into staging table
        
        COPY staging.{self.staging_table_name} FROM stdin with CSV HEADER DELIMITER as ',' QUOTE as '"' ;
        """
        logging.info("COPY JOB")
        logging.info(load_to_staging_sql)

        with open(self.csv_file_path, 'r') as read_file:
            self.cur.copy_expert(sql=load_to_staging_sql, file=read_file)
            self.conn.commit()
        end = timeit.default_timer()
        return end - start


    def load_from_staging_to_l0(
            self,
    ):
        start = timeit.default_timer()
        logging.info(f"Now loading data from staging to l0 with the below SQL:")
        logging.info(self.staging_to_l0_sql)

        if self.staging_l0_args is None:
            self.cur.execute(query=self.staging_to_l0_sql)
        else:
            self.cur.execute(self.staging_to_l0_sql, self.staging_l0_args)

        # Print notice
        notices = self.conn.notices
        if type(notices) == list:
            for notice in self.conn.notices:
                logging.info(notice)
        else:
            logging.info("No notice is printed")

        self.conn.commit()
        end = timeit.default_timer()
        return end - start
