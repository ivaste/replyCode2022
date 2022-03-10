"""
This file is used as template for:
- input parsing
- save solution to file (that will be uploaded to google)
- simulate the solution to compute the score
you just need to import this file into your python code.

Functions implemented:
- read_input_file():        
- print_problem_instance(): used mainly to check if the input is read correctly
- save_solution():          save solution to file (that we need to upload)
- read_solution_file(): 
- compare_solutions():      used to check if the solution is saved correctly
- simulate_solution():      returns the score
- simulate_all():           simulate all inpout files in the given list

From your python code you just need to call:
- read_input_file()
- save_solution()
- simulate_solution()
- simulate_all()
other functions are used to input/output debug

"""


#read one single file and return the problem instance
def read_input_file(filename):
  f = open(filename, "r")

  problem_instance=[]

  initial_stamina,max_stamina, T, D=list(map(int,f.readline().rstrip().split()))
  
  problem_instance.append(initial_stamina)
  problem_instance.append(max_stamina)
  problem_instance.append(T)
  problem_instance.append(D)
  demons={}
  for i in range(D):
    demon=list(map(int,f.readline().rstrip().split()))

    consumed_stamina,turn_wait,recovered_stamina, num_frag=demon[0:4]
    fragments=demon[4:]

    demon=[]
    demon.append(consumed_stamina)
    demon.append(turn_wait)
    demon.append(recovered_stamina)
    demon.append(num_frag)
    demon.append(fragments)

    demons[i]=demon
  
  problem_instance.append(demons)

  f.close()

  return problem_instance #list of parameters

#Check if the input is parsed correctly
def print_problem_instance(problem_instance):

  print(problem_instance[:4])

  for d in problem_instance[4]:
    print(d,problem_instance[4][d])

  return

#Save the solution into a file as described in the problem PDF
def save_solution(solution=None,filename=None):
  if not solution or not filename:
    print("empty solution or empty filename")
  
  f = open(filename, "w")

  for d in solution:
    f.write(str(d)+"\n")

  f.close()

  print("Solution saved correctly in:",filename)

#read a solution file and return the solution instance
def read_solution_file(filename=None):
  if not filename:
    print("empty filename")
    return
  
  #...COMPLETE...
  solution=...
  #...COMPLETE...

  return solution

#check if 2 solution are the same
#used to check if the solution is saved correctly
def compare_solutions(sol1=None,sol2=None):
  if not sol1 or not sol2:return False

#simulate the solution and return the score
def simulate_solution(solution=None,problem_instance=None,verbose=0):
  if not solution:
    print("empty soluton")
    return
  if not problem_instance:
    print("no problem given")
    return
  
  #read input file

  #execute solution on given input file
  #...COMPLETE...
  score=0
  #...COMPLETE...

  return score



########################################################################
"""
THE FOLLOWING LINES MUST BE COMMENTED WHEN SOLVING THE PROBLEM
"""

#Check if the input is parsed correctly
filename="data/00.txt"
problem_instance=read_input_file(filename)
print_problem_instance(problem_instance)
"""
#check if the solution is saved correctly
sol1=[1,2,3,4,5]  #COMPLETE
savefile="output/solution_test.txt"
save_solution(sol1, savefile)
sol2=read_solution_file(savefile)
equal=compare_solutions(sol1,sol2)
if not equal: print("Solution is NOT saved correctly")
else: print("Solution is saved correctly")

#compute the score
print(simulate_solution(sol1))
"""

