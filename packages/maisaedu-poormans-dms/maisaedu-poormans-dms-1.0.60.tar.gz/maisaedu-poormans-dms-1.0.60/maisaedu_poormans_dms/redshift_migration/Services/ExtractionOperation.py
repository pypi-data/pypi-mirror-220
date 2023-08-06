class ExtractionOperation:
    def __init__(self, conn=None):
        self.conn = conn

    def create(self, relation_id, url, load_option, status):
        cursor = self.conn.cursor()

        sql = f"""
            insert into dataeng.relations_extraction_operations
            (relation_id, url, option, status, created_at, updated_at)
            values
            ({relation_id}, '{url}', '{load_option}', '{status}', 'now()', 'now()')
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
