from cycler import cycler
from evaluation_metrics.plotting.plot_base import PlotBase
from pathlib import Path
import matplotlib.pyplot as plt
from scipy.stats import hmean
import seaborn as sns
from evaluation_metrics.constants import GRAPHICS_PATH 
from evaluation_metrics.plotting.plot_style import PlotStyleManager

class LocPlot(PlotBase):
    def __init__(self, csv_path: Path):
        super().__init__(csv_path)
        self.value_name = "LOC"                 

    def plot(self, algorithms=None, languages=None, save_file_name=None):
        self.plot_loc_by_algorithm(algorithms, languages, 'loc_by_algorithm.png')
        self.plot_mean_loc_by_language(algorithms, languages, 'loc_mean_by_algorithm.png')

    def plot_mean_loc_by_language(self, algorithms=None, languages=None, save_file_name='loc_by_algorithm.png'):
        df_filtered = self.filter_data(algorithms, languages)
        mean_values = df_filtered.groupby("Language")["LOC"].mean().sort_values()
        sem_values = df_filtered.groupby("Language")["LOC"].sem().reindex(mean_values.index)
        color_map = self.style_manager.get_color_map(mean_values.index)
        colors = [color_map.get(lang, "#cccccc") for lang in mean_values.index]
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(
            mean_values.index,
            mean_values.values,
            yerr=sem_values.values,
            capsize=5,
            color=colors)
        self.style_manager.style_axes(
            ax,
            title="Mean LOC by Algorithm Across Quantum Programming Languages",
            xlabel="Quantum Programming Languages",
            ylabel="Mean LOC")
        plt.tight_layout()
        if save_file_name:
            plt.savefig(GRAPHICS_PATH + save_file_name)
        plt.show()

    def plot_loc_by_algorithm(self, algorithms=None, languages=None, save_file_name=None):
        df_filtered = self.filter_data(algorithms, languages)
        pivot = df_filtered.pivot_table(index="Algorithm", columns="Language", values="LOC")
        color_map = self.style_manager.get_color_map(pivot.columns)
        colors = [color_map.get(lang, "#cccccc") for lang in pivot.columns]
        ax = pivot.plot(kind='bar', figsize=(16, 6), width=0.8, color=colors)
        self.style_manager.style_axes(
            ax,
            title="Lines of Code by Algorithm and Language",
            xlabel="Quantum Algorithm Implementations",
            ylabel="LOC"
        )        
        plt.tight_layout()
        if save_file_name:
            plt.savefig(GRAPHICS_PATH + save_file_name)        
        plt.show()
