#
# Markov Text Generator
# (c) Afaan Bilal
# https://afaanbilal.github.io
#

import sys
import os
import random
import json

class Markov:
    order = 4
    table = {}

    def build(self, text, order = 4):
        self.order = order

        for i in range(0, len(text)):
            char = text[i:i+order]
            if char not in self.table.keys():
                self.table[char] = {}
        
        for i in range(0, len(text) - order):
            char_i = text[i:i+order]
            char_v = text[i+order:i+2*order]

            if (char_v in self.table[char_i].keys()):
                self.table[char_i][char_v] += 1
            else:
                self.table[char_i][char_v] = 1
        
        with open('model.json', 'w') as f:
            f.write(json.dumps(self.table))

    def arr_sum(self, char):
        total = 0
        for (c, w) in self.table[char].items():
            total += w
        return total
    
    def next_char(self, char):
        total = self.arr_sum(char)
        
        if (total <= 1):
            return random.choice(list(self.table.keys()))
        
        rand  = random.randint(1, total - 1)
        
        for (c, w) in self.table[char].items():
            if rand <= w:
                return c
            rand -= w
        
        return random.choice(self.table.keys())

    def generate(self, length):
        if not os.path.exists('./model.json'):
            print("Error: Could not find model.json! Have you generated a model?")
            sys.exit()

        with open('model.json', encoding="utf8") as f:
            self.table = json.loads(f.read())
             
        char = random.choice(list(self.table.keys()))
        output = char
        for i in range(0, int(length / self.order)):
            char = self.next_char(char)
            output += char
        return output

if not os.path.exists('./text.txt'):
    print("Error: Could not find text.txt!")
    sys.exit()


markov = Markov()

# Uncomment the following lines to generate a model from text.txt
# text = ''
# with open('text.txt', encoding="utf8") as f:
#     text = f.read()
# markov.build(text, 5)

print(markov.generate(500))
