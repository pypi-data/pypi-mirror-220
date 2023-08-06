class ExtractionOperation:
    def __init__(self, conn=None):
        self.conn = conn

    def create(self, struct, url, load_option, status, platform):
        cursor = self.conn.cursor()

        sql = f"""
            insert into dataeng.relations_extraction_operations
            (target_schema, target_table, url, option, platform, status, created_at, updated_at, received_at)
            values
            ('{struct['target_schema']}', '{struct['target_table']}', '{url}', '{load_option}', '{platform}', '{status}', 'now()', 'now()', 'now()')
        """

        cursor.execute(sql)

        self.conn.commit()
        cursor.close()

    def update(self, url, status):
        cursor = self.conn.cursor()

        sql = f"""
            update dataeng.relations_extraction_operations
            set status = '{status}', updated_at = 'now()'
            where url = '{url}'
        """

        cursor.execute(sql)
        self.conn.commit()
        cursor.close()
