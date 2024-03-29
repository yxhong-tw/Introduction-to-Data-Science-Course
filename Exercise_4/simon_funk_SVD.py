import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Try to change the value of alpha
def mf_sgd(R, K=64, alpha=1e-4, beta=1e-2, iterations=50):
    """
    :param R: user-item rating matrix
    :param K: number of latent dimensions
    :param alpha: learning rate
    :param beta: regularization parameter
    """
    num_users, num_items = R.shape

    # Initialize user and item latent feature matrice
    P = np.random.normal(scale=1. / K, size=(num_users, K))
    Q = np.random.normal(scale=1. / K, size=(num_items, K))

    # Initialize the biases
    b_u = np.zeros(num_users)
    b_i = np.zeros(num_items)
    b = np.mean(R[np.where(R != 0)])

    # Create a list of training samples
    samples = [
        (i, j, R[i, j])
        for i in range(num_users)
        for j in range(num_items)
        if R[i, j] > 0
    ]

    # Perform stochastic gradient descent for number of iterations
    training_loss = []
    
    for iters in range(iterations):
        np.random.shuffle(samples)

# My code start
        loss = 0
# My code end

        for i, j, r in samples:
            """
            TODO: 
            In this for-loop scope, 
            you need to (1)update "b_u"(vector of rating bias for users) and "b_i"(vector of rating bias for items)
            and (2)update user and item latent feature matrices "P", "Q"
            """

# My code start
            # Comment out pred = 0
            # pred = 0

            # Calculate prediction and error
            hat_r = b + b_u[i] + b_i[j] + np.dot(P[i, :], Q[j, :])
            d_ij = r - hat_r

            # Calculate gradients
            gradient_b_u = -d_ij + (beta * b_u[i])
            gradient_b_i = -d_ij + (beta * b_i[j])
            gradient_P = -d_ij * Q[j, :] + (beta * P[i, :])
            gradient_Q = -d_ij * P[i, :] + (beta * Q[j, :])
            
            # Update all variables
            b_u[i] -= alpha * gradient_b_u
            b_i[j] -= alpha * gradient_b_i
            P[i, :] -= alpha * gradient_P
            Q[j, :] -= alpha * gradient_Q

            # Calculate loss
            loss += ((r - b - b_u[i] - b_i[j] - np.dot(P[i, :], Q[j, :])) ** 2)

        # Calculate loss
        loss /= len(samples)
        loss = loss ** 0.5

        temp = [iters, loss]
        training_loss.append(temp)

    pred = np.dot(P, Q.transpose())
# My code end

    return pred, b, b_u, b_i, training_loss


def plot_training_loss(training_loss):
    x = [x for x, y in training_loss]
    y = [y for x, y in training_loss]
    plt.figure(figsize=(16, 4))
    plt.plot(x, y)
    plt.xticks(x, x)
    plt.xlabel("Iterations")
    plt.ylabel("Root Mean Square Error")
    plt.grid(axis="y")
    plt.savefig("training_loss.png")
    plt.show()


if __name__ == "__main__":
    data = pd.read_csv('ratings.csv')
    table = pd.pivot_table(data, values='rating', index='userId', columns='movieId', fill_value=0)
    R = table.values

    pred, b, b_u, b_i, loss = mf_sgd(R,iterations=50)
    print("P x Q:")
    print(pred)
    print("Global bias:")
    print(b)
    print("User bias:")
    print(b_u)
    print("Item bias:")
    print(b_i)
    plot_training_loss(loss)
