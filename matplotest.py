import matplotlib.pyplot as plt
import numpy as np


#============================#
# normal histogram and curve #
#============================#
mat1 = np.random.rand(10,10)

mu = 10
sigma = 2
norm_sample = np.random.normal(mu, sigma, 1000)

plt.figure(num=1)
plt.style.use("ggplot")
plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)

num_bins = 300
count, bins, ignored = plt.hist(norm_sample, bins=num_bins, normed=True, color="blue", alpha=0.3, histtype="stepfilled", edgecolor="000000") # stepfilled
plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ), linewidth=2, color='r')
plt.xlabel(r"$x$")
plt.xlabel(r"$f(x)$")
plt.title(r"$Normal$")
ticks4x = ["idx" + str(loop) for loop in range(num_bins+1)]
plt.xticks([bins[0], bins[15], bins[30]], ["low", "middle", "high"])
plt.show()
plt.close()
#fig, ax1 = plt.subplots(figsize=(15,10.5))


#==========================================#
# modify position of axis and subplot2grid #
#==========================================#
# x = np.arange(1,10)
x = np.linspace(-5,5,50)
y = x**2 + 5

# gca: get current axis
plt.figure(num=2)
#plt.subplots_adjust(bottom=0.6, right=0.5, top=0.9)
#plt.style.use("")
ax1 = plt.subplot2grid((4,4),(0,0),rowspan=1,colspan=3)

plt.plot(x)
ax = plt.gca()
ax.xaxis.set_ticks_position("top")

ax2 = plt.subplot2grid((4,4),(1,0),rowspan=3,colspan=3)

l1, = plt.plot(x,y,linewidth=2,label=r"$y=x^2+5$")
plt.legend(handles=[l1,],labels=[r"y",],loc="best")
#plt.xlabel(r"$x$")
#plt.ylabel(r"$f(x)$")
#ax2.set_xlabel(r"$x$")
#ax2.set_ylabel(r"$f(x)$")
ax = plt.gca()
ax.spines["top"].set_color("none")
ax.spines["right"].set_color("none")
ax.xaxis.set_ticks_position("bottom")
ax.spines["bottom"].set_position(("axes",0.5)) # outward
ax.yaxis.set_ticks_position("left")
ax.spines["left"].set_position(("data",0))

ax3 = plt.subplot2grid((4,4),(1,3),rowspan=3,colspan=1)
plt.plot(y)
ax = plt.gca()
ax.yaxis.set_ticks_position("right")

plt.show()

plt.close(2)