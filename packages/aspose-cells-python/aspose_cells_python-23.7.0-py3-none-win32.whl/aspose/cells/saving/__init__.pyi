from typing import List, Optional, Dict, Iterable
import aspose.pycore
import aspose.pydrawing
import aspose.cells
import aspose.cells.charts
import aspose.cells.digitalsignatures
import aspose.cells.drawing
import aspose.cells.drawing.activexcontrols
import aspose.cells.drawing.equations
import aspose.cells.drawing.texts
import aspose.cells.externalconnections
import aspose.cells.json
import aspose.cells.markup
import aspose.cells.metadata
import aspose.cells.numbers
import aspose.cells.ods
import aspose.cells.pivot
import aspose.cells.properties
import aspose.cells.querytables
import aspose.cells.rendering
import aspose.cells.rendering.pdfsecurity
import aspose.cells.revisions
import aspose.cells.saving
import aspose.cells.settings
import aspose.cells.slicers
import aspose.cells.tables
import aspose.cells.timelines
import aspose.cells.utility
import aspose.cells.vba
import aspose.cells.webextensions

class SqlScriptColumnTypeMap:
    '''Represents column type map.'''
    
    def get_string_type(self) -> str:
        '''Gets string type in the database.'''
        ...
    
    def get_numberic_type(self) -> str:
        '''Gets numeric type in the database.'''
        ...
    
    ...

class SqlScriptSaveOptions(aspose.cells.SaveOptions):
    '''Represents the options of saving sql.'''
    
    @property
    def save_format(self) -> aspose.cells.SaveFormat:
        ...
    
    @property
    def clear_data(self) -> bool:
        ...
    
    @clear_data.setter
    def clear_data(self, value : bool):
        ...
    
    @property
    def cached_file_folder(self) -> str:
        ...
    
    @cached_file_folder.setter
    def cached_file_folder(self, value : str):
        ...
    
    @property
    def validate_merged_areas(self) -> bool:
        ...
    
    @validate_merged_areas.setter
    def validate_merged_areas(self, value : bool):
        ...
    
    @property
    def merge_areas(self) -> bool:
        ...
    
    @merge_areas.setter
    def merge_areas(self, value : bool):
        ...
    
    @property
    def create_directory(self) -> bool:
        ...
    
    @create_directory.setter
    def create_directory(self, value : bool):
        ...
    
    @property
    def sort_names(self) -> bool:
        ...
    
    @sort_names.setter
    def sort_names(self, value : bool):
        ...
    
    @property
    def sort_external_names(self) -> bool:
        ...
    
    @sort_external_names.setter
    def sort_external_names(self, value : bool):
        ...
    
    @property
    def refresh_chart_cache(self) -> bool:
        ...
    
    @refresh_chart_cache.setter
    def refresh_chart_cache(self, value : bool):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def update_smart_art(self) -> bool:
        ...
    
    @update_smart_art.setter
    def update_smart_art(self, value : bool):
        ...
    
    @property
    def check_if_table_exists(self) -> bool:
        ...
    
    @check_if_table_exists.setter
    def check_if_table_exists(self, value : bool):
        ...
    
    @property
    def column_type_map(self) -> aspose.cells.saving.SqlScriptColumnTypeMap:
        ...
    
    @column_type_map.setter
    def column_type_map(self, value : aspose.cells.saving.SqlScriptColumnTypeMap):
        ...
    
    @property
    def check_all_data_for_column_type(self) -> bool:
        ...
    
    @check_all_data_for_column_type.setter
    def check_all_data_for_column_type(self, value : bool):
        ...
    
    @property
    def add_blank_line_between_rows(self) -> bool:
        ...
    
    @add_blank_line_between_rows.setter
    def add_blank_line_between_rows(self, value : bool):
        ...
    
    @property
    def separator(self) -> char:
        '''Gets and sets character separator of sql script.'''
        ...
    
    @separator.setter
    def separator(self, value : char):
        '''Gets and sets character separator of sql script.'''
        ...
    
    @property
    def operator_type(self) -> aspose.cells.saving.SqlScriptOperatorType:
        ...
    
    @operator_type.setter
    def operator_type(self, value : aspose.cells.saving.SqlScriptOperatorType):
        ...
    
    @property
    def primary_key(self) -> int:
        ...
    
    @primary_key.setter
    def primary_key(self, value : int):
        ...
    
    @property
    def create_table(self) -> bool:
        ...
    
    @create_table.setter
    def create_table(self, value : bool):
        ...
    
    @property
    def id_name(self) -> str:
        ...
    
    @id_name.setter
    def id_name(self, value : str):
        ...
    
    @property
    def start_id(self) -> int:
        ...
    
    @start_id.setter
    def start_id(self, value : int):
        ...
    
    @property
    def table_name(self) -> str:
        ...
    
    @table_name.setter
    def table_name(self, value : str):
        ...
    
    @property
    def export_as_string(self) -> bool:
        ...
    
    @export_as_string.setter
    def export_as_string(self, value : bool):
        ...
    
    @property
    def sheet_indexes(self) -> List[int]:
        ...
    
    @sheet_indexes.setter
    def sheet_indexes(self, value : List[int]):
        ...
    
    @property
    def export_area(self) -> aspose.cells.CellArea:
        ...
    
    @export_area.setter
    def export_area(self, value : aspose.cells.CellArea):
        ...
    
    @property
    def has_header_row(self) -> bool:
        ...
    
    @has_header_row.setter
    def has_header_row(self, value : bool):
        ...
    
    ...

class SqlScriptOperatorType:
    '''Represents the type of operating data.'''
    
    @classmethod
    @property
    def INSERT(cls) -> SqlScriptOperatorType:
        '''Insert data.'''
        ...
    
    @classmethod
    @property
    def UPDATE(cls) -> SqlScriptOperatorType:
        '''Update data.'''
        ...
    
    @classmethod
    @property
    def DELETE(cls) -> SqlScriptOperatorType:
        '''Delete data.'''
        ...
    
    ...

