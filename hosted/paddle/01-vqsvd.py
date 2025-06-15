import numpy as np
from numpy import pi as PI
from matplotlib import pyplot as plt
from scipy.stats import unitary_group
from scipy.linalg import norm

import paddle
from paddle_quantum.ansatz import Circuit
from paddle_quantum.linalg import dagger

# 
# Draw the learning curve in the optimization process
def loss_plot(loss):
    '''
    loss is a list, this function plots loss over iteration
    '''
    plt.plot(list(range(1, len(loss)+1)), loss)
    plt.xlabel('iteration')
    plt.ylabel('loss')
    plt.title('Loss Over Iteration')
    plt.show()



def M_generator():
    I = np.array([[1, 0], [0, 1]])
    Z = np.array([[1, 0], [0, -1]])
    X = np.array([[0, 1], [1, 0]])
    Y = np.array([[0, -1j], [1j, 0]])
    M = 2 *np.kron(X, Z) + 6 * np.kron(Z, X) + 3 * np.kron(I, I)
    return M.astype('complex64')

print('The matrix M we want to decompose is: ')
print(M_generator())

# 
# We only need the following line of code to complete SVD
U, D, V_dagger = np.linalg.svd(M_generator(), full_matrices=True)


# Print decomposition results
print("The singular values of the matrix from large to small are:")
print(D)
print("The decomposed unitary matrix U is:")
print(U)
print("The decomposed unitary matrix V_dagger is:")
print(V_dagger)

# 
# Then assemble it back, can we restore the original matrix?
M_reconst = np.matmul(U, np.matmul(np.diag(D), V_dagger))
print(M_reconst)


np.random.seed(42)

# Set the number of qubits, which determines the dimension of the Hilbert space
N = 3

# Make a random matrix generator
def random_M_generator():
    M = np.random.randint(10, size = (2**N, 2**N)) + 1j*np.random.randint(10, size = (2**N, 2**N))
    return M

M = random_M_generator()
M_err = np.copy(M)


# Output the matrix M
print('The matrix M we want to decompose is:')
print(M)

# Apply SVD and record the exact singular values
U, D, V_dagger = np.linalg.svd(M, full_matrices=True)
print("The singular values of the matrix M are:")
print(D)

# 
# Hyperparameter settings
RANK = 8       # Set the number of rank you want to learn
ITR = 100   # Number of iterations
LR = 0.02   # Learning rate
SEED = 14   # Random seed

# Set the learning weight 
weight = np.arange(3 * RANK, 0, -3).astype('complex128')
print('The selected weight is:')
print(weight)

#  [markdown]
# We design QNN with the following structure:

# 
# Set circuit parameters
num_qubits = 3              # number of qubits
cir_depth = 20              # circuit depth

# 
# Define quantum neural network
def U_theta(num_qubits: int, depth: int) -> Circuit:

    # Initialize the network with Circuit
    cir = Circuit(num_qubits)
    
    # Build a hierarchy：
    for _ in range(depth):
        cir.ry()
        cir.rz()
        cir.cnot()

    return cir

#  [markdown]
# Then we complete the main part of the algorithm:

# 
class VQSVD():
    def __init__(self, matrix: np.ndarray, weights: np.ndarray, num_qubits: int, depth: int, rank: int, lr: float, itr: int, seed: int):
        
        # Hyperparameters
        self.rank = rank
        self.lr = lr
        self.itr = itr
        
        paddle.seed(seed)
        
        # Create the parameter theta for learning U
        self.cir_U = U_theta(num_qubits, depth)
        
        # Create a parameter phi to learn V_dagger
        self.cir_V = U_theta(num_qubits, depth)
        
        # Convert Numpy array to Tensor supported in Paddle
        self.M = paddle.to_tensor(matrix)
        self.weight = paddle.to_tensor(weights)

    # Define the loss function
    def loss_func(self):
        
        # Get the unitary matrix representation of the quantum neural network
        U = self.cir_U.unitary_matrix()
        V = self.cir_V.unitary_matrix()
    
        # Initialize the loss function and singular value memory
        loss = paddle.to_tensor(0.0)
        singular_values = np.zeros(self.rank)
        
        # Define loss function
        for i in range(self.rank):
            loss -= paddle.real(self.weight)[i] * paddle.real(dagger(U) @ self.M @ V)[i][i]
            singular_values[i] = paddle.real(dagger(U) @ self.M @ V)[i][i].numpy()
        
        # Function returns learned singular values and loss function
        return loss, singular_values
    
    def get_matrix_U(self):
        return self.cir_U.unitary_matrix()
    
    def get_matrix_V(self):
        return self.cir_V.unitary_matrix()
    
    # Train the VQSVD network
    def train(self):
        loss_list, singular_value_list = [], []
        optimizer = paddle.optimizer.Adam(learning_rate=self.lr, parameters=self.cir_U.parameters()+self.cir_V.parameters())
        for itr in range(self.itr):
            loss, singular_values = self.loss_func()
            loss.backward()
            optimizer.minimize(loss)
            optimizer.clear_grad()
            loss_list.append(loss.numpy()[0])
            singular_value_list.append(singular_values)
            if itr% 10 == 0:
                print('iter:', itr,'loss:','%.4f'% loss.numpy()[0])
                
        return loss_list, singular_value_list

# 
# Record the optimization process
loss_list, singular_value_list = [], []
U_learned, V_dagger_learned = [], []

# Construct the VQSVD network and train
net = VQSVD(matrix=M, weights=weight, num_qubits=num_qubits, depth=cir_depth, rank=RANK, lr=LR, itr=ITR, seed=SEED)
loss_list, singular_value_list = net.train()

# Draw a learning curve
loss_plot(loss_list)

# Record the last two learned unitary matrices
U_learned = net.get_matrix_U().numpy()
V_dagger_learned = dagger(net.get_matrix_V()).numpy()

singular_value = singular_value_list[-1]
err_subfull, err_local, err_SVD = [], [], []
U, D, V_dagger = np.linalg.svd(M, full_matrices=True)


# Calculate the Frobenius-norm error
for i in range(RANK):
    lowrank_mat = np.matrix(U[:, :i]) * np.diag(D[:i])* np.matrix(V_dagger[:i, :])
    recons_mat = np.matrix(U_learned[:, :i]) * np.diag(singular_value[:i])* np.matrix(V_dagger_learned[:i, :])
    err_local.append(norm(lowrank_mat - recons_mat)) 
    err_subfull.append(norm(M_err - recons_mat))
    err_SVD.append(norm(M_err- lowrank_mat))


# Plot
fig, ax = plt.subplots()
ax.plot(list(range(1, RANK+1)), err_subfull, "o-.", 
        label = 'Reconstruction via VQSVD')
ax.plot(list(range(1, RANK+1)), err_SVD, "^--", 
        label='Reconstruction via SVD')
plt.xlabel('Singular Value Used (Rank)', fontsize = 14)
plt.ylabel('Norm Distance', fontsize = 14)
leg = plt.legend(frameon=True)
leg.get_frame().set_edgecolor('k')


# Image processing package PIL
from PIL import Image

# Open the picture prepared in advance
img = Image.open('./figures/MNIST_32.png')
imgmat = np.array(list(img.getdata(band=0)), float)
imgmat.shape = (img.size[1], img.size[0])
imgmat = np.matrix(imgmat)/255

# 
# Then we look at the effect of the classic singular value decomposition
U, sigma, V = np.linalg.svd(imgmat)

for i in range(5, 16, 5):
    reconstimg = np.matrix(U[:, :i]) * np.diag(sigma[:i]) * np.matrix(V[:i, :])
    plt.imshow(reconstimg, cmap='gray')
    title = f"n = {i}"
    plt.title(title)
    plt.show()

# 
# Set circuit parameters
cir_depth = 40      # depth of circuit
num_qubits = 5      # Number of qubits

# Hyper-parameters
RANK = 8            # Set the number of rank you want to learn
ITR = 200           # Number of iterations
LR = 0.02           # Learning rate
SEED = 14           # Random number seed

# Set the learning weight
weight = np.arange(2 * RANK, 0, -2).astype('complex128')

# Convert the image into numpy array
def Mat_generator():
    imgmat = np.array(list(img.getdata(band=0)), float)
    imgmat.shape = (img.size[1], img.size[0])
    lenna = np.matrix(imgmat)
    return lenna.astype('complex128')

M_err = Mat_generator()
U, D, V_dagger = np.linalg.svd(Mat_generator(), full_matrices=True)

# 
# Define circuit of quantum neural network
def U_theta(num_qubits: int, depth: int) -> Circuit:

    # Initialize the network with Circuit
    cir = Circuit(num_qubits)
    
    # Build a hierarchy：
    for _ in range(depth):
        cir.ry()
        cir.cnot()

    return cir

# 
# Record the optimization process
loss_list, singular_value_list = [], []
U_learned, V_dagger_learned = [], []
    
# Construct the VQSVD network and train
net = VQSVD(matrix=Mat_generator(), weights=weight, num_qubits=num_qubits, depth=cir_depth, rank=RANK, lr=LR, itr=ITR, seed=SEED)
loss_list, singular_value_list = net.train()

# Record the last two unitary matrices learned
U_learned = net.get_matrix_U().numpy()
V_dagger_learned = dagger(net.get_matrix_V()).numpy()

singular_value = singular_value_list[-1]
mat = np.matrix(U_learned.real[:, :RANK]) * np.diag(singular_value[:RANK])* np.matrix(V_dagger_learned.real[:RANK, :])

reconstimg = mat
plt.imshow(reconstimg, cmap='gray')


# IMPORTANT DISCLAIMER:
# This code is base on the paper "Variational Quantum Singular Value Decomposition" by Wang, Song, and Wang [1].
# It is intended for educational purposes only and should not be used for commercial applications.

# ## References# 
# [1] Wang, X., Song, Z., & Wang, Y. Variational Quantum Singular Value Decomposition. [Quantum, 5, 483 (2021).](https://quantum-journal.org/papers/q-2021-06-29-483/)


