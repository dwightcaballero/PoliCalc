import matplotlib.pyplot as plt

plt.figure(figsize=(5, 5))

labels = ["POSITIVE", "NEGATIVE", "NEUTRAL"]
values = [31.27, 43.24, 25.48]
explode = [0, 0, 0]
colors = ["b", "r", "g"]

plt.pie(values, labels=labels, autopct="%.1f%%", explode=explode, colors=colors)

plt.show()
