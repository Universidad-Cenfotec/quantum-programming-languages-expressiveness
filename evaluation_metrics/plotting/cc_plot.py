# metrics/cc_plot.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import hmean
from evaluation_metrics.plotting.plot_base import PlotBase
from evaluation_metrics.constants import GRAPHICS_PATH
from typing import List, Optional

class CCPlot(PlotBase):
    def __init__(self, csv_path):
        super().__init__(csv_path)
        self.value_name = "CC" 

    def plot(self, algorithms: Optional[List[str]] = None, languages: Optional[List[str]] = None, save_file_name: Optional[str] = None):    
        self.plot_cc_by_algorithm(algorithms, languages, 'cc_by_algorithm.png')
        self.plot_mean_cc_by_language(algorithms, languages, 'mean_cc_by_algorithm.png')

    def plot_mean_cc_by_language(self, algorithms=None, languages=None, save_file_name=None):
        df_filtered = self.filter_data(algorithms, languages)
        mean_values = df_filtered.groupby("Language")["CC"].mean().sort_values()
        sem_values = df_filtered.groupby("Language")["CC"].sem().reindex(mean_values.index)
        color_map = self.style_manager.get_color_map(mean_values.index)
        colors = [color_map.get(lang, "#cccccc") for lang in mean_values.index]
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(
            mean_values.index,
            mean_values.values,
            yerr=sem_values.values,
            capsize=5,
            color=colors,      
        )
        self.style_manager.style_axes(
            ax,
            title="Mean CC by Algorithm Across Quantum Programming Languages",
            xlabel="Quantum Programming Languages",
            ylabel="Mean CC"
        )
        plt.tight_layout()
        if save_file_name:
            plt.savefig(GRAPHICS_PATH + save_file_name)
        plt.show()

    def plot_cc_by_algorithm(self, algorithms=None, languages=None, save_file_name=None):
        df_filtered = self.filter_data(algorithms, languages)
        pivot = df_filtered.pivot_table(index="Algorithm", columns="Language", values="CC")
        color_map = self.style_manager.get_color_map(pivot.columns)
        colors = [color_map.get(lang, "#cccccc") for lang in pivot.columns]
        ax = pivot.plot(kind='bar', figsize=(16, 6), width=0.8, color=colors)
        self.style_manager.style_axes(
            ax,
            title="CC by Algorithm in Quantum Programming Languages",
            xlabel="Quantum Algorithm Implementations",
            ylabel="CC"
        )        
        plt.tight_layout()
        if save_file_name:
            plt.savefig(GRAPHICS_PATH + save_file_name)        
        plt.show()
