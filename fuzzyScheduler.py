import sys
from cspProblem import CSP,Constraint
from cspConsistency import Search_with_AC_from_CSP
from searchGeneric import AStarSearcher


# add soft constraints, soft cost related to CSP as new_csp
class new_csp(CSP):
    def __init__(self, domains, constraints,soft_constraints,soft_cost):
        super().__init__(domains, constraints)
        self.soft_constraints = soft_constraints
        self.soft_cost = soft_cost
# add cost to consideration while searching with ARC from csp
class new_search_with_AC_from_CSP (Search_with_AC_from_CSP):
    def __init__(self,csp):
        super().__init__(csp)
        self.cost = []
        self.soft_constraints = csp.soft_constraints
        self.soft_cost = soft_cost
        # change  ARC def __init__(self, from_node, to_node, cost=1, action=None):
        # to  def __init__(self, from_node, to_node, cost=0, action=None): 

    # add a heuristic calculating method
    def heuristic(self,nodes):
        cost = 0
        for task in nodes:
            if task in self.soft_constraints:
                temp_cost = []
                expected_end_time = self.soft_constraints[task]
                for start_end in nodes[task]:
                    end_time = start_end[1]
                    if end_time > expected_end_time:
                        hours_postponed = (end_time//10- expected_end_time//10)*24 + ((end_time%10) - (expected_end_time%10))
                        temp_cost.append(self.soft_cost[task] * hours_postponed)
                    else:
                        temp_cost=[0]
                        break
                if len(temp_cost)!=0:
                    cost = cost + min(temp_cost)
        return cost
# set 'max_display_level = 1 to 'max_display_level = 0'
class new_AStarSearcher(AStarSearcher):
    def __init__(self, problem):
        super().__init__(problem)
        self.max_display_level=0
    

##############################
# define constraint conditions
##############################

def binary_before(task_1,task_2):
    return task_1[1]<=task_2[0]

def binary_after(task_1,task_2):
    return task_2[1]<=task_1[0]

def binary_same_day(task_1,task_2):
    return task_1[0]//10 == task_2[0]//10

def binary_starts_at(task_1,task_2):
    return task_1[0] == task_2[1]

def hard_day(day):
    converted_day = week_to_number[day]
    condition = lambda x: x[0]//10 ==converted_day//10
    return condition

def hard_time(time):
    converted_time = time_to_number[time]
    condition = lambda x: x[0]%10 == converted_time
    return condition

def hard_starts_before_day_time(day,time):
    converted_day = week_to_number[day]
    converted_time = time_to_number[time]
    start_time = converted_day + converted_time
    condition = lambda x: x[0] <= start_time
    return condition

def hard_starts_before_time(time):
    converted_time = time_to_number[time]
    condition = lambda x: x[0]%10 <= converted_time
    return condition

def hard_starts_after_day_time(day,time):
    converted_day = week_to_number[day]
    converted_time = time_to_number[time]
    starts_after = converted_day + converted_time
    condition = lambda x: x[0] >= starts_after
    return condition
    
def hard_starts_after_time(time):
    converted_time = time_to_number[time]
    condition = lambda x: x[0]%10 >= converted_time
    return condition

def hard_ends_before_day_time(day,time):
    converted_day = week_to_number[day]
    converted_time = time_to_number[time]
    ends_before = converted_day + converted_time
    condition = lambda x: x[1] <= ends_before
    return condition

def hard_ends_before_time(time):
    converted_time = time_to_number[time]
    condition = lambda x: x[1]%10 <= converted_time
    return condition

def hard_ends_after_day_time(day,time):
    converted_day = week_to_number[day]
    converted_time = time_to_number[time]
    ends_after = converted_day + converted_time
    condition = lambda x: x[1] >= ends_after
    return condition

def hard_ends_after_time(time):
    converted_time = time_to_number[time]
    condition = lambda x: x[1]%10 >= converted_time
    return condition
    
def hard_starts_in_range(day_1,time_1,day_2,time_2):
    converted_day_1 = week_to_number[day_1]
    converted_day_2 = week_to_number[day_2]
    converted_time_1 = time_to_number[time_1]
    converted_time_2 = time_to_number[time_2]

    range_left = converted_day_1 + converted_time_1
    range_right = converted_day_2 + converted_time_2
    
    def start_range(val):
        return val[0]>=range_left and val[0]<=range_right

    return start_range

def hard_ends_in_range(day_1,time_1,day_2,time_2):
    converted_day_1 = week_to_number[day_1]
    converted_day_2 = week_to_number[day_2]
    converted_time_1 = time_to_number[time_1]
    converted_time_2 = time_to_number[time_2]

    range_left = converted_day_1 + converted_time_1
    range_right = converted_day_2 + converted_time_2
    
    def end_range(val):
        return val[1]>=range_left and val[1]<=range_right

    return end_range




########################################
# read the file and prepare to build CSP
########################################

file_name = sys.argv[1]

file = open(file_name,'r')
file_list = file.readlines()

# day & time convertion for reading and calculation
week_to_number = {'mon': 10, 'tue': 20, 'wed': 30, 'thu': 40, 'fri': 50}
number_to_week = {1 : 'mon', 2: 'tue', 3: 'wed', 4: 'thu', 5: 'fri'}

time_to_number = {'9am': 1, '10am': 2, '11am':3, '12pm': 4, '1pm': 5, '2pm': 6, '3pm': 7, '4pm': 8, '5pm':9}
number_to_time = {1 : '9am', 2: '10am', 3:'11am',4 :'12pm', 5 :'1pm', 6:'2pm', 7:'3pm', 8 :'4pm', 9:'5pm'}

# set up the variables
domain = {}
hard_constraints=[]
soft_constraints = {}
soft_cost = {}


#############################
# read each line to build CSP
#############################

for line in file_list:
    # filter out the comment lines
    if '#' in line:
        continue
    # filter out the blank lines
    if line == '\n':
        continue
    # get each element in a line
    elements = line.strip().replace(',','').split()
    if elements == []:
        continue
    # get basic task information

    #############################
    # set up domain for each task
    #############################
    elif elements[0] == 'task':
        
        task = elements[1]
        duration = int(elements[2])
        # generate a simple domain based on input
        # first int stands for day(1 to 5 or 10 to 50 combined with hours), second int stands for time (1 to 9 == 9 to 5)
        # for example monday 9 to monday 5 is represented as (11,19)
        task_domain = set()
        for days in range(1,6):
            for hours in range(1,10-duration):
                task_domain.add((days*10+hours,days*10+hours+duration))
        domain[task] = task_domain
    #######################
    # get binary contraints
    #######################
    elif elements[0] == 'constraint':
        task_1 = elements[1]
        task_2 = elements[3]
        constraint_description = elements[2]
        # constraint, <t1> before <t2> # t1 ends when or before t2 starts
        if constraint_description == 'before':
            hard_constraints.append(Constraint((task_1, task_2), binary_before))
        # constraint, <t1> after <t2> # t1 starts after or when t2 ends
        if constraint_description == 'after':
            hard_constraints.append(Constraint((task_1, task_2), binary_after))
        # constraint, <t1> same-day <t2> # t1 and t2 are scheduled on the same day
        if constraint_description == 'same-day':
            hard_constraints.append(Constraint((task_1, task_2), binary_same_day))
        # constraint, <t1> starts-at <t2> # t1 starts exactly when t2 ends
        if constraint_description == 'starts-at':
            hard_constraints.append(Constraint((task_1, task_2), binary_starts_at))

    ############################
    # get hard & soft constraints
    ############################
    # get hard constraints
    elif elements[0] == 'domain':
        task = elements[1]
        if len(elements) == 3:
            # domain, <t> <day> t starts on given day at any time
            if elements[2] in week_to_number:
                day_constraint = elements[2]
                hard_constraints.append(Constraint((task,),hard_day(day_constraint)))
            # domain, <t> <time> t starts at given time on any day
            if elements[2] in time_to_number:
                time_contraint = elements[2]
                hard_constraints.append(Constraint((task,),hard_time(time_contraint)))
        elif len(elements) == 4:
            time_contraint = elements[3]
            constraint_description = elements[2]
            # domain, <t> starts-before <time> # at or before time on any day
            if constraint_description == 'starts-before':
                hard_constraints.append(Constraint((task,),hard_starts_before_time(time_contraint)))
            # domain, <t> ends-before <time> # at or before time on any day
            if constraint_description == 'ends-before':
                hard_constraints.append(Constraint((task,),hard_ends_before_time(time_contraint)))
            # domain, <t> starts-after <time> # at or after time on any day
            if constraint_description == 'starts-after':
                hard_constraints.append(Constraint((task,),hard_starts_after_time(time_contraint)))
            # domain, <t> ends-before <time> # at or after time on any day
            if constraint_description == 'ends-after':
                hard_constraints.append(Constraint((task,),hard_ends_after_time(time_contraint)))
        elif len(elements) == 5:
            constraint_description = elements[2]
            day_constraint = elements[3]
            time_contraint = elements[4]
            # domain, <t> starts-before <day> <time> # at or before given time
            if constraint_description == 'starts-before':
                hard_constraints.append(Constraint((task,),hard_starts_before_day_time(day_constraint,time_contraint)))
            # domain, <t> ends-before <day> <time> # at or before given time
            if constraint_description == 'ends-before':
                hard_constraints.append(Constraint((task,),hard_ends_before_day_time(day_constraint,time_contraint)))
            # domain, <t> starts-after <day> <time> # at or after given time
            if constraint_description == 'starts-after':
                hard_constraints.append(Constraint((task,),hard_starts_after_day_time(day_constraint,time_contraint)))
            # domain, <t> ends-before <day> <time> # at or after given time
            if constraint_description == 'ends-after':
                hard_constraints.append(Constraint((task,),hard_ends_after_day_time(day_constraint,time_contraint)))
        elif len(elements) == 6:
            constraint_description = elements[2]
            
            # domain, <t> starts-in <day> <time>-<day> <time> # day-time range
            if constraint_description == 'starts-in':
                format_split = elements[4].split('-')
                day_1 = elements[3]
                time_1 = format_split[0]
                day_2 = format_split[1]
                time_2 = elements[5]
                hard_constraints.append(Constraint((task,), hard_starts_in_range(day_1,time_1,day_2,time_2)))
            # domain, <t> ends-in <day> <time>-<day> <time> # day-time range
            if constraint_description == 'ends-in':
                format_split = elements[4].split('-')
                day_1 = elements[3]
                time_1 = format_split[0]
                day_2 = format_split[1]
                time_2 = elements[5]
                hard_constraints.append(Constraint((task,), hard_ends_in_range(day_1,time_1,day_2,time_2)))
            ###################
            # soft constraint #
            # cost per hour of missing deadline
            ###################
            if constraint_description == 'ends-by':
                day_constraint = elements[3]
                time_contraint = elements[4]
                cost = elements[5]

                converted_day = week_to_number[day_constraint]
                converted_time = time_to_number[time_contraint]
                soft_cost[task]=int(cost)
                soft_constraints[task]=converted_day+converted_time

# now we run the test
csp = new_csp (domain, hard_constraints, soft_constraints,soft_cost)
problem = new_search_with_AC_from_CSP(csp)
solution = new_AStarSearcher(problem).search()

# print output
if solution != None:
    optimal_solution = solution.end()
    cost = problem.heuristic(optimal_solution)
    for task in optimal_solution:
        # sample format is '{(11, 14)}' at this stage below
        the_number_for_day = int(str(optimal_solution [task])[2])
        day = number_to_week[the_number_for_day]
        the_number_for_time = int(str(optimal_solution [task])[3])
        time = number_to_time[the_number_for_time]
        print(f'{task}:{day} {time}')
    print(f'cost:{cost}')
else:
    print('No solution')
          