import io
import pandas as pd
from datetime import datetime
from .Types import LOCAL, FULL, INCREMENTAL, SAVED_S3
from .Services.ExtractionOperation import ExtractionOperation


class Reader:
    def __init__(self, s3_credentials, struct, migrator_redshift_connector):
        self.struct = struct
        self.s3_credentials = s3_credentials
        self.migrator_redshift_connector = migrator_redshift_connector

    def convert_types(self, df):
        for c in self.struct["columns"]:
            case_target_type = {
                "varchar": "str",
                "text": "str",
                "timestamp": "datetime64[ns]",
                "super": "str",
                "int": pd.Int64Dtype(),
                "bigint": pd.Int64Dtype(),
            }

            if c["target_type"] in case_target_type.keys():
                df[c["source_name"]] = df[c["source_name"]].astype(
                    case_target_type[c["target_type"]]
                )
                if case_target_type[c["target_type"]] == "str":
                    df[c["source_name"]].replace("None", "", inplace=True)
        return df

    def get_incremental_statement(self):
        if (
            "source_incremental_column" in self.struct.keys()
            and self.struct["source_incremental_column"] is not None
            and "target_incremental_column" in self.struct.keys()
            and self.struct["target_incremental_column"] is not None
            and (self.load_option is None)
        ):
            self.migrator_redshift_connector.connect_target()
            sql = f"""
                select max("{self.struct["target_incremental_column"]}") as max_value
                from "{self.struct["target_schema"]}"."{self.struct["target_table"]}"
            """

            cursor = self.migrator_redshift_connector.target_conn.cursor()

            cursor.execute(sql)
            result = cursor.fetchall()

            if len(result) == 0 or result[0][0] is None:
                sql_return = ""
                self.load_option = FULL
            else:
                for c in self.struct["columns"]:
                    if c["target_name"] == self.struct["target_incremental_column"]:
                        target_type = c["target_type"]

                if (
                    target_type == "int"
                    or target_type == "bigint"
                    or target_type == "numeric"
                    or target_type == "float"
                    or target_type == "double"
                ):
                    sql_return = f'and "{self.struct["source_incremental_column"]}" > {result[0][0]}'
                else:
                    if (
                        self.struct["incremental_interval_delta"] is None
                        or self.struct["incremental_interval_delta"] == ""
                    ):
                        sql_return = f'and "{self.struct["source_incremental_column"]}" > \'{result[0][0]}\''
                    else:
                        sql_return = f'and "{self.struct["source_incremental_column"]}" >= \'{result[0][0]}\'::timestamp - interval \'{self.struct["incremental_interval_delta"]}\''

                self.load_option = INCREMENTAL

            cursor.close()
            self.migrator_redshift_connector.target_conn.close()

            return sql_return
        else:
            self.load_option = FULL
            return ""

    def get_columns_source(self):
        columns = []
        for c in self.struct["columns"]:
            if (
                c["target_type"] == "super"
                or c["target_type"] == "varchar"
                or c["target_type"] == "text"
            ):
                columns.append(
                    f'substring("{c["source_name"]}"::varchar,0,60000) as "{c["source_name"]}"'
                )
            else:
                columns.append(f'"{c["source_name"]}"')
        return ",".join(columns)

    def get_order_by_sql_statement(self):
        if (
            "source_incremental_column" in self.struct.keys()
            and self.struct["source_incremental_column"] is not None
        ):
            return f' order by "{self.struct["source_incremental_column"]}" asc'
        else:
            return ""

    def get_limit_sql_statement(self):
        if self.migrator_redshift_connector.env == LOCAL:
            return f" limit 100"
        else:
            return f""

    def get_sql_statement(self):
        sql = f"""
            select {self.get_columns_source()} 
            from "{self.struct["source_schema"]}"."{self.struct["source_table"]}" 
            where 1=1
            {self.get_incremental_statement()} 
            {self.get_order_by_sql_statement()}
            {self.get_limit_sql_statement()}
        """
        print(f"SQL Statement: {sql}")
        return sql

    def save_data_to_s3(self, load_option=None):
        self.load_option = load_option
        self.migrator_redshift_connector.connect_s3()
        self.migrator_redshift_connector.connect_source()

        sql = self.get_sql_statement()

        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        idx = 1
        path_file = None

        for chunk_df in pd.read_sql(
            sql,
            self.migrator_redshift_connector.source_conn,
            chunksize=self.struct["read_batch_size"],
        ):
            if len(chunk_df) != 0:
                path_file = f'raw/prefect/{self.migrator_redshift_connector.env}/{self.struct["database"]}/{self.struct["source_schema"]}/{self.struct["source_table"]}/{time}/{idx}.parquet'
                print(f"Saving file {path_file}")

                buffer = io.BytesIO()
                chunk_df = self.convert_types(chunk_df)

                chunk_df.to_parquet(buffer, index=False, engine="pyarrow")
                self.migrator_redshift_connector.s3_session.Object(
                    self.s3_credentials["bucket"],
                    path_file,
                ).put(Body=buffer.getvalue())

                buffer.close()
                idx = idx + 1

        self.migrator_redshift_connector.close_source()

        if path_file is None:
            return None
        else:
            url = f's3://{self.s3_credentials["bucket"]}/raw/prefect/{self.migrator_redshift_connector.env}/{self.struct["database"]}/{self.struct["source_schema"]}/{self.struct["source_table"]}/{time}/'

            self.migrator_redshift_connector.connect_target()
            ExtractionOperation(
                conn=self.migrator_redshift_connector.target_conn,
            ).create(
                relation_id=self.struct["id"],
                url=url,
                load_option=self.load_option,
                status=SAVED_S3,
            )
            self.migrator_redshift_connector.close_target()

            return url
