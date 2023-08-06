from .Connector import Connector
from .Reader import Reader
from .Writer import Writer
from .Services.Struct import Struct
from .Types import check_if_env_is_valid, check_if_option_is_valid


class MigratorRedshift:
    def __init__(
        self,
        env=None,
        s3_credentials=None,
        struct=None,
        source_credentials=None,
        target_credentials=None,
    ):
        check_if_env_is_valid(env)

        self.migrator_redshift_connector = Connector(
            env=env,
            s3_credentials=s3_credentials,
            source_credentials=source_credentials,
            target_credentials=target_credentials,
        )

        self.migrator_redshift_reader = Reader(
            s3_credentials=s3_credentials,
            struct=struct,
            migrator_redshift_connector=self.migrator_redshift_connector,
        )

        self.migrator_redshift_writer = Writer(
            struct=struct,
            migrator_redshift_connector=self.migrator_redshift_connector,
        )

        self.source_credentials = source_credentials
        self.struct = struct
        self.s3_credentials = s3_credentials
        self.env = env

    def check_target_table_has_data(self):
        self.migrator_redshift_connector.connect_target()
        sql = f"""
            select count(*) from "{self.struct["target_schema"]}"."{self.struct["target_table"]}" limit 1
        """
        cursor = self.migrator_redshift_connector.target_conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if result[0][0] == 0:
            return False
        else:
            return True

    def extract_to_redshift(self, load_option=None):
        check_if_option_is_valid(load_option)

        url = self.migrator_redshift_reader.save_data_to_s3(load_option)
        return self.migrator_redshift_writer.save_to_redshift(url)

    def get_structs_source_to_target(self, database, tables="all"):
        self.migrator_redshift_connector.connect_target()
        structs = Struct(conn=self.migrator_redshift_connector.target_conn).get(
            database=database,
            tables=tables,
        )

        self.migrator_redshift_connector.target_conn.close()

        return structs
