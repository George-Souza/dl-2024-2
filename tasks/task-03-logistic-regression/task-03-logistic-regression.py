import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs

class LogisticNeuron:
    def __init__(self, input_dim, learning_rate=0.1, epochs=1000):
        """
        Inicializa os pesos, bias, taxa de aprendizado e número de épocas.
        """
        self.weights = np.random.randn(input_dim) * 0.01  # Pesos pequenos aleatórios
        self.bias = 0.0  # Bias inicializado como zero
        self.learning_rate = learning_rate
        self.epochs = epochs
    
    def sigmoid(self, z):
        """
        Calcula a função sigmoide.
        """
        return 1 / (1 + np.exp(-z))
    
    def predict_proba(self, X):
        """
        Calcula as probabilidades usando a saída do modelo.
        """
        z = np.dot(X, self.weights) + self.bias
        return self.sigmoid(z)
    
    def predict(self, X):
        """
        Faz previsões binárias (0 ou 1) com base em um limite de 0.5.
        """
        probabilities = self.predict_proba(X)
        return (probabilities >= 0.5).astype(int)
    
    def train(self, X, y):
        """
        Treina o modelo usando gradiente descendente.
        """
        m = X.shape[0]  # Número de exemplos
        
        for epoch in range(self.epochs):
            # Cálculo da saída do modelo
            z = np.dot(X, self.weights) + self.bias
            predictions = self.sigmoid(z)
            
            # Gradientes
            dw = (1 / m) * np.dot(X.T, (predictions - y))
            db = (1 / m) * np.sum(predictions - y)
            
            # Atualização dos pesos e bias
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db
            
            # Impressão opcional do erro a cada 100 épocas
            if (epoch + 1) % 100 == 0:
                loss = -np.mean(y * np.log(predictions) + (1 - y) * np.log(1 - predictions))
                print(f"Epoch {epoch + 1}/{self.epochs}, Loss: {loss:.4f}")


def generate_dataset():
    X, y = make_blobs(n_samples=200, centers=2, random_state=42, cluster_std=2.0)
    return X, y

def plot_decision_boundary(model, X, y):
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100), np.linspace(y_min, y_max, 100))
    
    Z = model.predict_proba(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    plt.contourf(xx, yy, Z, levels=20, cmap='coolwarm', alpha=0.7)
    plt.colorbar(label='Logistic Regression Output')
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap='bwr', edgecolors='k')
    plt.title('Logistic Regression Decision Boundary')
    plt.show()

def plot_loss(model):
    plt.plot(model.loss_history, 'k.')
    plt.xlabel('Iterations')
    plt.ylabel('Loss')
    plt.title('Loss over Training Iterations')
    plt.show()

# Generate dataset
X, y = generate_dataset()

# Train the model
neuron = LogisticNeuron(input_dim=2, learning_rate=0.1, epochs=100)
neuron.train(X, y)

# Plot decision boundary
plot_decision_boundary(neuron, X, y)

# Plot loss over training iterations
plot_loss(neuron)
