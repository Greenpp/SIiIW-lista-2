import sqlalchemy as sql


class Collector:
    """
    Data collector
    """

    def __init__(self, db_name='scp'):
        """
        :param db_name: str, optional
            Name of database
        """
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        """
        Connect to mariadb
        """

        self.connection = sql.create_engine('mysql+mysqldb://collector:1234@localhost:3306/' + self.db_name).connect()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close db connection
        """
        if self.connection is not None:
            self.connection.close()

    def push_data(self, file_name, time, returns, evals, method, order, dynamic):
        """
        Insert data into db
        """
        dynamic = 1 if dynamic else 0

        query = f'INSERT INTO tests (`file_name`, `time`, `returns`, `evals`, `method`, `order`, `dynamic`)' \
            f'VALUES ("{file_name}", {time}, {returns}, {evals}, "{method}", "{order}", {dynamic})'

        self.connection.execute(query)
