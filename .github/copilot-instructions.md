# Data Processing App - AI Agent Instructions

## Project Overview
Offline desktop app for preprocessing tabular datasets (CSV/Excel) using rule-based detection and user-confirmed transformations. Modular Python architecture with Pandas for data handling and Tkinter for GUI.

## Architecture
- **core/**: Business logic modules
  - `loader.py`: File loading (CSV via `pd.read_csv`, Excel via `pd.read_excel`)
  - `processor.py`: Data operations (duplicates, missing values, standardization, merging)
  - `state.py`: Dataset management with `DatasetManager` class handling multiple datasets and active selection
  - `utils.py`: Helper functions like `generate_temp_name` for temporary datasets
- **ui/**: Tkinter interface (`tkinter_ui.py`) with buttons for operations and file dialogs
- **utils/**: Shared utilities (`exporter.py` for multi-format export, though UI currently handles export inline)

## Key Patterns
- **DataFrame Operations**: All processing functions follow `df -> df` pattern (e.g., `remove_duplicates(df)` returns modified DataFrame)
- **State Management**: Use `DatasetManager` for dataset storage; operations modify active dataset in-place via `apply_basic_op`
- **Cross-file Operations**: Select multiple datasets from listbox, apply functions like `merge_datasets(dfs)` returning concatenated DataFrame
- **Temporary Datasets**: Merges create temporary datasets with auto-generated names (e.g., `temp_1705123456`)

## Developer Workflows
- **Run App**: `python main.py` launches Tkinter GUI
- **Dependencies**: Install via `pip install -r requirements.txt` (pandas, openpyxl)
- **File Loading**: Supports `.csv`, `.xlsx`, `.xls`; raises ValueError for unsupported formats
- **Export Formats**: CSV (no index), Excel (no index), JSON (records orient with indent)

## Conventions
- **Import Structure**: Core modules import Pandas; UI imports core modules directly
- **Error Handling**: Use try/except with `messagebox.showerror` for user-facing errors
- **Naming**: Dataset names from file paths; temporary names prefixed with operation type
- **Data Types**: Standardization converts objects to lowercase/stripped strings, numerics to numeric where possible

## Integration Points
- **File Dialogs**: `filedialog.askopenfilenames` for multi-file upload, `asksaveasfilename` for export
- **Preview**: Display DataFrame head(20) in Tkinter Text widget
- **Missing Value Handling**: Dialog-based method selection (delete/zero/fill) with optional fill value input