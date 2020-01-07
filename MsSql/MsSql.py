from sqlalchemy import create_engine


class MsSql(object):
    def __init__(self, host=None, db_name=None, user=None, pw=None, driver=None):
        self.conn = ''
        self.cursor = ''
        self.host = host
        self.db_name = db_name
        self.user = user
        self.pw = pw
        self.driver = driver
        self.engine = ''

    def session_conn(self):
        self.engine = create_engine(
            'mssql+pyodbc://{}:{}@{}/{}?driver={}'.format(self.user, self.pw, self.host, self.db_name, self.driver))
        self.conn = self.engine.connect()

    def get_column_names(self):
        columns = [c[0] for c in self.cursor.description]
        return columns

    def query(self, sql=None, many=True):
        if not sql:
            return 'no sql'
        qry = self.conn.execute(sql)
        qry_res = {'cols': qry.keys(), 'rows': qry.fetchall()}
        return qry_res

    def matrix(self, sql=None):
        table = self.query(sql=sql)
        rows = table.get('rows')
        cols = table.get('cols')
        obj_list = []
        for row in rows:
            zipped = zip(cols, row)
            obj_list.append(dict(zipped))
        return obj_list

    def upsert(self, df, index, conn=None, table=None, schema=None, chunk_size=1000, datatypes={}, temp=True):
        temp_table = "temp_" + table
        if temp:
            print('temp table loading')
            df.to_sql(name=temp_table, con=conn, if_exists='append',
                      index=False, schema=schema, chunksize=chunk_size,
                      dtype=datatypes)

            columns = df.columns.tolist()
            cols = tuple(columns)

            insert_values = ''
            update_values = ''

            for col in cols:
                insert_values += 'S.{col}, '.format(col=col)
                update_values += 'T.{col} = S.{col}, '.format(col=col)

            ids = ''
            for id in index:
                ids += 'T.{id} = S.{id} and '.format(id=id)

            sql = """MERGE {schema}.{target} AS T
            USING {schema}.{source} AS S
            ON ({ids})
            WHEN NOT MATCHED BY TARGET
            THEN INSERT ({cols}) VALUES ({insert_values})
            WHEN MATCHED
            THEN UPDATE SET {update_values};""".format(target=table, source=temp_table, schema=schema,
                                                       cols=','.join(cols), ids=ids[:-5],
                                                       insert_values=insert_values[:-2],
                                                       update_values=update_values[:-2])

            self.conn = self.conn.execution_options(autocommit=True)
            self.conn.execute(sql)
            self.conn.close()
