from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional, Union, Iterable

from .batchwriter import BatchWriter
from .inputdata import InputData
from .metadata import MetaData
from .table import Table


class Job:
    def __init__(
        self,
        input_data: InputData,
        tables: Optional[Iterable[Table]] = None,
        metadata: Optional[MetaData] = None,
        directory: Optional[Union[str, Path]] = None,
        name: Optional[str] = None,
        logbook: Union[bool, str] = True,
        interactive: bool = False,
        setup: bool = True,
    ):
        """
        A job to protect a data source.

        This class takes care of generating all input/meta files that TauArgus needs.
        If a directory is supplied, the necessary files will be created in that directory.
        Otherwise, a temporary directory is created, but it's better to always supply one.
        Existing files won't be written to `directory`.
        For example, if metadata is created from
        `MetaData.from_rda("otherdir/metadata.rda")`
        the existing file is used. If modifications are made to the metadata, then the user
        should call metadata.to_rda() first.

        :param input_data: The source from which to generate tables. Needs to be either
        MicroData or TableData.
        :param tables: The tables to be generated. Can be omitted if input_data is TableData.
        :param metadata: The metadata of input_data. If omitted, it will be derived from input_data.
        :param directory: Where to write tau-argus files.
        :param name: Name from which to derive the name of some temporary files.
        :param logbook: Whether this job should create its own logging file.
        :param interactive: Whether the gui should be opened.
        :param setup: Whether to set up the job inmediately. (required before run).
        """

        if directory is None:
            # Prevent the directory from being garbage-collected as long as this job exists
            self._tmp_directory = TemporaryDirectory(prefix='pyargus_')
            directory = Path(self._tmp_directory.name)

        if name is None:
            name = f'job_{id(self)}'

        if not isinstance(input_data, InputData):
            raise TypeError("Input needs to be MicroData or TableData")

        if tables is None:
            if isinstance(input_data, Table):
                tables = [input_data]
            else:
                raise ValueError("No outputs specified")

        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.input_data = input_data
        self.tables = tables
        self.metadata = metadata
        self.directory = Path(directory).absolute()
        self.name = name
        self.logbook = logbook
        self.interactive = interactive

        if setup:
            self.setup()

    def __str__(self):
        return self.name

    @property
    def batch_filepath(self):
        return self.directory / f'{self.name}.arb'

    @property
    def logbook_filepath(self):
        if self.logbook is True:
            logbook = self.directory / f'{self.name}_logbook.txt'
        else:
            logbook = self.logbook

        return Path(logbook).absolute()

    @property
    def workdir(self):
        return self.directory / "work" / self.name

    def setup(self, check=True):
        """Generate all files required for TauArgus to run."""
        self._setup_directories()
        self._setup_input_data()
        self._setup_hierarchies()
        self._setup_codelists()
        self._setup_metadata()
        self._setup_apriories()
        self._setup_tables()
        self._setup_batch()

        if check:
            self.check()

    def _setup_directories(self):
        input_directory = self.directory / 'input'
        output_directory = self.directory / 'output'
        input_directory.mkdir(exist_ok=True)
        output_directory.mkdir(exist_ok=True)
        self.workdir.mkdir(parents=True, exist_ok=True)

    def _setup_input_data(self):
        default = self.directory / 'input' / f"{self.input_data.name}.csv"
        if not self.input_data.filepath:
            self.input_data.to_csv(default)

    def _setup_metadata(self):
        if not self.metadata:
            self.metadata = self.input_data.generate_metadata()

        default = self.directory / 'input' / f"{self.input_data.name}.rda"
        if not self.metadata.filepath:
            self.metadata.to_rda(default)

    def _setup_hierarchies(self):
        self.input_data.resolve_column_lengths()
        for col, hierarchy in self.input_data.hierarchies.items():
            if not hierarchy.filepath:
                default = self.directory / 'input' / f'hierarchy_{col}.hrc'
                hierarchy.to_hrc(default, length=self.input_data.column_lengths[col])

    def _setup_codelists(self):
        self.input_data.resolve_column_lengths()
        for col, codelist in self.input_data.codelists.items():
            if not codelist.filepath:
                default = self.directory / 'input' / f'codelist_{col}.cdl'
                codelist.to_cdl(default, length=self.input_data.column_lengths[col])

    def _setup_apriories(self):
        for table in self.tables:
            if table.apriori and table.apriori.filepath is None:
                default = self.directory / 'input' / f'apriori_{table.name}.hst'
                table.apriori.to_hst(default)

    def _setup_tables(self):
        for table in self.tables:
            if table.filepath_out is None:
                table.filepath_out = Path(self.directory / 'output' / f'{table.name}.csv')

    def _setup_batch(self):
        with open(self.batch_filepath, 'w') as batch:
            writer = BatchWriter(batch)

            if isinstance(self.input_data, Table):
                writer.open_tabledata(str(self.input_data.filepath))
            else:
                writer.open_microdata(str(self.input_data.filepath))

            writer.open_metadata(str(self.metadata.filepath))

            for table in self.tables:
                writer.specify_table(table.explanatory, table.response, table.shadow, table.cost,
                                     table.labda)

                safety_rules = table.safety_rule,
                writer.safety_rule(safety_rules)

            if isinstance(self.input_data, Table):
                writer.read_table()
            else:
                writer.read_microdata()

            for t_index, table in enumerate(self.tables, 1):
                if table.apriori:
                    writer.apriori(
                        table.apriori.filepath,
                        t_index,
                        separator=table.apriori.separator,
                        ignore_error=table.apriori.ignore_error,
                        expand_trivial=table.apriori.expand_trivial,
                    )

                if table.suppress_method:
                    writer.suppress(table.suppress_method, t_index, *table.suppress_method_args)

                writer.write_table(t_index, 2, {"AS": True}, str(table.filepath_out))

            if self.interactive:
                writer.go_interactive()

    def check(self):
        problems = []
        for table in self.tables:
            for var in table.find_variables():
                if var not in self.input_data.dataset.columns:
                    problems.append(f"Variable {var} not present in input_data")
                elif self.metadata is not None:
                    if var not in self.metadata:
                        problems.append(f"Variable {var} not present in metadata.")

            for var in table.find_variables(categorical=True, numeric=False):
                if var in self.metadata:
                    if not self.metadata[var]["RECODABLE"] or self.metadata[var]["RECODEABLE"]:
                        problems.append(f"Variable {var} not recodable")
                else:
                    problems.append(f"Variable {var} not in metadata")

            for var in table.find_variables(categorical=False, numeric=True):
                if var in self.metadata:
                    if not self.metadata[var]["NUMERIC"]:
                        problems.append(f"Variable {var} not numeric.")
                else:
                    problems.append(f"Variable {var} not in metadata")

        if problems:
            raise JobSetupError(problems)


class JobSetupError(Exception):
    def __init__(self, problems):
        self.problems = problems

    def __str__(self):
        problem_str = "\n".join([f"- {problem}" for problem in self.problems])
        return f"Problems found in setup:\n{problem_str}"
