import os
import pandas as pd
import numpy as np
from evaluation_metrics.core.metric_base import MetricBase
from evaluation_metrics.core.registry import register_metric

@register_metric("cc_loc_ratio")
class CcLocRatioAnalyzer(MetricBase):
    """
    Analizador para calcular el ratio de Complejidad Ciclomática (CC) / Líneas de Código (LOC).
    Este analizador depende de los resultados de 'loc_analyzer' y 'cyclomatic_analyzer'.
    """

    def __init__(self, config: dict, scanner):
        super().__init__(config, scanner)
        # Extrae la configuración específica para este analizador
        metric_config = config.get("metrics", {}).get("cc_loc_ratio", {})
        
        # Archivos de entrada
        self.ccc_file = metric_config.get("ccc_input", "evaluation_metrics/results/cyclomatic_complexity_calculator.csv")
        self.loc_file = metric_config.get("loc_input", "evaluation_metrics/results/loc.csv")
        
        # Archivo de salida
        self.output_file = metric_config.get("output", "evaluation_metrics/results/cc_loc_ratio.csv")
        
        self.results_df = None

    def run(self):
        print("\n Running CC / LOC Ratio analysis...")
        try:
            # Cargar los CSV generados por los otros analizadores
            # Asumimos que la primera columna es el índice (Language)
            loc_df = pd.read_csv(self.loc_file, index_col=0)
            ccc_df = pd.read_csv(self.ccc_file, index_col=0)

            # Asegurarse de que los datos sean numéricos, convirtiendo errores a NaN
            loc_numeric = loc_df.apply(pd.to_numeric, errors='coerce')
            ccc_numeric = ccc_df.apply(pd.to_numeric, errors='coerce')

            # Calcular el ratio
            # Usamos .div() para la división y reemplazamos inf (división por cero) y NaN con 0
            ratio_df = ccc_numeric.div(loc_numeric)
            ratio_df.replace([np.inf, -np.inf], 0, inplace=True)
            ratio_df.fillna(0, inplace=True)
            
            self.results_df = ratio_df

            print(" CC / LOC Ratio calculation complete.")

        except FileNotFoundError as e:
            print(f" ERROR: Input file not found. Make sure 'loc' and 'ccc' metrics have run.")
            print(f" Missing file: {e.filename}")
        except Exception as e:
            print(f" ERROR calculating CC/LOC ratio: {e}")

    def save_results(self):
        if self.results_df is not None:
            os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
            self.results_df.to_csv(self.output_file, index=True)
            print("-----------------------------------------------------------")
            print(self.results_df.round(2))
            print("-----------------------------------------------------------")
            print(f"CC / LOC Ratio results saved to {self.output_file}\n")
        else:
            print(" No CC / LOC Ratio results to save.")