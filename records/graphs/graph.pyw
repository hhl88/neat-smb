import math
import matplotlib.pyplot as plt
import numpy as np
import os
import ast
import sys


save_path = os.getcwd()
sub_path = "/records/graphs"
if not os.path.exists(save_path+ sub_path):
    os.makedirs(save_path + sub_path)
with open(save_path + sub_path + '/results.json', 'r') as f:
	s = f.read()
	loaded_results = ast.literal_eval(s)

fig = plt.figure(facecolor='white')

ax = plt.subplot(1, 1, 1)
max_fitness = []
average_fitness = []
for x in loaded_results.values():
    max_fitness.append(x[0])
    average_fitness.append(x[1])


ax.plot(loaded_results.keys(), max_fitness)
ax.plot(loaded_results.keys(), average_fitness)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.73, box.height])

# ax.legend(['max fitness', 'average fitness'], loc='center left', bbox_to_anchor=(1, 0.5))
max_length = len(loaded_results)
max_interval = 10 ** max(0, (len(str(max_length)) - 2))
print "max interval = %d" % max_interval
# min_interval = max_length / 2
max_length = int(math.ceil(max_length /float(max_interval) + 1) * max_interval)
print "max length = %d" % max_interval

ax.legend(['max fitness', 'average fitness'], loc='center left', bbox_to_anchor=(1, 0.5))
major_ticks = np.arange(0, max_length, max_interval)
# minor_ticks = np.arange(0, max_length, min_interval)
ax.set_xticks(major_ticks)

# ax.set_xticks(minor_ticks, minor=True)
ax.set_xlim(xmin=1)
print "max_length= %s" % max_length

plt.title('NEAT Generation')
plt.ylabel('Fitness')
plt.xlabel('Generation')
plt.show(transparent=True, facecolor='white')
# max_length = 30
# max_interval = 10
# max_length1 = int(math.ceil(max_length /float(max_interval))* max_interval)
# max_length2 = max_length // max_interval + (max_length % max_interval > 0)
# print "max_length1 = %d" % max_length1
# print "max_length2 = %d" % max_length2
sys.exit(0)
