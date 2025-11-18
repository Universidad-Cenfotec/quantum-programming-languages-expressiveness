import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Optional, List
import re

from evaluation_metrics.plotting.plot_base import PlotBase
from evaluation_metrics.constants import GRAPHICS_PATH
from evaluation_metrics.plotting.plot_style import PlotStyleManager

class RatioPlot(PlotBase):
    """
    Generates a scatter plot comparing Cognitive Load (Effort/LOC)
    vs. Control Flow Density (CC/LOC).
    """

    def __init__(self, cc_loc_ratio_path: Path, effort_loc_ratio_path: Path):
        # We pass one of the paths to super() just to comply with the signature
        super().__init__(cc_loc_ratio_path)
        
        # We store the paths of the two ratio files
        self.cc_loc_ratio_path = cc_loc_ratio_path
        self.effort_loc_ratio_path = effort_loc_ratio_path
        
        self.df = None
        self.style_manager = PlotStyleManager()
        self.value_name = "Ratio"

    def load_data(self):
        """
        Loads and merges the two ratio CSVs (CC/LOC and Effort/LOC).
        """
        try:
            # Charging data
            cc_loc_df = pd.read_csv(self.cc_loc_ratio_path)
            effort_loc_df = pd.read_csv(self.effort_loc_ratio_path)
            cc_loc_df.rename(columns={cc_loc_df.columns[0]: 'Language'}, inplace=True)
            effort_loc_df.rename(columns={effort_loc_df.columns[0]: 'Language'}, inplace=True)
            cc_loc_melted = cc_loc_df.melt(
                id_vars="Language", var_name="Algorithm", value_name="CC_LOC_Ratio"
            )
            effort_loc_melted = effort_loc_df.melt(
                id_vars="Language", var_name="Algorithm", value_name="Effort_LOC_Ratio"
            )
            # Merge the two long dataframes
            master_df = pd.merge(
                cc_loc_melted, 
                effort_loc_melted, 
                on=["Algorithm", "Language"], 
                how="outer"
            )
            master_df.fillna(0, inplace=True)            
            self.df = master_df
            print("✅ Ratio data loaded and merged successfully.")
            
        except FileNotFoundError as e:
            print(f" ERROR: Input file not found. Have you run the ratio analyzers?")
            print(f" Missing file: {e.filename}")
            raise
        except Exception as e:
            print(f" ERROR loading ratio data: {e}")
            raise

    def plot(self, algorithms: Optional[List[str]] = None, languages: Optional[List[str]] = None, save_file_name: str = "ratio_scatter_plot.png"):
        """
        Main function to generate the ratio scatter plot.
        """
        if self.df is None:
            self.load_data()        
        self.plot_ratio_scatter(algorithms, languages, save_file_name)

    def plot_ratio_scatter(self, algorithms=None, languages=None, save_file_name=None):
        """
        Creates a scatter plot of Effort/LOC vs CC/LOC.
        """
        if self.df is None:
            print("Data not loaded. Call load_data() first.")
            return
        df_filtered = self.filter_data(algorithms, languages)   
        df_mean = df_filtered.groupby("Language")[["CC_LOC_Ratio", "Effort_LOC_Ratio"]].mean().reset_index()
        df_mean = df_mean[~df_mean["Language"].isin(["classic", "paddle"])]
        fig, ax = plt.subplots(figsize=(12, 8))
        color_map = self.style_manager.get_color_map(df_mean["Language"].unique())
        sns.scatterplot(
            data=df_mean,
            x="CC_LOC_Ratio",
            y="Effort_LOC_Ratio",
            hue="Language",
            palette=color_map,
            s=220,
            ax=ax,
            edgecolor="black",
            legend=False
        )
        for i in range(df_mean.shape[0]):
            plt.text(
                x=df_mean["CC_LOC_Ratio"][i] * 1.01,
                y=df_mean["Effort_LOC_Ratio"][i],
                s=df_mean["Language"][i],
                fontdict=dict(color='black', size=15)
            )
        self.style_manager.style_axes(
            ax,
            title="Control Flow Density vs. Cognitive Load per Line",
            xlabel="Control Flow Density (CC / LOC)",
            ylabel="Cognitive Load per Line (Effort / LOC)",
            show_legend=False
            
        )        
        # Move the legend outside the plot
        #ax.legend(title="Programming Languages", loc='upper left')
        plt.tight_layout()
        if save_file_name:
            full_path = GRAPHICS_PATH + save_file_name
            plt.savefig(full_path)
            print(f"✅ Scatter plot saved to {full_path}")        
        plt.show()