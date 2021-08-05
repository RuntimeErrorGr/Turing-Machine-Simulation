# Lăbău Cristea Andrei Liviu 324CB
import sys
import fileinput

# @noStates = total number of states
# @finalStates = array of final states
# @transitions = list of tuples with possible transitions
# Define a Turing Machine class.
class Machine:
	noStates = 0
	finalStates = []
	transitions = []
	def print(self):
		print(self.noStates)
		print(self.finalStates)
		print(self.transitions)
# Read the input from stdin untile EOF is reached.
# return @string = input represented as string
def getInputString():
	string = ""
	for line in sys.stdin:
		try:
			string += line
		except EOFError:
			break;
	return string;
# Convert a list to a list of lists.
# This function is used to get the second line of the input file
# (input according to name of task -> step/accept/k_accept)
# and to convert it in a useful form, getting rid of special
# characters and blank spaces.
# @string = string of "(left_word, state, right_word)"
# return @configs = list of configurations [left_word, state, right_word]
def stringToMatrix(string):
	configs = (string[1].strip("\r")).split(" ")
	for i in range(len(configs)):
		configs[i] = (configs[i].strip("()")).split(",")
		for j in range(len(configs[i])):
			if configs[i][j].isdigit():
				configs[i][j] = (int)(configs[i][j])
	return configs
# Convert @string in an internal representation of TM.
# Each atribute of TM is initialised accordingly.
# @machine = turing machine object
# @string = input string (it starts from the 3rd line of the input file
# because 1st line = task name, 2nd line = input configurations / words).
def readTM(machine, string):
	machine.noStates = (int)(string[2])				# get total number of states
	string[3] = (string[3].strip("\r")).split(" ")
	for x in string[3]:								# get final states
		if x.isdigit():
			machine.finalStates.append((int)(x))
	if string[len(string) - 1] == "": 				# if an input file has '\n'
		lines = len(string) - 5						# at the end don't count it
	else:											# at number of lines
		lines = len(string) - 4
	machine.transitions = [[] for x in range(lines)] # get transitions
	for i in range(lines):
		string[i + 4] = (string[i + 4].strip("\r")).split(" ")
		for j in range(5):
			if string[i + 4][j].isdigit():
				machine.transitions[i].append((int)(string[i + 4][j]))
			else:
				machine.transitions[i].append(string[i + 4][j])
# Convert list @s in a string @strl.
# This function is used to convert "right_word" from tuples because
# my tuples are in the form of:
# left_word -> string 
# current state -> int
# right_word -> list
# (for easier printing)
def listToString(s):  
    str1 = ""  
    for el in s:  
        str1 += el   
    return str1  
# @configs = list of configurations to be printed
# Print at stdout a string of "(left_word, state, right_word)".
# It includes special characters such as '(', ')', ',' and blank spaces.
# It is used to print list of updated configurations after one step.
def printNextConfigs(configs):
	for i in range(len(configs)):
		if configs[i] == [] or configs[i][1] < 0:
			print("False", end='')
		else:
			print("(" + configs[i][0] + ",", end='')
			print((str)(configs[i][1]).strip("[]") + ",", end='')
			print(listToString(configs[i][2]).strip("[]"), end='')
			print(")", end='')
		if i != len(configs) - 1:
			print(" ", end='')
# @machine = turing machine object
# @config = initial configuration
# return @config = modified configuration afer one step
# Make a transition from "(left_word, state, right_word)" to
# "(new_left_word, new_state, new_right_word)" accordingly
# to the list of tuples with possible transitions.
# In a for loop I go through all possible transitions.
# If current state (config[1]) from configuration matches with current state
# from a possible transition (trans[0]) and current character (config[2][0])
# matches with current character from a possible transition (trans[1]):
# update current state and current character and move the cursor:
# If cursor goes right -> add current character to left_word and remove it 
# from right_word. If right_word remains empty, append a '#' to it. Now transition
# is complete -> break.
# If cursor goes left -> add at the beggining of right_word last char of left_word
# and remove it from left_word. If left_word remains empty, append a '# to it'.
# Now transition is complete -> break.
# If cursor halts -> don't make any additional changes on words. -> break
# Also we have to count how many possible transitions it skkiped. If the machine
# went through all possible transitions and doesn't have any match it hangs
# and current state is updated at -1 (invalid state).
def oneStep(machine, config):
	count = 0
	for trans in machine.transitions:
		if config[1] == trans[0] and config[2][0] == trans[1]:
			config[1] = trans[2]
			config[2] = (list)(config[2])
			config[2][0] = trans[3]
			if trans[4] == "R":
				config[0] += config[2][0]
				config[2].pop(0)
				if len(config[2]) == 0:
					if config[2] == []:
						config[2].append("#")
				break
			if trans[4] == "L":
				config[2].insert(0, config[0][len(config[0]) - 1])
				config[0] = config[0][:-1]
				if config[0] == "":
					config[0] += "#"
				break
			else:
				break
		else:
			count += 1
	if count >= len(machine.transitions):
		config[1] = -1
	return config
# @machine = turing machine object
# @configs = list of initial configurations
# return @configs = list of modified configurations after one step
# For all initial configurations given as input make one step. 
def step(machine, configs):
	for config in configs:
		config = oneStep(machine, config);
	return configs 
# @machine = turing machine object
# @words = list of words
# return @bools = list of booleans and blank spaces without '\n'
# In a for loop I go through all words given as input:
# Starting from the initial configuration ('#', state 0, word), the machine
# is allowed to perform a huge number of steps (k = 1000). For each configuration
# the machine reaches, the final state (config[1]) is compared to all states
# from machine.finalStates list:
# If we have a match, the machine is in a final state, therefor the word is 
# accepted and a "True" is added in booleans string. -> break. 
# If we don't have any match, the machine performs one more step.
# If the machine reaches a state from wich it can no longer perform steps, the 
# word is rejected and a "False" is added in booleans string.
# Also if the word is not accepted in k = 1000 steps, it is rejected and a
# "False" is added in booleans string.
def accept(machine, words):
	booleans = ""
	for w in words:
		ok = 0
		k = 1000
		word = w[0]
		config = ["#", 0, (list)(word)]
		if config[1] >= 0:
			while k >= 0:
				for f in machine.finalStates:
					if config[1] == f:
						ok = 1       
						break
				if ok == 1:
					break
				config = oneStep(machine, config)
				k -= 1
			if ok == 1:
				booleans += "True" + " " 
			else:
				booleans += "False" + " "
		else:
			booleans += "Flase" + " "
	return booleans.rstrip()
# @machine = turing machine object
# @words = list of words and maximum number of steps
# return @bools = list of booleans and blank spaces without '\n'
# Similar to the previous case.
# In a for loop I go through all words given as input:
# Starting from the initial configuration ('#', state 0, word), the machine
# is allowed to perform as many steps as specified in the input.
# For each configuration the machine reaches, the final state (config[1]) is 
# compared to all states from machine.finalStates list:
# If we have a match, the machine is in a final state, therefor the word is 
# accepted and a "True" is added in booleans string. -> break. 
# If we don't have any match, the machine performs one more step.
# If the machine reaches a state from wich it can no longer perform steps, the 
# word is rejected and a "False" is added in booleans string.
# Also if the word is not accepted in k specified steps, it is rejected and a
# "False" is added in booleans string.
def k_accept(machine, words):
	booleans = ""
	for w in words:
		ok = 0
		k = w[1]
		config = ["#", 0, w[0]]
		if config[1] >= 0:
			while k >= 0:
				for f in machine.finalStates:
					if config[1] == f:
						ok = 1 
						break
				if ok == 1:
					break
				config = oneStep(machine, config)
				k -= 1
			if ok == 1:
				booleans += "True" + " "
			else:
				booleans += "False" + " "
		else:
			booleans += "Flase" + " "
	return booleans.rstrip()
def main():
	string = getInputString().split("\n")
	taskName = string[0].strip("\r")
	if taskName == "step":
		machine = Machine()
		readTM(machine, string)
		configs = stringToMatrix(string)
		printNextConfigs(step(machine, configs))
	if(taskName == "accept"):
		machine = Machine()
		readTM(machine, string)
		words = stringToMatrix(string)
		print(accept(machine, words), end='')
	if(taskName == "k_accept"):
		machine = Machine()
		readTM(machine, string)
		words = stringToMatrix(string)
		print(k_accept(machine, words), end='')
if __name__ == "__main__":
	main()

