#!/usr/bin/python
# -*- coding: utf-8 -*-

#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from random import choice
from sys import stdin
from time import sleep

class word:
    def __init__(self, value=""):
        """
        A word saves what precedes and what follows itself.
        It also knows its position inside a sentence.
        """

        # this list holds sentence fragments occuring after this word
        # imagine the word being before the list
        self.nextFragments = []

        # this list holds sentence fragments occuring before this word
        # imagine the word being after the list
        self.prevFragments = []

        # keys are possible positions in sentences
        # values hold how often the word occurred
        self.positions = {}

        self.value = value

    def __repr__(self):
        return self.value + str(self.positions.keys())

    def __str__(self):
        return self.value

    def addNextFragment(self, nextWord):
        """Adds Fragment following this word."""
        self.nextFragments.append(nextWord)

    def addPrevFragment(self, prevWord):
        """Adds Fragment preceding this word."""
        self.prevFragments.append(prevWord)

    def getNextFragments(self):
        """Gets all Fragments following this word."""
        return self.nextFragments

    def getPrevFragments(self):
        """Gets Fragments preceding this word."""
        return self.prevFragments

    def getNextRandomFragment(self):
        randomFragment = choice(self.nextFragments)
        return randomFragment

    def getPrevRandomFragment(self):
        randomFragment = choice(self.prevFragments)
        return randomFragment

    def addPosition(self, position):
        try:
            self.positions[position] += 1
        except KeyError:
            self.positions[position] = 1

    def getPositions(self):
        return self.positions

class dictionary:
    def __init__(self, debug=False):
        """
        A Dissociated Press dictionary contains a python dictionary of words.
        Sentences (strings) can be associated into or out of it.
        """
        self.words = {}
        self.debug = debug

    def __repr__(self):
        return str(self.words)

    def __getitem__(self, key):
        return self.words[key]

    def getWordsAtPosition(self, position):
        """Get all words that may occur at one position."""

        wordsAtPosition = []

        for w in self.words:
            if position in self.words[w].getPositions().keys():
                wordsAtPosition.append(w)

        return wordsAtPosition

    def dissociate(self, string, separator=" ", N=1):
        """
        Dissociate a sentence into this dictionary.

        N tells how many words are fused back together into a Fragment.
        """

        sentence = string.split(separator)

        # pad list with empty elements
        rest = len(sentence) % N

        for i in range(N-rest):
            sentence.append("")

        # fuse words into parts of N size each
        # kudos to Ronny Pfannschmidt for figuring this out
        sentence = [separator.join(x) for x in zip(*[iter(sentence)]*N)]

        # remove erroneous separators introduced through padding
        sentence[-1] = sentence[-1].rstrip()

        for i, token in enumerate(sentence):

            if token not in self.words:
                w = self.words[token] = word(token)
            else:
                w = self.words[token]

            if i > 0:
                if self.debug:
                    print sentence[i-1],
                w.addPrevFragment(sentence[i-1])
            else:
                if self.debug:
                    print "@ START",

            if self.debug:
                print "->", sentence[i], "@", i, "->",

            if (i+1) < len(sentence):
                if self.debug:
                    print sentence[i+1]
                w.addNextFragment(sentence[i+1])
            else:
                if self.debug:
                    print "@ ENDE"

            w.addPosition(i)

    def associate(self, next=True, prev=False, separator=" ", startWord="", ttl=255):
        """
        Associate a sentence from the dictionary using separators.

        The next and prev parameter control if next and previous fragments
        are considered during the process of association.
        WARNING: 

        The startWord parameter provides an optional entry point.
        The ttl parameter is a limit for the number of iterations.
        """

        # we need a first word
        if startWord:
            w = startWord
        else:
            w = choice(self.getWordsAtPosition(0))

        self.sentence = w
        self.entryPoint = w

        for i in range(ttl):
            if w:
                if prev:
                    try:
                        w = self.words[w].getPrevRandomFragment()
                        if w: self.sentence = w + separator + self.sentence
                    except IndexError: # occurs when looking up an empty word
                        pass

        w = self.entryPoint

        for i in range(ttl):
            if w:
                if next:
                    try:
                        w = self.words[w].getNextRandomFragment()
                        if w: self.sentence = self.sentence + separator + w
                    except IndexError: # occurs when looking up an empty word
                        pass

            else:
                break

        return self.sentence

if __name__ == '__main__':
    d = dictionary()
    input = []

    while 1:
        i = stdin.readline()[:-1] # cut off last char "\n"

        if i == "":
            break

        input.append(i)

        for sentence in i.split(". "): # ugly hack
            d.dissociate(sentence)

    print "=== Dissociated Press ==="

    try:
        while 1:
            sentence = d.associate()
    
            if sentence not in input:
                print sentence
                sleep(1)
    
    except KeyboardInterrupt:
        print "=== Enough! ==="
    
