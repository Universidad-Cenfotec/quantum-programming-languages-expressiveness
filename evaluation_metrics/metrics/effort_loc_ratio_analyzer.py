import os
import pandas as pd
import numpy as np
from evaluation_metrics.core.metric_base import MetricBase
from evaluation_metrics.core.registry import register_metric

@register_metric("effort_loc_ratio")
class EffortLocRatioAnalyzer(MetricBase):
    """
    Analizador para calcular el ratio de Esfuerzo (Halstead) / Líneas de Código (LOC).
    Este analizador depende de los resultados de 'loc_analyzer' y 'halstead_analyzer'.
    """

    def __init__(self, config: dict, scanner):
        super().__init__(config, scanner)
        metric_config = config.get("metrics", {}).get("effort_loc_ratio", {})
        
        # Archivos de entrada
        self.halstead_file = metric_config.get("halstead_input", "evaluation_metrics/results/halstead.csv")
        self.loc_file = metric_config.get("loc_input", "evaluation_metrics/results/loc.csv")
        
        # Archivo de salida
        self.output_file = metric_config.get("output", "evaluation_metrics/results/effort_loc_ratio.csv")
        
        self.results_df = None

    def run(self):
        print("\n Running Effort / LOC Ratio analysis...")
        try:
            # Cargar los CSV generados
            loc_df_wide = pd.read_csv(self.loc_file)
            halstead_df_long = pd.read_csv(self.halstead_file)

            # --- Preparar datos de LOC ---
            # loc.csv está en formato ancho, lo pasamos a formato largo (melt)
            loc_df_long = loc_df_wide.melt(id_vars=loc_df_wide.columns[0], var_name="Algorithm", value_name="LOC")
            loc_df_long = loc_df_long.rename(columns={loc_df_long.columns[0]: "Language"})

            # --- Preparar datos de Halstead ---
            # halstead.csv ya está en formato largo, solo renombramos columnas
            halstead_df_clean = halstead_df_long[["Directory", "File Name", "Effort"]].rename(
                columns={"Directory": "Language", "File Name": "Algorithm"}
            )

            # --- Unir los DataFrames ---
            merged_df = pd.merge(loc_df_long, halstead_df_clean, on=["Language", "Algorithm"])

            # --- Calcular el Ratio ---
            merged_df["LOC"] = pd.to_numeric(merged_df["LOC"], errors='coerce')
            merged_df["Effort"] = pd.to_numeric(merged_df["Effort"], errors='coerce')

            # Manejar división por cero
            merged_df["Effort_LOC_Ratio"] = merged_df.apply(
                lambda row: row['Effort'] / row['LOC'] if row['LOC'] > 0 else 0,
                axis=1
            )
            
            # Volver a pivotar a formato ancho para que sea consistente con los otros CSV
            self.results_df = merged_df.pivot(index="Language", columns="Algorithm", values="Effort_LOC_Ratio")
            self.results_df.fillna(0, inplace=True)

            print(" Effort / LOC Ratio calculation complete.")

        except FileNotFoundError as e:
            print(f" ERROR: Input file not found. Make sure 'loc' and 'halstead' metrics have run.")
            print(f" Missing file: {e.filename}")
        except Exception as e:
            print(f" ERROR calculating Effort/LOC ratio: {e}")

    def save_results(self):
        if self.results_df is not None:
            os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
            self.results_df.to_csv(self.output_file, index=True)
            print("-----------------------------------------------------------")
            print(self.results_df.round(2))
            print("-----------------------------------------------------------")
            print(f"Effort / LOC Ratio results saved to {self.output_file}\n")
        else:
            print(" No Effort / LOC Ratio results to save.")