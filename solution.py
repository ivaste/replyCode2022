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


from io_simulate import * #import input/output/simulation functions
import glob         #used to get directories files


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

def fight_demon(turn_instance):
  remaining_demons=turn_instance["remaining_demons"]
  if len(remaining_demons)==0: return

  #select demon
  idx=0
  found=False
  #for demon_idx in range(len(turn_instance["demons"])):
  for demon_idx in remaining_demons:
    #if demon_idx not in remaining_demons:continue

    demon=turn_instance["demons"][demon_idx]
    consumed_stamina=demon[0]
    if turn_instance["current_stamina"]<=consumed_stamina:continue

    #consume stamina
    turn_instance["current_stamina"]-=consumed_stamina
    found=True
    idx=demon_idx
    break
  
  if not found: return
  demon_idx=idx
  #remove the demon
  remaining_demons.remove(demon_idx)

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
  turn_instance["remaining_demons"]=set()
  for idx in demons:turn_instance["remaining_demons"].add(idx)
  turn_instance["defeated_demons"]={}
  turn_instance["useless_demons"]={}
  turn_instance["stamina_demons"]={}
  turn_instance["accumulated_fragments"]=0
  turn_instance["current_stamina"]=initial_stamina
  turn_instance["max_stamina"]=max_stamina
  turn_instance["solution"]=[]

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
filename=files[0]
problem_instance=read_input_file(filename)
solution=solve(problem_instance)
savefile="output/"+filename[5:]
save_solution(solution, savefile)
#score=simulate_solution(solution,problem_instance,verbose=0)
#print(filename,score)

#solve all problems
#solve_all(files)
