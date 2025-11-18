from evaluation_metrics.plotting.plot_base import PlotBase
from evaluation_metrics.constants import GRAPHICS_PATH
from evaluation_metrics.plotting.plot_style import PlotStyleManager
from pathlib import Path
from typing import Optional, List
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import seaborn as sns
from matplotlib.ticker import MaxNLocator


class HalsteadPlot(PlotBase):
    def __init__(self, halstead_csv_path: Path, loc_csv_path: Path, cc_csv_path: Path):
        super().__init__(halstead_csv_path)
        self.loc_csv_path = loc_csv_path
        self.cc_csv_path = cc_csv_path
        self.df = None
        self.style_manager = PlotStyleManager()

    def plot(self, algorithms: Optional[List[str]] = None, languages: Optional[List[str]] = None, save_file_name: Optional[str] = None):
        self.load_data(algorithms, languages)
        self.plot_halstead_radar(algorithms, languages, "radar_halstead.png")
        self.plot_scatter_grid_metrics(algorithms, languages, "scatter_grid_halstead.png")
    def _clean_algorithm_name(self, name: str) -> str:
        return re.sub(r"^\d{2}[-_]", "", name)

    def normalize_metrics(self, df, columns):
        return ((df[columns] - df[columns].mean()) / df[columns].std()).add(5).div(10)

    def filter_data(self, algorithms: Optional[List[str]] = None, languages: Optional[List[str]] = None, df_filtered: pd.DataFrame = None) -> pd.DataFrame:
        if df_filtered is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        if algorithms:
            clean_algorithms = [self._clean_algorithm_name(a) for a in algorithms]
            df_filtered = df_filtered[df_filtered["Algorithm"].isin(clean_algorithms)]
        if languages:
            df_filtered = df_filtered[df_filtered["Language"].isin(languages)]
        df_filtered["Algorithm"] = df_filtered["Algorithm"].apply(self._clean_algorithm_name)
        return df_filtered

    def load_data(self, algorithms=None, languages=None,):
        halstead_df = pd.read_csv(self.csv_path, index_col=0)        
        loc_df = pd.read_csv(self.loc_csv_path, index_col=0)
        cc_df = pd.read_csv(self.cc_csv_path, index_col=0)
        halstead_df.rename(columns={"Directory": "Language"}, inplace=True)
        loc_melted = loc_df.reset_index().melt(id_vars="index", var_name="Algorithm", value_name="LOC")
        loc_melted.rename(columns={"index": "Language"}, inplace=True)
        cc_melted = cc_df.reset_index().melt(id_vars="index", var_name="Algorithm", value_name="CC")
        cc_melted.rename(columns={"index": "Language"}, inplace=True)
        halstead_df["Algorithm"] = halstead_df["File Name"].apply(
            lambda x: self._clean_algorithm_name(re.sub(r".*?/", "", x).replace(".py", ""))        )

        loc_melted["Algorithm"] = loc_melted["Algorithm"].apply(self._clean_algorithm_name)
        cc_melted["Algorithm"] = cc_melted["Algorithm"].apply(self._clean_algorithm_name)

        halstead_df = self.filter_data(algorithms, languages, halstead_df)
        loc_melted = self.filter_data(algorithms, languages, loc_melted)
        cc_melted = self.filter_data(algorithms, languages, cc_melted)

        metrics_df = pd.merge(loc_melted, cc_melted, on=["Algorithm", "Language"], how="outer")        
        halstead_metrics = halstead_df[
            ["Algorithm", "Language", "Vocabulary", "Length", "Volume", "Difficulty", "Effort"]
        ]
        
        master_df = pd.merge(metrics_df, halstead_metrics, on=["Algorithm", "Language"], how="left")
        self.df = master_df
        print("Master DataFrame .")
        print(master_df)
        

    def mean_data_master(self, df): 
        columns_metrics = [
            "CC", "LOC", "Vocabulary", "Length", "Volume", "Difficulty", "Effort"]
        df_average = df.groupby("Language")[columns_metrics].mean().round(2).reset_index()
        return df_average

    def plot_halstead_radar(self, algorithms:  Optional[List[str]], languages:  Optional[List[str]], save_file_name: str):
        halstead_metrics = ["Vocabulary", "Length", "Volume", "Difficulty", "Effort", "LOC", "CC"]
        df_grouped = self.df.groupby("Language")[halstead_metrics].mean()
        print("Mean Master DataFrame .")
        print(df_grouped)
        if languages:
            df_grouped = df_grouped.loc[df_grouped.index.isin(languages)]
        df_normalized = self.normalize_metrics(df_grouped, columns=halstead_metrics)
        df_normalized = df_normalized.reset_index()
        labels = halstead_metrics
        num_vars = len(labels)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]
        categories = df_normalized["Language"].unique()
        self.color_map = self.style_manager.get_color_map(categories)
        fig, ax = plt.subplots(figsize=(10, 7), subplot_kw=dict(polar=True))
        for _, row in df_normalized.iterrows():
            values = row[labels].tolist()
            values += values[:1]
            color = self.color_map.get(row["Language"], "gray")
            ax.plot(angles, values, label=row["Language"], linewidth=2, color=color)
            ax.fill(angles, values, alpha=0.1, color=color)

        ax.set_title("Complexity Metrics for Quantum Programming Languages", size=18, y=1.1)
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_thetagrids(np.degrees(angles[:-1]), labels)
        ax.set_ylim(0, 1)
        ax.legend(title="Language", loc='upper right', bbox_to_anchor=(1.2, 1.1))
        plt.tight_layout()

        full_path = GRAPHICS_PATH + save_file_name
        plt.savefig(full_path)
        plt.savefig(full_path.replace('.png', '.eps'), format='eps')
        print(f"✅ Radar chart saved to {full_path} y {full_path.replace('.png', '.eps')}")
        plt.show()


    def plot_scatter_grid_metrics(self, algorithms: Optional[List[str]], languages: Optional[List[str]], save_file_name: str):
        df = self.filter_data(algorithms, languages, self.df)
        if hasattr(self, "language_order") and self.language_order:
            df["Language"] = pd.Categorical(df["Language"], categories=self.language_order, ordered=True)
            df = df.sort_values("Language")
        df_grouped = df.groupby("Language")[
            ["LOC", "CC", "Vocabulary", "Length", "Volume", "Difficulty", "Effort"]
        ].mean().reset_index()
        df_grouped = df_grouped[~df_grouped["Language"].isin(["qasm", "classic"])]
        metric_pairs = [
            ("LOC", "CC"),
            ("LOC", "Effort"),
            ("CC", "Effort"),
            ("Volume", "Effort"),
            ("Difficulty", "Effort"),
            ("LOC", "Vocabulary")
        ]
        cols = 3
        rows = (len(metric_pairs) + cols - 1) // cols
        fig, axs = plt.subplots(rows, cols, figsize=(18, 4 * rows))
        axs = axs.flatten()
        for i, (x, y) in enumerate(metric_pairs):
            ax = axs[i]
            sns.scatterplot(
                data=df_grouped,
                x=x,
                y=y,
                hue="Language",
                s=100,
                ax=ax,
                palette=self.style_manager.get_color_map(df_grouped["Language"].unique()),
                legend=False
            )
            for j in range(df_grouped.shape[0]):
                ax.text(df_grouped[x].iloc[j] + 0.5, df_grouped[y].iloc[j], str(df_grouped["Language"].iloc[j]), fontsize=10)
            ax.set_title(f"{x} vs {y}", fontsize=10)
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        for j in range(i + 1, len(axs)):
            fig.delaxes(axs[j])
        ax.set_xlabel(x, fontsize=8)
        ax.set_ylabel(y, fontsize=8)
        plt.tight_layout()
        full_path = GRAPHICS_PATH + save_file_name
        plt.savefig(full_path)
        plt.savefig(full_path.replace('.png', '.eps'), format='eps')
        plt.show()