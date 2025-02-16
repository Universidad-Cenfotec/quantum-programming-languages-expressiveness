# quantum-programming-languages-expressiveness
This repository aims to compare the expressiveness of different quantum programming languages, both hosted and non-hosted, analyzing their capabilities, strengths, and limitations. Doing an implementation of quantum algorithm



# Steps to run the code

## Hosted programming languages
## Qiskit and Cirq
Qiskit and Cirq as based on Python for installing the dependecies we highltly recommend to create a virtual environment.
#### On Windows
0. Install python. This experiment was run in python 3.12.8
1. Go to the project folder and and open a terminal 
2. python -m venv .venv 
3. cd quantum-programming-languages-expressiveness
4. .venv\Scripts\activate  
5. Install: python hosted/qiskit/requirements.txt

#### On Mac and Linux
0. Install python. This experiment was run in python 3.12.8
1. Navigate to your project directory
2. python3 -m venv venv  
3. source venv/bin/activate  
4. Install the hosted/qiskit/requirements.txt

## Cirq

## Qapl

## Qrisp

## Standalone programming languages

## Q#

## Quipper

## Silq


## ######################### create docker container ##################################
00. ubicarse donde esta docker

01. docker build -t my-quantum .

02. docker run -p 8888:8888 -v "C:\Users\danny.valerio\Documents\Danny\Quamtum\expressiveness-repo\quantum-programming-languages-expressiveness":/workspace --name my-quantum-c my-quantum


## # others
docker start my-quantum-c // inicar
docker stop my-quantum-c


docker ps // ver estatus

--docker exec -it my-quantum-c bash
--jupyter notebook --ip=0.0.0.0 --no-browser --allow-root

docker logs my-quantum-c
