import pathlib
from abc import ABC, abstractmethod
from typing import Dict, List, Union

from pydantic import Field

from metabolights_utils.isatab.isa_table_file_reader import IsaTableFileReaderResult
from metabolights_utils.models.isa.common import IsaTable
from metabolights_utils.models.parser.common import ParserReport
from metabolights_utils.tsv.model import (
    TsvAction,
    TsvActionReport,
    TsvColumnData,
    TsvUpdateColumnsAction,
)
from metabolights_utils.tsv.tsv_file_updater import TsvFileUpdater


class IsaTableFileWriter(ABC):
    @abstractmethod
    def apply_actions(
        self,
        file_path: Union[str, pathlib.Path],
        file_sha256_hash: str,
        actions: List[TsvAction],
    ) -> TsvActionReport:
        """Applies

        Args:
            file_path (Union[str, pathlib.Path], optional): File path or pathlib.Path object.
            file_sha256_hash (str): SH256 of the input file. If file SHA256 does not match, method returns error.
            actions (List[TsvAction]): List of allowed actions
        Returns:
            TsvActionReport: results of each action. If an action result is not success, result message will be available.
        """

    @abstractmethod
    def save_isa_table(
        self,
        file_path: Union[str, pathlib.Path],
        file_sha256_hash: str,
        isa_table: IsaTable,
    ) -> TsvActionReport:
        """Applies

        Args:
            file_path (Union[str, pathlib.Path], optional): File path or pathlib.Path object.
            file_sha256_hash (str): SH256 of the input file. If file SHA256 does not match, method returns error.
            actions (List[TsvAction]): List of allowed actions
        Returns:
            TsvActionReport: results of each action. If an action result is not success, result message will be available.
        """


class IsaTableFileWriterImpl(TsvFileUpdater, IsaTableFileWriter):
    def save_isa_table(
        self,
        file_path: Union[str, pathlib.Path],
        file_sha256_hash: str,
        isa_table: IsaTable,
    ) -> TsvActionReport:
        column_indices = dict(zip(isa_table.columns, isa_table.column_indices))
        headers = {column_indices[x.column_header]: x.column_header for x in isa_table.headers}

        columns: Dict[int, TsvColumnData] = {}
        for column_name in isa_table.data:
            column_data: TsvColumnData = TsvColumnData()
            column_index = column_indices[column_name]
            columns[column_index] = column_data
            column_data.header_name = headers[column_index]
            column_data.values = dict(zip(isa_table.row_indices, isa_table.data[column_name]))

        column_update_action = TsvUpdateColumnsAction(columns=columns)
        report = self.apply_actions(
            file_path=file_path, file_sha256_hash=file_sha256_hash, actions=[column_update_action]
        )
        return report
