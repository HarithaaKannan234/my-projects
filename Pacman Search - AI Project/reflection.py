# reflection.py
# -----------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
from typing import List

######################
# REFLECTION QUESTIONS #
######################
  
def question10a() -> bool:
    answer = True # Change None to True or False
    return answer

def question10b() -> bool:
    answer = False # Change None to True or False
    return answer

def question10c() -> List[bool]:
    Q1 = False # Change None to True or False
    Q2 = False # Change None to True or False
    Q3 = False # Change None to True or False
    Q4 = False # Change None to True or False
    Q9 = True # Change None to True or False
    return [Q1, Q2, Q3, Q4, Q9]

def question10d() -> List[bool]:
    Q1 = False # Change None to True or False
    Q2 = False # Change None to True or False
    Q3 = False # Change None to True or False
    Q4 = False # Change None to True or False
    Q9 = True # Change None to True or False
    return [Q1, Q2, Q3, Q4, Q9]

if __name__ == '__main__':
    print('Answers to reflection questions:')
    import reflection
    for q in [q for q in dir(reflection) if q.startswith('question')]:
        response = getattr(reflection, q)()
        print('  Question %s:\t%s' % (q, str(response)))
