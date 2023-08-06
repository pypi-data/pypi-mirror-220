## Using catsim objects outside of a Simulator
# this function generates an item bank, in case the user cannot provide one
from catsim.cat import generate_item_bank
# simulation package contains the Simulator and all abstract classes
from catsim.simulation import *
# initialization package contains different initial proficiency estimation strategies
from catsim.initialization import *
# selection package contains different item selection strategies
from catsim.selection import *
# estimation package contains different proficiency estimation methods
from catsim.estimation import *
# stopping package contains different stopping criteria for the CAT
from catsim.stopping import *
import catsim.plot as catplot
from catsim.irt import icc
import random

import matplotlib.pyplot as plt
import pandas as pd
items = pd.read_csv('items.csv')
items = items[['measure', 't1', 't2', 't3']].to_numpy()
responses =          [0, 2]
administered_items = [0, 1]

initializer = FixedPointInitializer(0)
selector = MaxInfoSelector()
estimator = NumericalSearchEstimator(method='partial_credit')
stopper = MinErrorStopper(.2)

est_theta = initializer.initialize()
print('Examinee initial proficiency:', est_theta)
est_theta = estimator.estimate(items=items, administered_items=administered_items, response_vector=responses, est_theta=est_theta)
print('Estimated sample location, given answered items:', -1*est_theta)

_stop = stopper.stop(administered_items=items[administered_items], theta=est_theta)
print('Should the test be stopped:', _stop)

item_index = selector.select(items=items, administered_items=administered_items, est_theta=est_theta)
print('Next item to be administered:', item_index)


administered_items.append(item_index)
responses.append(2)
