import pandas as pd
import matplotlib.pyplot as plt 
import os


   
def plot_means(file_path, param):
    df = pd.read_csv(file_path, delimiter=',', header = 0)
    means = (df.groupby(param).mean())
    label = file_path.split("/")[1].split(".")[0]
    plt.plot(means.index, means['mean'], label = label)

data_files = os.listdir("data")
m_files, n_files, p_max_files = [], [], []

for file in data_files:
    if "_n.csv" in file:
        n_files.append(file)
    elif "_m.csv" in file:
        m_files.append(file)
    else:
        p_max_files.append(file)

for file in n_files:
    plot_means(f'data/{file}', 'n')
plt.legend()
plt.show()

for file in m_files:
    plot_means(f'data/{file}', 'm')
plt.legend()
plt.show()

for file in p_max_files:
    plot_means(f'data/{file}', 'p_max')
plt.legend()
plt.show()
