class Dataset:
    def __init__(self, name, dataframe, temporary=False):
        self.name = name
        self.df = dataframe
        self.is_temporary = temporary
        self.history = [dataframe.copy()]  # Store history for undo/reset

    def save_state(self):
        """Save current state to history"""
        self.history.append(self.df.copy())

    def undo(self):
        """Undo last operation"""
        if len(self.history) > 1:
            self.df = self.history[-2].copy()
            self.history = self.history[:-1]
            return True
        return False

    def reset(self):
        """Reset to original state"""
        if len(self.history) > 1:
            self.df = self.history[0].copy()
            self.history = [self.history[0].copy()]  # Reset history to just original
            return True
        return False

class DatasetManager:
    def __init__(self):
        self.datasets = {}  # name -> Dataset
        self.active_dataset_name = None

    def add_dataset(self, name, df, temporary=False):
        """Add a new dataset"""
        self.datasets[name] = Dataset(name, df, temporary)
        if self.active_dataset_name is None:
            self.active_dataset_name = name

    def get_active_dataset(self):
        """Return the currently active dataset"""
        if self.active_dataset_name:
            return self.datasets[self.active_dataset_name]
        return None

    def apply_basic_op(self, op_func):
        """Apply a per-file operation to the active dataset"""
        ds = self.get_active_dataset()
        if ds:
            ds.df = op_func(ds.df)

    def apply_cross_file_op(self, selected_names, op_func, result_name):
        """Apply a cross-file operation on selected datasets"""
        dfs = [self.datasets[name].df for name in selected_names if name in self.datasets]
        if not dfs:
            return None
        result_df = op_func(dfs)
        self.add_dataset(result_name, result_df, temporary=True)
        self.active_dataset_name = result_name
        return result_df
