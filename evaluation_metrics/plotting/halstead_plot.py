from evaluation_metrics.plotting.plot_base import PlotBase
from evaluation_metrics.constants import GRAPHICS_PATH
from evaluation_metrics.plotting.plot_style import PlotStyleManager
from pathlib import Path
from typing import Optional, List
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re

class HalsteadPlot(PlotBase):
    def __init__(self, halstead_csv_path: Path, loc_csv_path: Path, cc_csv_path: Path):
        super().__init__(halstead_csv_path)
        self.loc_csv_path = loc_csv_path
        self.cc_csv_path = cc_csv_path
        self.df = None
        self.style_manager = PlotStyleManager()

    def plot(self, algorithms: Optional[List[str]] = None, languages: Optional[List[str]] = None, save_file_name: Optional[str] = None):
        self.plot_halstead_radar(algorithms, languages, "radar_halstead.png")

    def _clean_algorithm_name(self, name: str) -> str:
        return re.sub(r"^\d{2}[-_]", "", name)

    def normalize_metrics(self, df, columns):
        return ((df[columns] - df[columns].mean()) / df[columns].std()).add(5).div(10)

    def load_data(self):
        halstead_df = pd.read_csv(self.csv_path, index_col=0)
        loc_df = pd.read_csv(self.loc_csv_path, index_col=0)
        cc_df = pd.read_csv(self.cc_csv_path, index_col=0)

        halstead_df.rename(columns={"Directory": "Language"}, inplace=True)
        loc_melted = loc_df.reset_index().melt(id_vars="index", var_name="Algorithm", value_name="LOC")
        loc_melted.rename(columns={"index": "Language"}, inplace=True)
        cc_melted = cc_df.reset_index().melt(id_vars="index", var_name="Algorithm", value_name="CC")
        cc_melted.rename(columns={"index": "Language"}, inplace=True)
        loc_melted["Algorithm"] = loc_melted["Algorithm"].apply(self._clean_algorithm_name)
        cc_melted["Algorithm"] = cc_melted["Algorithm"].apply(self._clean_algorithm_name)

        metrics_df = pd.merge(loc_melted, cc_melted, on=["Algorithm", "Language"], how="outer")

        halstead_df["Algorithm"] = halstead_df["File Name"].apply(
            lambda x: self._clean_algorithm_name(re.sub(r".*?/", "", x).replace(".py", ""))
        )
        halstead_metrics = halstead_df[
            ["Algorithm", "Language", "Vocabulary", "Length", "Volume", "Difficulty", "Effort"]
        ]
        master_df = pd.merge(metrics_df, halstead_metrics, on=["Algorithm", "Language"], how="left")

        self.df = master_df
        print("Master DataFrame correctly built.")
        print(self.df.head())


    def mean_data_master(self, df):
        columns_metrics = [
            "CC", "LOC", "Vocabulary", "Length", "Volume", "Difficulty", "Effort"]
        df_average = df.groupby("Language")[columns_metrics].mean().round(2).reset_index()
        return df_average

    def plot_halstead_radar(self, algorithms:  Optional[List[str]], languages:  Optional[List[str]], save_file_name: str):
        #df_normalized=self.mean_data_master(self.df)
        halstead_metrics = ["Vocabulary", "Length", "Volume", "Difficulty", "Effort", "LOC", "CC"]
        df_grouped = self.df.groupby("Language")[halstead_metrics].mean()
        df_normalized = self.normalize_metrics(df_grouped, columns=halstead_metrics)        
        df_normalized = df_normalized.select_dtypes(include=[np.number])
        #df_grouped = self.df.groupby("Language")[halstead_metrics].mean()
        #df_normalized = self.normalize_metrics(df_grouped, columns=halstead_metrics)
        df_normalized = df_normalized.reset_index()

        if languages:
            df_normalized = df_normalized[df_normalized["Language"].isin(languages)]
        print('MASTER DATAFRAME')
        print(df_normalized.head())
        labels = df_normalized.columns.tolist()[1:]
        num_vars = len(labels)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]
        categories = df_normalized["Language"].unique()
        self.color_map = self.style_manager.get_color_map(categories)

        # Plot
        fig, ax = plt.subplots(figsize=(10, 7), subplot_kw=dict(polar=True))
        for _, row in df_normalized.iterrows():
            values = row[labels].tolist()
            values += values[:1]
            color = self.color_map.get(row["Language"], "gray")
            ax.plot(angles, values, label=row["Language"], linewidth=2, color=color)
            ax.fill(angles, values, alpha=0.1, color=color)

        ax.set_title("Halstead Radar Chart", size=18, y=1.1)
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_thetagrids(np.degrees(angles[:-1]), labels)
        ax.set_ylim(0, 1)
        ax.legend(title="Language", loc='upper right', bbox_to_anchor=(1.2, 1.1))
        plt.tight_layout()

        # Guardar y mostrar
        full_path = GRAPHICS_PATH + save_file_name
        plt.savefig(full_path)
        print(f"✅ Radar chart saved to {full_path}")
        plt.show()
