# Usamos una imagen base de Python 3.12.8
FROM python:3.12.8-slim

# Instalar dependencias básicas y Jupyter
RUN pip install --upgrade pip
RUN pip install jupyter numpy pandas cirq==0.10.0 qiskit==1.3.2 aer==0.3.0 qiskit[visualization] qrisp==0.6

# Instalar aer manualmente para asegurarnos de que esté presente
RUN pip install qiskit-aer

# Resolver problemas de compatibilidad con flask y werkzeug
RUN pip uninstall -y flask werkzeug
RUN pip install flask==2.2.0 werkzeug==2.3.0

# Establecemos el directorio de trabajo
WORKDIR /workspace

# Exponemos el puerto 8888 (el puerto de Jupyter Notebook)
EXPOSE 8888

# Comando para ejecutar Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
