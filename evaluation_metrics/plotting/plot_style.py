
import json
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors

class PlotStyleManager:
    def __init__(self, palette_name="Set3", override_colors=None):
        self.palette_name = palette_name
        self.override_colors = override_colors or {}
        
        config_path  = "evaluation_metrics/config.json"
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)
        self.language_order = config.get("language_order", [])


    def get_color_map(self, categories):        
        used_languages = [cat for cat in self.language_order if cat in categories]        
        if not used_languages:
            print("[ERROR] There is not recognized 'language_order' for the given categories.")
            return {cat: "#cccccc" for cat in categories}
        palette = sns.color_palette(self.palette_name, n_colors=len(used_languages))
        for idx, color in self.override_colors.items():
            if idx < len(palette):
                try:
                    palette[idx] = mcolors.to_rgb(color)
                except ValueError:
                    print(f"[WARNING] Invalid color: {color}")
        color_map = {}
        for i, cat in enumerate(used_languages):
            try:
                color = palette[i]
                color_map[cat] = mcolors.to_hex(color)
            except IndexError:
                print(f"[WARNING] No color for '{cat}'.")
                color_map[cat] = "#cccccc"
        for cat in categories:
            if cat not in color_map:
                print(f"[WARNING] '{cat}' is not in 'language_order'. Gray will be assigned")
                color_map[cat] = "#cccccc"
        return color_map

    def apply(self, figsize=(12, 6)):
        plt.figure(figsize=figsize)        
        plt.grid(axis='y', linestyle='--', alpha=0.7)
                

    def style_legend(self, ax, title="Programming Languages"):
        ax.legend(
            title=title,
            loc='upper left',
            bbox_to_anchor=(1.02, 1),
            borderaxespad=0,
            frameon=True,
            framealpha=0.4
        )

    def style_ticks(self, ax, x_rotation=45, y_rotation=0):
        ax.tick_params(axis='x', rotation=x_rotation, labelsize=13)
        ax.tick_params(axis='y', rotation=y_rotation, labelsize=13)
        

    def style_axes(self, ax, title: str, xlabel: str, ylabel: str, legend_title: str = "Programming Languages", title_fontsize=20, label_fontsize=16, show_legend: bool = True):
        ax.set_title(title, fontsize=title_fontsize)
        ax.set_xlabel(xlabel, fontsize=label_fontsize)
        ax.set_ylabel(ylabel, fontsize=label_fontsize)
        self.style_ticks(ax)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        if show_legend:
            ax.legend(
                title=legend_title,
                loc='best',
                frameon=True,
                fontsize=11
            )

