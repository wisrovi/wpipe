from wpipe.sqlite.Sqlite import SQLite


class Wsqlite:

    id: str = None

    output_db: dict = {}
    details_db: dict = {}
    input_db: dict = {}

    def __init__(self, db_name: str = "register.db") -> None:
        self.db_name = db_name

    @property
    def _input(self):
        pass

    @_input.setter
    def input(self, input: dict):
        self._create(input=input)

    @property
    def _output(self):
        pass

    @_output.setter
    def output(self, output: dict):
        self.output_db = output

    @property
    def _details(self):
        pass

    @_details.setter
    def details(self, details: dict):
        self.details_db = details

    def _create(self, input: dict):
        id = None
        with SQLite(self.db_name) as conection_db:
            id = conection_db.async_write(input=input)

        self.id = str(id)

    def _update(self, output: dict, details: dict = {}):
        with SQLite(self.db_name) as conection_db:
            conection_db.async_write(output=output, details=details, id=self.id)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._update(output=self.output_db, details=self.details_db)
