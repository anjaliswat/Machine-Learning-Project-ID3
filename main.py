#!/usr/bin/python

import argparse
import copy
import sys

import attributes
import dataset

parser = argparse.ArgumentParser(
           description='Train (and optionally test) a decision tree')
parser.add_argument('dtree_module',
                    metavar='dtree-module',
                    help='Decision tree module name')
parser.add_argument('classifier',
                    help='Name of the attribute to use for classification')
parser.add_argument('--attributes',
                    type=argparse.FileType('r'),
                    help='Name of the attribute specification file',
                    dest='attributes_file',
                    required=True)
parser.add_argument('--train',
                    type=argparse.FileType('r'),
                    help='Name of the file to use for training',
                    dest='training_file',
                    required=True)
parser.add_argument('--test',
                    type=argparse.FileType('r'),
                    dest='testing_file',
                    help='Name of the file to use for testing')
args = parser.parse_args()

# Read in a complete list of attributes.
# global all_attributes
all_attributes = attributes.Attributes(args.attributes_file)
if args.classifier not in all_attributes.all_names():
  sys.stderr.write("Classifier '%s' not a recognized attribute name\n" %
                   args.classifier)
  sys.exit(1)

classifier = all_attributes[args.classifier]

attributes_names = []
attributes = {}

for atr in all_attributes:
  temp_array = atr.values
  attribute_array = []
  for value in temp_array:
      attribute_array.append(value)
      attribute_array.append(0)
  atr = str(atr)
  atr = atr.split(" ")
  atr = atr[0]
  attributes[atr] = attribute_array
  attributes_names.append(atr)


del attributes_names[-1]

# Import the d-tree module, removing the .py extension if found
if args.dtree_module.endswith('.py') and len(args.dtree_module) > 3:
  dtree_pkg = __import__(args.dtree_module[:-3])
else:
  dtree_pkg = __import__(args.dtree_module)

# Train
training_data = dataset.DataSet(args.training_file, all_attributes)
starting_attrs = copy.copy(all_attributes)
starting_attrs.remove(classifier)
dtree = dtree_pkg.DTree(classifier, training_data, attributes, attributes_names)
dtree.construct_tree()

print dtree.dump()

if args.testing_file:
  testing_data = dataset.DataSet(args.testing_file, attributes)
  correct_results = dtree.test(classifier, testing_data)
  print("%d of %d (%.2f%%) of testing examples correctly identified" %
        (correct_results, len(testing_data),
         (float(correct_results) * 100.0)/ float(len(testing_data))))
