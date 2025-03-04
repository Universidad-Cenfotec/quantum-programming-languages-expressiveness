# Usamos una imagen base de Python 3.12.8
FROM python:3.12.8-slim

# Establecemos el directorio de trabajo
WORKDIR /workspace

# Copiamos el archivo de requerimientos
COPY requirements.txt .

# Instalamos las dependencias desde requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Instalamos paquetes adicionales para Q# y Azure Quantum
RUN python -m pip install qsharp azure-quantum \
    && python -m pip install ipykernel ipympl jupyterlab

# Exponemos el puerto 8888 (para Jupyter Notebook)
EXPOSE 8888

# Comando para ejecutar Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
