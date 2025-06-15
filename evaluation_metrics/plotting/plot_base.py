from cycler import cycler
from matplotlib import pyplot as plt
import pandas as pd
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, List

from evaluation_metrics.plotting.plot_style import PlotStyleManager


class PlotBase(ABC):
    def __init__(self, csv_path: Path):
        self.csv_path = csv_path
        self.df: Optional[pd.DataFrame] = None
        self.value_name = ""

        # Set the default styles
        self.style_manager = PlotStyleManager(override_colors={1: '#FFFF4B'})
        colors_dict = self.style_manager.get_color_map(range(10))
        color_list = list(colors_dict.values())
        plt.rc('axes', prop_cycle=cycler('color', color_list))

    def load_data(self):
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        self.df = pd.read_csv(self.csv_path)
        print(f"✅ Data loaded from: {self.csv_path}")
        self.df = self.df.rename(columns={"Unnamed: 0": "Language"})
        self.df = self.df.melt(id_vars="Language", var_name="Algorithm", value_name=self.value_name)

    def filter_data(
        self,
        algorithms: Optional[List[str]] = None,
        languages: Optional[List[str]] = None
    ) -> pd.DataFrame:
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")    
        print(self.df)

        df_filtered = self.df
        if algorithms:
            df_filtered = df_filtered[df_filtered["Algorithm"].isin(algorithms)]
        if languages:
            df_filtered = df_filtered[df_filtered["Language"].isin(languages)]
        print(df_filtered)
        return df_filtered

    @abstractmethod
    def plot(self):
        """Subclasses must implement at least one plot method."""
        pass
