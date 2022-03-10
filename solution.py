"""
This file is used as template for Google HashCode
Functions:
- solve():      given problem_instance returns a solution
- solve_all():  
------------------------------------------------------------

REPRESENTATION OF THE DATA:

problem instance: [initial_stamina,max_stamina, T, D, DEMONS]
            DEMONS= {}
                  index--->[consumed_stamina,turn_wait,recovered_stamina, num_frag, FRAGMENTS]
            FRAGMENTS=[1,5,7,8,...]




"""


from collections import OrderedDict
from io_simulate import * #import input/output/simulation functions
import glob         #used to get directories files
from heapq import *
import statistics

#turn simulation

"""
For each turn:
  1) Recover stamina (if any)
	2) Face the most rewarding demon (DIFFICULT PART!)
	3) Gather accumulated fragments by defeated demons (if any)

turn_instance:
  demons
  turn
  remaining_demons: {demon_idx,...}
  defeated_demons: demon_idx--->defeated_turn
  useless_demons:  turn--->[demon_idx,..]
  stamina_demons: turn--->stamina_recovered
  accumulated_fragments
  current_stamina
  solution=[demon_idx,..] temporal ordered list of defeated demons


"""
def recover_stamina(turn_instance):
  stamina_demons=turn_instance["stamina_demons"]
  turn=turn_instance["turn"]

  if turn not in stamina_demons: return
  stamina_recovered=stamina_demons[turn]
  turn_instance["current_stamina"]+=stamina_recovered

def select_demon(turn_instance):
  remaining_demons=turn_instance["remaining_demons"]
  idx=0
  found=False
  
  for demon_idx in remaining_demons:

    demon=turn_instance["demons"][demon_idx]
    consumed_stamina=demon[0]
    if turn_instance["current_stamina"]<consumed_stamina:continue

    found=True
    idx=demon_idx
    break

  if not found:return -1
  demon_idx=idx
  return demon_idx

def select_demon_average(turn_instance):
  remaining_demons=turn_instance["remaining_demons"]

  heap_score=turn_instance["heap_score"]

  if not heap_score:return -1
  new_heap=[]

  #while the best has a too high stamina pop it
  score,demon_idx=heap_score[0]
  demon=turn_instance["demons"][demon_idx]
  consumed_stamina=demon[0]
  while heap_score and turn_instance["current_stamina"]<consumed_stamina:
    heappush(new_heap,heappop(heap_score))
    if heap_score:
      score,demon_idx=heap_score[0]
      demon=turn_instance["demons"][demon_idx]
      consumed_stamina=demon[0]

  if not heap_score:
    turn_instance["heap_score"]=new_heap
    return -1
  
  #rebuil the heap
  while new_heap:
    heappush(heap_score,heappop(new_heap))
  
  score,demon_idx=heappop(heap_score)
  return demon_idx

  
  

def fight_demon(turn_instance):
  remaining_demons=turn_instance["remaining_demons"]
  if len(remaining_demons)==0: return

  #select demon
  demon_idx=select_demon(turn_instance)
  #demon_idx=select_demon_average(turn_instance)

  if demon_idx<0:return

  #consume stamina
  demon=turn_instance["demons"][demon_idx]
  consumed_stamina=turn_instance["current_stamina"]
  turn_instance["current_stamina"]-=consumed_stamina

  #remove the demon
  #remaining_demons.remove(demon_idx)
  del remaining_demons[demon_idx]

  turn_instance["solution"].append(demon_idx)

  defeated_demons=turn_instance["defeated_demons"]
  turn=turn_instance["turn"]
  defeated_demons[demon_idx]=turn

  #save when the selected demon will stop giving us fragments
  useless_demons=turn_instance["useless_demons"]
  turn_wait=demon[3]
  useless_turn=turn+turn_wait
  if useless_turn not in useless_demons:useless_demons[useless_turn]=[]
  useless_demons[useless_turn].append(demon_idx)

  #save when the selected demon give us stamina
  stamina_demons=turn_instance["stamina_demons"]
  turn_wait=demon[1]
  stamina_turn=turn+turn_wait
  stamina_recovered=demon[2]
  if stamina_turn not in stamina_demons:stamina_demons[stamina_turn]=0
  stamina_demons[stamina_turn]+=stamina_recovered
  stamina_demons[stamina_turn]=max(stamina_demons[stamina_turn],turn_instance["max_stamina"])

def gather_fragments(turn_instance):
  useless_demons=turn_instance["useless_demons"]
  defeated_demons=turn_instance["defeated_demons"]
  turn=turn_instance["turn"]

  #remove demons from defeated if useless
  if turn in useless_demons:
    for idx in useless_demons[turn]:
      del defeated_demons[idx]
  
  #update reward
  current_reward=0
  for demon_idx in defeated_demons:
    defeated_turn=defeated_demons[demon_idx]
    demon=turn_instance["demons"][demon_idx]
    fragments=demon[4]
    current_reward+=fragments[turn-defeated_turn]
  turn_instance["accumulated_fragments"]+=current_reward



def turn(turn_instance):

  recover_stamina(turn_instance)
  fight_demon(turn_instance)
  gather_fragments(turn_instance)

  turn_instance["turn"]+=1


#solve the problem
def solve(problem_instance=None):
  if not problem_instance:
    print("no problem given")
    return

  initial_stamina,max_stamina, T, D, demons=problem_instance

  turn_instance={}
  turn_instance["demons"]=demons
  turn_instance["turn"]=0
  #turn_instance["remaining_demons"]=set()
  #for idx in demons:turn_instance["remaining_demons"].add(idx)

  turn_instance["remaining_demons"]=OrderedDict()
  new_rem=[]
  for demon_idx in demons:
    score=0
    if len(demons[demon_idx][4])!=0:
      score=statistics.mean(demons[demon_idx][4])
    new_rem.append((score,demon_idx))
  new_rem.sort(key=lambda x:-x[0])
  for score,idx in new_rem:
    turn_instance["remaining_demons"][idx]=score

  turn_instance["defeated_demons"]={}
  turn_instance["useless_demons"]={}
  turn_instance["stamina_demons"]={}
  turn_instance["accumulated_fragments"]=0
  turn_instance["current_stamina"]=initial_stamina
  turn_instance["max_stamina"]=max_stamina
  turn_instance["solution"]=[]

  """heap_score=[]
  for demon_idx in demons:
    score=0
    if len(demons[demon_idx][4])!=0:
      score=statistics.mean(demons[demon_idx][4])
    heap_score.append((-score,demon_idx))
  #heapify(heap_score)
  heap_score.sort(key=lambda x:-x[0])
  heap_score=heap_score[0:10000]
  heapify(heap_score)
  turn_instance["heap_score"]=heap_score"""
  
  

  for t in range(T):
    turn(turn_instance)
  
  solution=turn_instance["solution"]

  return solution


#given a list of input files solve all
def solve_all(files=None,verbose=0):
  if not files:
    print("no files given")
    return -1
  
  print("Scores:")
  for filename in files:
    problem_instance=read_input_file(filename)
    solution=solve(problem_instance)
    score=simulate_solution(solution,problem_instance,verbose)

    print("\t",filename,score)


###################################################

#input files paths
files=glob.glob("data/*.txt")

#solve 1 single problem
for filename in files:
  print("Executing",filename)
  #filename=files[0]
  problem_instance=read_input_file(filename)
  solution=solve(problem_instance)
  savefile="output/"+filename[5:]
  save_solution(solution, savefile)
#score=simulate_solution(solution,problem_instance,verbose=0)
#print(filename,score)

#solve all problems
#solve_all(files)
