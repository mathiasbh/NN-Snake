
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd

datafile = '__models/04102020_10snakes_simplevision/_fitness.csv'
df = pd.read_csv(datafile)


N = 15
x = df["#generation"]

def movingmean(x, N):
    #return(np.convolve(x, np.ones((N,))/N, mode='valid')[(N-1):])
    return(x.rolling(N).mean())



fig, (ax1, ax2) = plt.subplots(2,1, figsize=(16,16))

# Plot 1
ax1.plot(x, df["fitness_mean"], 'b.', alpha=0.3)
ax1.plot(x, df["fitness_median"], 'r.', alpha=0.3)
ax1.plot(x, movingmean(df["fitness_mean"], N), 'b-', alpha=1, label="mean fitness")
ax1.plot(x, movingmean(df["fitness_median"], N), 'r-', alpha=1, label="median fitness")


# Settings
#ax1.set_xlabel("Generation")
ax1.set_ylabel("Fitness")
ax1.set_xticks(np.arange(0, max(x), step=50))
ax1.legend(loc="upper left")
ax1.set_ylim([0, max(df["fitness_mean"]*1.1)])
ax1.set_xlim([0, max(x)])
ax1.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))

# Plot 2
ax2.plot(x, df["fitness_max"], 'k.', alpha=0.3)
ax2.plot(x, movingmean(df["fitness_max"], N), 'k-', alpha=1, label="max fitness",)

# Settings
ax2.set_xlabel("Generation")
ax2.set_ylabel("Fitness")
ax2.set_xticks(np.arange(0, max(x), step=50))
ax2.legend(loc="upper left")
ax2.set_ylim([0, max(df["fitness_max"])*1.1])
ax2.set_xlim([0, max(x)])
ax2.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))

plt.savefig('Fitness_generation.png', format='png')



fig2, (ax3) = plt.subplots(1,1, figsize=(16,8))

# Plot 
ax3.plot(x, df["score_mean"], 'b.', alpha=0.3)
ax3.plot(x, df["score_median"], 'r.', alpha=0.3)
ax3.plot(x, movingmean(df["score_mean"], N), 'b-', alpha=1, label="mean score")
ax3.plot(x, movingmean(df["score_median"], N), 'r-', alpha=1, label="median score")
ax3.plot(x, df["score_max"], 'k.', alpha=0.3)
ax3.plot(x, movingmean(df["score_max"], N), 'k-', alpha=1, label="max score",)

# Settings
ax3.set_xlabel("Generation")
ax3.set_ylabel("Score")
ax3.set_xticks(np.arange(0, max(x), step=50))
ax3.legend(loc="upper left")
ax3.set_ylim([0, max(df["score_max"])*1.1])
ax3.set_xlim([0, max(x)])

plt.savefig('Score_generation.png', format='png')
plt.show()




# fig, ax = plt.subplots()
# ax.plot(x, df["score_mean"], 'b.', label="mean score", alpha=0.25)
# ax.plot(x, df["score_median"], 'r.', label="median score", alpha=0.25)
# #ax.plot(df["#generation"], df["fitness_max"], 'k.', label="max fitness", alpha=0.25)
# #ax.ticklabel_format(axis="y", style="sci")
# ax.legend(loc="upper left")
# plt.show()