import matplotlib.pyplot as plt
import pickle as pc
import numpy as np

# available experimental data
x = np.array([[0.707], [1.154], [0.8], [0.9], [1.0923058339133385], [1.2468599995447698], [1.0279948921302733], [1.1575448215964406], [1.0], [1.0582700265151894], [1.0515717191642762], [1.3], [1.0436040442000285], [1.0434329027743154], [1.0564829616196934], [1.0529520952697302], [1.0683363715166259], [1.049553093963671], [1.070487144644817], [1.0703083106373923], [1.0505981566571503], [1.0345773843348864], [1.1093705179819866], [1.1994451595370388]])
y = np.array([(0.333-0.128), (0.446-0.333), (0.333-0.181), (0.333-0.235), 0.03092448, 0.14420573, 0.01204427, 0.10123698, 0.06380208,
       0.00846354, 0.00748698, 0.16276042, 0.00260417, 0.01627604,
       0.01106771, 0.00846354, 0.01041667, 0.01627604, 0.00748698,
       0.02115885, 0.01204427, 0.0139974 , 0.07096354, 0.10611979])


# convert to absolute value of fraction of standing coins
# this is necessary due to the way how optimization works
best_y_i = np.argmin(y)
I = x[:, 0] < x[best_y_i, 0]
y[I] *= -1
y += 0.333

print('Best thickness: %s' % x[best_y_i, 0])
print('Best fraction: %s' % y[best_y_i])

# end of wizardry, plot the graph
# make the figure
plt.figure(figsize=(8,5))

# set the title of the figure
plt.title('Fraction of coins landing on the edge w.r.t. thickness of coin')

# plot the data points
plt.scatter(x[:, 0], y, label='Simulator data')
plt.scatter(x[:2, 0], [0.132, 0.41], label='Data from standupmaths et al.', marker='*', linewidths=3)

# plot the vertical and horizontal lines
plt.axvline(x[best_y_i], label='Best match to 0.33', dashes=[5, 5], c='r')
plt.axhline(0.333, dashes=[5, 5], c='r')

# add the text of best matching thickness
plt.text(x[best_y_i]+0.01, 0.125, str(x[best_y_i, 0]))

# add labels to the axes
plt.xlabel('Thickness of a coin')
plt.ylabel('Fraction of coins that land on edge')

# add legends and grid
plt.legend()
plt.grid()

# show the graph
plt.show()