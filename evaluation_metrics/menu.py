
from .plotting.loc_plot import LocPlot
from .plotting.cc_plot import CCPlot
from .plotting.halstead_plot import HalsteadPlot
from pathlib import Path
from evaluation_metrics.constants import  RESULT_LOC_CSV_PATH, RESULT_CC_CSV_PATH, RESULT_HALSTEAD_CSV_PATH

DEFAULT_LANGUAGES = ['qiskit', 'cirq', 'qrisp', 'quapl', 'q#', 'qmod']   # Example: ['qiskit', 'cirq', 'qrisp', 'quapl', 'q#', 'qmod','pennylane', 'paddle']
DEFAULT_ALGORITHMS = ['01-deutsch-jotza','02-bernstein-vazirani','03-simon','04-grover'] # Example: ['01-deutsch-jotza','02-bernstein-vazirani','03-simon','04-grover','05-vqsvd']

def run_loc_plot():
    path = Path(RESULT_LOC_CSV_PATH)
    plotter = LocPlot(path)
    plotter.load_data()
     
    plotter.plot(DEFAULT_ALGORITHMS, DEFAULT_LANGUAGES)

def run_cc_plot():
    path = Path(RESULT_CC_CSV_PATH)
    plotter = CCPlot(path)
    plotter.load_data()
    plotter.plot(DEFAULT_ALGORITHMS, DEFAULT_LANGUAGES)

def run_halstead_plot():
    halstead_csv_path = Path(RESULT_HALSTEAD_CSV_PATH)
    loc_csv_path  = Path(RESULT_LOC_CSV_PATH)
    cc_csv_path = Path(RESULT_CC_CSV_PATH)
    plotter = HalsteadPlot(halstead_csv_path,loc_csv_path,cc_csv_path)    
    plotter.plot(DEFAULT_ALGORITHMS, DEFAULT_LANGUAGES)

def run_all_plots():
    for func in [run_loc_plot, run_cc_plot, run_halstead_plot]:
        func()

def main():
    while True:
        print("\n--- Menu ---")
        print("1. LOC")
        print("2. CC")
        print("3. Halstead")
        print("4. All Plots")
        print("0. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            run_loc_plot()
        elif choice == "2":
            run_cc_plot()
        elif choice == "3":
            run_halstead_plot()
        elif choice == "4":
            run_all_plots()
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
