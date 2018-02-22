from __future__ import division
import math
import copy
import dataset
from dataset import DataSet


class DTree:
  'Represents a decision tree created with the ID3 algorithm'

  def __init__(self, classifier, training_data, attributes , attributes_names):
    self.attributes = attributes
    self.attributes_names = attributes_names
    self.training_data = training_data
    self.classifier_values = classifier.values
    self.classifier_name = str(classifier)
    self.classifier_name = self.classifier_name.split(" ")
    self.classifier_name = self.classifier_name[0]

  def probability_set(self, target, data_set):
    attributes = copy.deepcopy(self.attributes)
    total_traits = len(data_set)
    probability = []

    i = 0
    while i < len(attributes[target]):
        j = 0
        while j < len(data_set):
            if data_set.all_examples[j].values[target] == attributes[target][i]:
                attributes[target][i+1] = attributes[target][i+1] + 1
            j = j + 1
        i = i + 2

    i = 0
    while i < len(attributes[target]):
        probability.append(attributes[target][i])
        prob = attributes[target][i+1]/total_traits
        probability.append(prob)
        i = i + 2

    return probability

  def probability_subset(self, target, data_set):
    attributes = copy.deepcopy(self.attributes)
    classifier = self.classifier_name
    total_traits = len(data_set)
    probability = []
    classifier_traits = []

    i = 0

    while i < len(self.classifier_values):
        classifier_traits.append(0)
        i = i + 1

    i = 0
    while i < len(attributes[target]):
        array = copy.deepcopy(classifier_traits)
        attributes[target][i+1] = array
        i = i + 2

    i = 0
    while i < len(attributes[target]):
        j = 0
        while j < len(self.classifier_values):
            k = 0
            while k < len(data_set):
                if self.classifier_values[j] == data_set.all_examples[k].values[classifier]:
                    if data_set.all_examples[k].values[target] == attributes[target][i]:
                        attributes[target][i+1][j] = attributes[target][i+1][j] + 1
                k = k + 1
            j = j + 1
        i = i + 2

    i = 0
    while i < len(attributes[target]):
        total = 0
        prob = []
        for value in attributes[target][i+1]:
            total = total + value
        for value in attributes[target][i+1]:
            prob.append(value/total)
        probability.append(prob)
        i = i + 2

    return probability

  def entropy(self, data_set_probability, set_type):
    entropy = 0
    entropy_set = 0
    entropy_subset = []
    temp = 0
    if set_type == "set":
        for prob in data_set_probability:
            if type(prob) == int or type(prob) == float:
                entropy_set = entropy_set - (prob * math.log(prob, 2.0))
        entropy = entropy_set

    if set_type == "subset":
        for prob_list in data_set_probability:
            temp_entropy = 0
            for prob in prob_list:
                temp_entropy = temp_entropy - (prob * math.log(prob, 2.0))
            entropy_subset.append(temp_entropy)
        entropy = entropy_subset

    return entropy

  def information_gain(self, set_entropy,subset_entropy,set_probability):
    temp = 0
    gain = 0
    i = 0
    j = 0

    while j < len(set_probability):
     temp = temp - set_probability[j+1] * subset_entropy[i]
     i = i + 1
     j = j + 2
    gain = set_entropy + temp
    return "%.5f" % gain

  def max_gain(self, attributes_queue, sub_attributes_queue, information_gain_array, data_set):
      attributes = copy.deepcopy(self.attributes)

      for attribute in attributes_queue:
          classifier_set_prob = self.probability_set(self.classifier_name, data_set)
          target_set_prob = self.probability_set(attribute, data_set)
          subset_prob = self.probability_subset(attribute, data_set)
          set_entropy = self.entropy(classifier_set_prob,"set")
          subset_entropy = self.entropy(subset_prob,"subset")
          gain = self.information_gain(set_entropy, subset_entropy, target_set_prob)
          information_gain_array.append(gain)

      max_value = max(information_gain_array)
      max_index = information_gain_array.index(max_value)
      node = attributes_queue.pop(max_index)

      for sub_attribute in attributes[node]:
          if type(sub_attribute) == str:
              sub_attributes_queue.append(sub_attribute)

      return node

  def construct_tree(self):
      attributes_queue = copy.deepcopy(self.attributes_names)
      sub_attributes_queue = []
      data_set = self.training_data

      while len(attributes_queue) != 0:

          information_gain_array = []
          node = self.max_gain(attributes_queue, sub_attributes_queue, information_gain_array, data_set)

          print "NODE"
          print node

          while len(sub_attributes_queue) != 0:
            current_attribute = sub_attributes_queue.pop(0)
            print "current_attribute"
            print current_attribute

            i = 0

            temp_data_set = copy.deepcopy(data_set)

            while i < len(data_set):
                if data_set.all_examples[i].values[node] != current_attribute:
                    del(temp_data_set.all_examples[i])

                    #within new data set call self.max_gain
                print temp_data_set.all_examples[i].values

                #print data_set.all_examples[i].values
                i = i + 1

  def test(self, classifier, testing_data):
    return 0

  def dump(self):
    return ""
