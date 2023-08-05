import pathlib
from abc import ABC, abstractmethod
from io import IOBase
from typing import Union

from pydantic import Field

from metabolights_utils.models.common import MetabolightsBaseModel
from metabolights_utils.models.isa.investigation_file import Investigation
from metabolights_utils.models.isa.parser.investigation_parser import get_investigation
from metabolights_utils.models.parser.common import ParserReport


class InvestigationFileReaderResult(MetabolightsBaseModel):
    investigation: Investigation = Field(Investigation())
    parser_report: ParserReport = Field(ParserReport())


class InvestigationFileReader(ABC):
    @abstractmethod
    def read(
        self,
        file_buffer: IOBase = None,
        file_path: Union[str, pathlib.Path] = None,
        skip_parser_info_messages: bool = True,
    ) -> InvestigationFileReaderResult:
        """Reads investigation an file and return Investigation model and parser messages.
            If file buffer is not defined, it reads file_path.
           At least one of the file_buffer and file_path parameters should be defined.

        Args:
            file_buffer (IOBase): File buffer to read file content. io.StringIO, io.TextIOWrapper with open(), etc. Defaults to None.
            file_path (Union[str, pathlib.Path], optional): File path or pathlib.Path object. Defaults to None.
            skip_parser_info_messages (bool, optional): clear INFO messages from parser messages. Defaults to True.

        Raises:
            exc: any unexpected exception while reading file

        Returns:
            InvestigationFileReaderResult: Investigation model and parser messages
        """
        pass
