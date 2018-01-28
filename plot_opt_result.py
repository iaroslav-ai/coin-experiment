import matplotlib.pyplot as plt
import pickle as pc
import numpy as np

y = np.array([(0.333-0.128), (0.446-0.333), (0.333-0.181), (0.333-0.235), 0.03092448, 0.14420573, 0.01204427, 0.10123698, 0.06380208,
       0.00846354, 0.00748698, 0.16276042, 0.00260417, 0.01627604,
       0.01106771, 0.00846354, 0.01041667, 0.01627604, 0.00748698,
       0.02115885, 0.01204427, 0.0139974 , 0.07096354, 0.10611979])

x = np.array([[0.707], [1.154], [0.8], [0.9], [1.0923058339133385], [1.2468599995447698], [1.0279948921302733], [1.1575448215964406], [1.0], [1.0582700265151894], [1.0515717191642762], [1.3], [1.0436040442000285], [1.0434329027743154], [1.0564829616196934], [1.0529520952697302], [1.0683363715166259], [1.049553093963671], [1.070487144644817], [1.0703083106373923], [1.0505981566571503], [1.0345773843348864], [1.1093705179819866], [1.1994451595370388]])

plt.scatter(x[:, 0], y)
plt.show()