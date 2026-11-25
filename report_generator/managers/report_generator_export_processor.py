import tomllib
from typing import Any

from django.core.files.base import ContentFile
from file_export.managers.file_export_processor_abc import FileExportProcessorABC
from process_pipeline.functions.processor_functions import ProcessorReturn
from process_pipeline.functions.result_files import (
    build_bytes_file,
    build_excel_file,
    build_zip_file,
)
from process_pipeline.functions.selection import FunctionSelection

from mt_tools.excel_processor.modules.excel_processor_formatter import (
    ExcelProcessorMontrekFormatter,
)
from mt_tools.report_generator.modules.report_generator_functions import (
    ReportGeneratorReturnType,
)

# OSError covers the missing settings file; KeyError covers a missing selection.
SETTINGS_ERRORS = (KeyError, OSError, tomllib.TOMLDecodeError)


class ReportGeneratorFileExportProcessor(FileExportProcessorABC):
    """Runs the report function the user picked and hands back the file it built.

    The selection travels in ``pipeline_data``, so this works the same whether the
    manager runs inline or in a Celery worker. Settings are resolved up front in
    ``pre_check`` so a broken TOML file fails the run with a readable message
    instead of blowing up halfway through a report.
    """

    excel_formatter = ExcelProcessorMontrekFormatter

    def __init__(self, registry_hub: Any, session_data: dict[str, Any]) -> None:
        super().__init__(registry_hub, session_data)
        self.output: ProcessorReturn | None = None
        self.settings: dict[str, Any] = {}
        self._selection: FunctionSelection | None = None

    @property
    def selection(self) -> FunctionSelection:
        if self._selection is None:
            self._selection = FunctionSelection.from_pipeline_data(self.pipeline_data)
        return self._selection

    def pre_check(self) -> bool:
        try:
            self.settings = self.selection.get_settings()
        except SETTINGS_ERRORS as e:
            self.set_message(f"Could not load the report settings: {e}")
            return False
        return True

    def process(self) -> bool:
        function_name = self.selection.function_name
        try:
            report_function = self.selection.get_function()
            self.output = report_function(self.session_data, self.settings)
        except Exception as e:
            self.set_message(
                f"Error raised during report function {function_name}: {e}"
            )
            return False
        self.set_message(f"Generated {function_name}!")
        return True

    def post_check(self) -> bool:
        if self.output is None:
            self.set_message("The report function returned nothing.")
            return False
        self.set_result_file(self.build_result_file())
        return True

    @property
    def processed_output(self) -> ProcessorReturn:
        if self.output is None:
            raise RuntimeError("The report function has not produced an output.")
        return self.output

    def build_result_file(self) -> ContentFile:
        output = self.processed_output
        file_name = f"{self.selection.function_name}.{output.return_type.value}"
        if output.return_type is ReportGeneratorReturnType.XLSX:
            return build_excel_file(
                output.data,
                file_name,
                formatter=self.excel_formatter.format_excel,
            )
        if output.return_type is ReportGeneratorReturnType.ZIP:
            return build_zip_file(list(output.data), file_name)
        if output.return_type is ReportGeneratorReturnType.PDF:
            return build_bytes_file(output.data, file_name)
        raise TypeError(f"Unknown return type {output.return_type}")
