# NLP Programming Assignment #4
# NaiveBayesWithNegationFeature
# 2012

#
# The area for you to implement is marked with TODO!
# Generally, you should not need to touch things *not* marked TODO
#
# Remember that when you submit your code, it is not run from the command line
# and your main() will *not* be run. To be safest, restrict your changes to
# addExample() and classify() and anything you further invoke from there.
#


import sys
import getopt
import os
import re
import math
import nltk
from ImdbNaiveBayes import ImdbNaiveBayes

punctuation_pat = '[.?]+'
negation_pat = '(not|Not|n\'t|never)'


class NaiveBayesWithNegationFeature:
    imdb_naive_bayes = ImdbNaiveBayes()

    class TrainSplit:
        """Represents a set of training/testing data. self.train is a list of Examples, as is self.test.
        """

        def __init__(self):
            self.train = []
            self.test = []

    class Example:
        """Represents a document with a label. klass is 'pos' or 'neg' by convention.
           words is a list of strings.
        """

        def __init__(self):
            self.klass = ''
            self.words = []

    def __init__(self):
        """NaiveBayes initialization"""
        self.FILTER_STOP_WORDS = False
        self.stopList = set(self.readFile('../data/english.stop'))
        self.numFolds = 10

    #############################################################################
    # TODO TODO TODO TODO TODO

    def classify(self, words):
        """ TODO
          'words' is a list of words to classify. Return 'pos' or 'neg' classification.
        """
        score_pos, score_neg = self.imdb_naive_bayes.get_score(words)
        if score_pos > score_neg:
            return 'pos'
        else:
            return 'neg'

    def addExample(self, klass, words):
        """
        * TODO
        * Train your model on an example document with label klass ('pos' or 'neg') and
        * words, a list of strings.
        * You should store whatever data structures you use for your classifier
        * in the NaiveBayes class.
        * Returns nothing
        """
        self.imdb_naive_bayes.add_words(klass, self.filterStopWords(words))

    def filterStopWords(self, words):
        """
        * TODO
        * Filters stop words found in self.stopList.
        """
        new_words = []
        isNegation = False
        # word_tag_list = nltk.pos_tag(words)
        # for word, tag in word_tag_list:
        #     if re.match(negation_pat, word):
        #         isNegation = True
        #     if re.match(punctuation_pat, word):
        #         isNegation = False
        #     if word not in self.stopList:
        #         if isNegation and (tag.startswith('JJ') or tag.startswith('V')):
        #             word = 'NOT_' + word
        #         new_words.append(word)
        for word in words:
            if re.match(negation_pat, word):
                isNegation = True
            if re.match(punctuation_pat, word):
                isNegation = False
            if word not in self.stopList:
                word = 'NOT_' + word if isNegation else word
                new_words.append(word)
        return new_words

    # TODO TODO TODO TODO TODO
    #############################################################################

    def readFile(self, fileName):
        """
         * Code for reading a file.  you probably don't want to modify anything here,
         * unless you don't like the way we segment files.
        """
        contents = []
        f = open(fileName)
        for line in f:
            contents.append(line)
        f.close()
        result = self.segmentWords('\n'.join(contents))
        return result

    def segmentWords(self, s):
        """
         * Splits lines on whitespace for file reading
        """
        return s.split()

    def trainSplit(self, trainDir):
        """Takes in a trainDir, returns one TrainSplit with train set."""
        split = self.TrainSplit()
        posTrainFileNames = os.listdir('%s/pos/' % trainDir)
        negTrainFileNames = os.listdir('%s/neg/' % trainDir)
        for fileName in posTrainFileNames:
            example = self.Example()
            example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
            example.klass = 'pos'
            split.train.append(example)
        for fileName in negTrainFileNames:
            example = self.Example()
            example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
            example.klass = 'neg'
            split.train.append(example)
        return split

    def train(self, split):
        for example in split.train:
            words = example.words
            if self.FILTER_STOP_WORDS:
                words = self.filterStopWords(words)
            self.addExample(example.klass, words)

    def crossValidationSplits(self, trainDir):
        """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
        splits = []
        posTrainFileNames = os.listdir('%s/pos/' % trainDir)
        negTrainFileNames = os.listdir('%s/neg/' % trainDir)
        # for fileName in trainFileNames:
        for fold in range(0, self.numFolds):
            split = self.TrainSplit()
            for fileName in posTrainFileNames:
                example = self.Example()
                example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
                example.klass = 'pos'
                if fileName[2] == str(fold):
                    split.test.append(example)
                else:
                    split.train.append(example)
            for fileName in negTrainFileNames:
                example = self.Example()
                example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
                example.klass = 'neg'
                if fileName[2] == str(fold):
                    split.test.append(example)
                else:
                    split.train.append(example)
            splits.append(split)
        return splits

    def test(self, split):
        """Returns a list of labels for split.test."""
        labels = []
        for example in split.test:
            words = example.words
            if self.FILTER_STOP_WORDS:
                words = self.filterStopWords(words)
            guess = self.classify(words)
            labels.append(guess)
        return labels

    def buildSplits(self, args):
        """Builds the splits for training/testing"""
        trainData = []
        testData = []
        splits = []
        trainDir = args[0]
        if len(args) == 1:
            print '[INFO]\tPerforming %d-fold cross-validation on data set:\t%s' % (self.numFolds, trainDir)

            posTrainFileNames = os.listdir('%s/pos/' % trainDir)
            negTrainFileNames = os.listdir('%s/neg/' % trainDir)
            for fold in range(0, self.numFolds):
                split = self.TrainSplit()
                for fileName in posTrainFileNames:
                    example = self.Example()
                    example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
                    example.klass = 'pos'
                    if fileName[2] == str(fold):
                        split.test.append(example)
                    else:
                        split.train.append(example)
                for fileName in negTrainFileNames:
                    example = self.Example()
                    example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
                    example.klass = 'neg'
                    if fileName[2] == str(fold):
                        split.test.append(example)
                    else:
                        split.train.append(example)
                splits.append(split)
        elif len(args) == 2:
            split = self.TrainSplit()
            testDir = args[1]
            print '[INFO]\tTraining on data set:\t%s testing on data set:\t%s' % (trainDir, testDir)
            posTrainFileNames = os.listdir('%s/pos/' % trainDir)
            negTrainFileNames = os.listdir('%s/neg/' % trainDir)
            for fileName in posTrainFileNames:
                example = self.Example()
                example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
                example.klass = 'pos'
                split.train.append(example)
            for fileName in negTrainFileNames:
                example = self.Example()
                example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
                example.klass = 'neg'
                split.train.append(example)

            posTestFileNames = os.listdir('%s/pos/' % testDir)
            negTestFileNames = os.listdir('%s/neg/' % testDir)
            for fileName in posTestFileNames:
                example = self.Example()
                example.words = self.readFile('%s/pos/%s' % (testDir, fileName))
                example.klass = 'pos'
                split.test.append(example)
            for fileName in negTestFileNames:
                example = self.Example()
                example.words = self.readFile('%s/neg/%s' % (testDir, fileName))
                example.klass = 'neg'
                split.test.append(example)
            splits.append(split)
        return splits


def main():
    nb = NaiveBayesWithNegationFeature()

    # default parameters: no stop word filtering, and
    # training/testing on ../data/imdb1
    if len(sys.argv) < 2:
        options = [('', '')]
        args = ['../data/imdb1/']
    else:
        (options, args) = getopt.getopt(sys.argv[1:], 'f')
    if ('-f', '') in options:
        nb.FILTER_STOP_WORDS = True

    splits = nb.buildSplits(args)
    avgAccuracy = 0.0
    fold = 0
    for split in splits:
        classifier = NaiveBayesWithNegationFeature()
        accuracy = 0.0
        for example in split.train:
            words = example.words
            if nb.FILTER_STOP_WORDS:
                words = classifier.filterStopWords(words)
            classifier.addExample(example.klass, words)

        for example in split.test:
            words = example.words
            if nb.FILTER_STOP_WORDS:
                words = classifier.filterStopWords(words)
            guess = classifier.classify(words)
            if example.klass == guess:
                accuracy += 1.0

        accuracy = accuracy / len(split.test)
        avgAccuracy += accuracy
        print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy)
        fold += 1
    avgAccuracy = avgAccuracy / fold
    print '[INFO]\tAccuracy: %f' % avgAccuracy


if __name__ == "__main__":
    # nltk.download('all')
    main()
