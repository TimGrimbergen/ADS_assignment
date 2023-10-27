import pandas as pd
import matplotlib.pyplot as plt 
import os


def plot_means(file_path, param):
    df = pd.read_csv(file_path, delimiter=',', header = 0)[[param,'mean']]
    means = (df.groupby(param).mean())
    stds = (df.groupby(param).std())
    print(stds)
    label = file_path.split("/")[1].split(".")[0]
    mean_min_std = means['mean'] - stds['mean']
    mean_plus_std = means['mean'] + stds['mean']
    plt.plot(means.index, means['mean'], label = label)
    plt.fill_between(stds.index, mean_min_std, mean_plus_std, alpha=0.2)
    plt.xlabel(f"${param}$")
    plt.ylabel("Average competitive ratio")
    plt.xlim(min(means.index), max(means.index))
    plt.ylim(1, 1.1*max(mean_plus_std))
    plt.xscale('log')
    plt.yscale('log')

def violin_plot_data(save_location, file_name, data):
    labels = [point[1] for point in data]
    data = [point[0]['mean'] for point in data]
    plt.figure(dpi=300).subplots_adjust(bottom=0.2)
    plt.violinplot(data, showmeans=True)
    plt.rcParams.update({'xtick.labelsize': 'small'})
    plt.xticks(ticks = range(1, len(data) + 1), labels = labels)
    plt.title("Violin plot of observed competitive ratios")
    plt.ylabel("Average competitive ratio")
    plt.yscale('log')
    plt.savefig(f'{save_location}/{file_name}')

data_files = os.listdir("data")
m_files, n_files, p_max_files, violin_files = [], [], [], []

for file in data_files:
    if "_n.csv" in file:
        n_files.append(file)
    elif "_m.csv" in file:
        m_files.append(file)
    elif "_p_max.csv" in file:
        p_max_files.append(file)
    else:
        violin_files.append(file)

plt.figure()
for file in n_files:
    plot_means(f'data/{file}', 'n')
plt.legend()
plt.savefig("figures/chpt6/n", dpi=300)
#plt.show()

plt.figure()
for file in m_files:
    plot_means(f'data/{file}', 'm')
plt.legend()
plt.savefig("figures/chpt6/m", dpi=300)
#plt.show()

plt.figure()
for file in p_max_files:
    plot_means(f'data/{file}', 'p_max')
plt.legend()
plt.savefig("figures/chpt6/pmax", dpi=300)
#plt.show()

violin_data = []

for file in violin_files:
    label = file.split("_violin")[0]
    df = pd.read_csv(f'data/{file}', delimiter=',', header = 0)
    violin_data.append((df, label))
violin_plot_data("figures", "violin.png", violin_data)