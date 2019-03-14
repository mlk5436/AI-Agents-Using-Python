############################################################
# CMPSC 442: Homework 5
############################################################

student_name = "Meng Kry"


############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import copy


############################################################
# Section 1: Propositional Logic
############################################################

class Expr(object):
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))


class Atom(Expr):
    def __init__(self, name):
        self.name = name
        self.hashable = name

    def __eq__(self, other):
        if type(self)!= type(other):
            return False
        return self.name== other.name

    def __repr__(self):
        return "Atom("+str(self.name)+")"

    def atom_names(self):
        return set([self.name])

    def evaluate(self, assignment):
        return assignment[self.name]

    def to_cnf(self):
        return self


class Not(Expr):
    def __init__(self, arg):
        self.arg = arg
        self.hashable = arg

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.arg== other.arg

    def __repr__(self):
        return "Not("+str(self.arg)+")"

    def atom_names(self):
        return self.arg.atom_names()

    def evaluate(self, assignment):
        if self.arg.evaluate(assignment) == True:
            return False
        return True

    def to_cnf(self):
        cnf = []
        tmp = self.arg.to_cnf()
        #de morgan case 1: Not(And(a,b)) === Or(Not(a),Not(b))
        if isinstance(tmp,And):
            for x in tmp.hashable:
                cnf.append(Not(x).to_cnf())
            return Or(*cnf).to_cnf()
        #de morgan case 2: Not(Or(a,b)) === And(Not(a),Not(b))
        elif isinstance(tmp,Or):
            for x in tmp.hashable:
                cnf.append(Not(x).to_cnf())
            return And(*cnf).to_cnf()
        elif isinstance(tmp,Not):
            return tmp.arg
        elif isinstance(tmp,Atom):
            return Not(tmp)

class And(Expr):
    def __init__(self, *conjuncts):
        self.conjuncts = frozenset(conjuncts)
        self.hashable = self.conjuncts

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.conjuncts == other.conjuncts

    def __repr__(self):
        str = "And("
        for x in self.hashable:
            str+= repr(x)+ ", "
        return str[:-2]+")"

    def atom_names(self):
        name = set()
        for x in self.conjuncts:
            name = name.union(x.atom_names())
        return name

    def evaluate(self, assignment):
        for x in self.hashable:
            if x.evaluate(assignment) == False:
                return False
        return True

    def to_cnf(self):
        cnf = []
        if len(self.hashable)== 1:
            for x in self.hashable:
                return x
        # distribution case1: And(And(a,b), c) === And(a,b,c)
        for x in self.hashable:
            if isinstance(x,Not):
                if isinstance(x.arg, Or):
                    for y in x.arg.hashable:
                        cnf.append(Not(y))
                elif isinstance(x.arg, And):
                    tmp = []
                    for y in x.arg.hashable:
                        tmp.append(Not(y))
                    cnf.append(Or(*tmp))
                else:
                    cnf.append(x)
            elif isinstance(x, And):
                for y in x.hashable:
                    cnf.append(y)
            else:
                cnf.append(x)
        return And(*cnf)

class Or(Expr):
    def __init__(self, *disjuncts):
        self.disjuncts = frozenset(disjuncts)
        self.hashable = self.disjuncts

    def __eq__(self, other):
        if type(self)!=type(other):
            return False
        return self.disjuncts == other.disjuncts

    def __repr__(self):
        str = "Or("
        for x in self.hashable:
            str += repr(x) + ", "
        return str[:-2]+")"

    def atom_names(self):
        name = set()
        for x in self.disjuncts:
            name = name.union(x.atom_names())
        return name

    def evaluate(self, assignment):
        for x in self.hashable:
            if x.evaluate(assignment) == True:
                return True
        return False

    def to_cnf(self):
        tmp_And = []
        tmp_Or = []
        # case: Or(And(a,b),c)
        # case: Or(And(a,b),And(c,d))
        # case: Or(And(a,b),And(c,d),e)
        # case: Or(And(a,Not(b)),And(Not(a),b))
        # (a^~b)v(~a^b) === (avb)^(~av~b)
        cnf_list = []
        cnf = []
        for x in self.hashable:
            if isinstance(x, Not):
                if isinstance(x.arg, Atom):
                    cnf_list.append(x)
                else:
                    cnf_list.append(x.to_cnf())
            else:
                cnf_list.append(x.to_cnf())

        for x in cnf_list:
            if isinstance(x,Or):
                for y in x.hashable:
                    tmp_Or.append(y)
            elif isinstance(x, Not):
                if isinstance(x.arg, Atom):
                    tmp_Or.append(x)
                else:
                    tmp_Or.append(x.to_cnf())
            elif isinstance(x, And):
                tmp = []
                for y in x.hashable:
                    tmp.append(y)
                tmp_And.append(tmp)
            else:
                tmp_Or.append(x)

        if len(tmp_And) > 1:
            for list in tmp_And:
                for x in list:
                    for list1 in tmp_And:
                        i = 0
                        if list != list1:
                            while i < 2:
                                tmp = copy.deepcopy(tmp_Or)
                                if isinstance(list1[i], Not):
                                    if list1[i].arg != x:
                                        tmp.append(x)
                                        tmp.append(list1[i])
                                        cnf.append(Or(*tmp))
                                elif isinstance(x, Not):
                                    if x.arg != list1[i]:
                                        tmp.append(x)
                                        tmp.append(list1[i])
                                        cnf.append(Or(*tmp))
                                elif isinstance(x, Atom) and isinstance(list1[1], Atom):
                                    if x != list1[i]:
                                        tmp.append(x)
                                        tmp.append(list1[i])
                                        if (tmp == list) or (tmp==list1) or (tmp == [list1[1],list1[0]]) or (tmp ==[list[1],list[0]]):
                                            tmp = copy.deepcopy(tmp_Or)
                                            i =2
                                        else:
                                            cnf.append(Or(*tmp))
                                    else:
                                        cnf.append(x)

                                i = i + 1
            return And(*cnf)
        elif len(tmp_And) == 1:
            for x in tmp_And:
                for y in x:
                    tmp = copy.deepcopy(tmp_Or)
                    tmp.append(y)
                    cnf.append(Or(*tmp))
            return And(*cnf)
        else:
            return Or(*tmp_Or)

class Implies(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (self.hashable == other.hashable)

    def __repr__(self):
        return "Implies(" + str(repr(self.left))+", "+str(repr(self.right))+")"

    def atom_names(self):
        return self.left.atom_names().union(self.right.atom_names())

    def evaluate(self, assignment):
        if (self.left.evaluate(assignment) == True) and (self.right.evaluate(assignment) == False):
            return False
        return True


    def to_cnf(self):
        # case1: a=>b --> Or(Not(a),b)
        return Or(Not(self.left),self.right).to_cnf()
        # case2: a<=>b ==> And(Or(Not(a),b),Or(a,Not(b))



class Iff(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)

    def __eq__(self, other):
        if type(self)!= type(other):
            return False
        return (self.hashable == other.hashable)

    def __repr__(self):
        return "Iff("+str(self.left)+", "+str(self.right)+")"

    def atom_names(self):
        return self.left.atom_names().union(self.right.atom_names())

    def evaluate(self, assignment):
        if (self.left.evaluate(assignment) == True) and (self.right.evaluate(assignment) == True):
            return True
        if (self.left.evaluate(assignment) == True) and (self.right.evaluate(assignment) == False):
            return False
        if (self.left.evaluate(assignment) == False) and (self.right.evaluate(assignment) == True):
            return False
        if (self.left.evaluate(assignment) == False) and (self.right.evaluate(assignment) == False):
            return True

    def to_cnf(self):
        # (a^~b)v(~a^b) === (avb)^(~av~b)
        # Or(And(a,Not(b)),And(Not(a),b)) === And(Or(a,b), Or(Not(a),Not(b))
        return And(Implies(self.left,self.right).to_cnf(),Implies(self.right,self.left).to_cnf()).to_cnf()


def generate_assignments(n, lists):
    if n == 0:
        return lists
    else:
        if len(lists) == 0:
            return generate_assignments(n-1, ["0", "1"])
        else:
            return generate_assignments(n-1, [i + "0" for i in lists] + [i + "1" for i in lists])

def satisfying_assignments(expr):
    n =len(expr.atom_names())
    assignments_binary = generate_assignments(n,[])
    assignments = []
    for binary in assignments_binary:
        assignment = []
        for x in binary:
            if x == '0':
                assignment.append(True)
            else:
                assignment.append(False)
        assignments.append(assignment)
    dict_list = []
    for assignment in assignments:
        i = 0
        dict = {}
        for x in expr.atom_names():
            dict[x] = assignment[i]
            i = i + 1
        dict_list.append(dict)

    for assignment in dict_list:
        if expr.evaluate(assignment):
            sat = copy.deepcopy(assignment)
            yield sat


class KnowledgeBase(object):
    def __init__(self):
        self.facts = set()

    def get_facts(self):
        return self.facts

    def tell(self, expr):
        expr = expr.to_cnf()
        if isinstance(expr, And):
            for x in expr.hashable:
                self.facts.add(x)
        else:
            self.facts.add(expr)

    def get_atoms(self, object):
        list = []
        for y in object.hashable:
            list.append(y)
        return list

    def ask(self, expr):
        flag = 0
        if isinstance(expr, Atom) or isinstance(expr, Not):
            for x in self.facts:
                if isinstance(x, Atom) or isinstance(x, Not):
                    if x == expr:
                        flag =1
                        break
                else:
                    list = self.get_atoms(x)
                    for i in list:
                        if expr == i:
                            flag = 1
                            break

        if flag == 0:
            return False

        expression = And(*self.facts)
        valid = satisfying_assignments(expression)
        dict= next(valid)
        #print dict
        if isinstance(expr, Atom):
                return dict[expr.atom_names().pop()]
        if isinstance(expr, Not):
                return not dict[expr.atom_names().pop()]

        if isinstance(expr, Or) or isinstance(expr, And):
                return expr.evaluate(dict)

        '''
        
        
        clauses = []
        clauses = And(And(*self.facts).to_cnf(),Not(expr).to_cnf()).to_cnf()
        
        comparelist = self.get_atoms(clauses)

        newlist = []
        while (1):
            for clause in clauses.hashable:
                for clause1 in clauses.hashable:
                    if clause!=clause1:
                        # clause is Or Object
                        if (isinstance(clause, Or) == True):
                            #  if clause1 is Or object
                            if isinstance(clause1, Or) == True:
                                for x in clause.hashable:
                                    for y in clause1.hashable:
                                        if x == Not(y) or Not(x) == y:
                                            list = self.get_atoms(clause)
                                            list1 = self.get_atoms(clause1)
                                            list.remove(x)
                                            list1.remove(y)
                                            lists = list + list1
                                            clause = Or(*list)
                                            clause1 = Or(*list1)
                                            newlist.append(Or(*lists))
                                            if len(list) == 0 or len(list1) == 0:
                                                return True

                            else:
                                for x in clause.hashable:
                                    if x == Not(clause1) or Not(clause1) == x:
                                        tmp = self.get_atoms(clause)
                                        tmp.remove(x)
                                        clause = Or(*tmp)
                                        tmp = self.get_atoms(clauses)
                                        tmp.remove(clause1)
                                        clauses = And(*tmp)
                                        return True
                        else:
                            if isinstance(clause1, Or) == True:
                                for x in clause1.hashable:
                                    if x == Not(clause) or clause == Not(x):
                                        tmp = self.get_atoms(clause1)
                                        tmp.remove(x)
                                        clause1 = Or(*tmp)
                                        tmp = self.get_atoms(clauses)
                                        tmp.remove(clause)
                                        clauses = And(*tmp)
                                        return True
                            else:
                                if clause == Not(clause1) or clause1 == Not(clause):
                                    tmp = self.get_atoms(clauses)
                                    tmp.remove(clause)
                                    tmp.remove(clause1)
                                    clauses = And(*tmp)
                                    return True
            if len(newlist)== 0:
                return False
            comparelist = self.get_atoms(clauses)
            if newlist in comparelist:
                return False
            merge = newlist+comparelist
            clauses = And(*merge)
      
a, b, c, d, e, f= map(Atom, "abcdef")


print a == a
print a==b
print And(a,Not(b)) == And(Not(b),a)

print Implies(a, Iff(b,c))
print And(a, Or(Not(b),c))

print Not(a).atom_names()
print a.atom_names()
expr = And(a, Implies(b, Iff(a,c)))
print expr.atom_names()

e = Implies(a,b)
print e.evaluate({"a": False, "b": True})
print e.evaluate({"a": True, "b": False})
e = And(Not(a), Or(b,c))
print e.evaluate({"a": False, "b": False, "c": True})

ex = Implies(a,b)
sat = satisfying_assignments(ex)
print next(sat)
print next(sat)
print next(sat)
e = Iff(Iff(a,b),c)
print list(satisfying_assignments(e))

a, b, c, d, e, f= map(Atom, "abcdef")

print "Or(And(a,b),And(c,d))"
print Or(And(a,b),And(c,d)).to_cnf()
print

print "Or(And(a,b),c)"
print Or(And(a,b),c).to_cnf()
print
print "Or(And(a,b),And(c,d),e)"
print Or(And(a,b),And(c,d),e).to_cnf()
print
print "Or(And(a,Not(b)),And(Not(a),b))"
print Or(And(a,Not(b)),And(Not(a),b)).to_cnf()
print
print "Or(Not(Or(b,c)),a).to_cnf()"
print Or(Not(Or(b,c)),a).to_cnf()
print
print "Or(Not(a),Or(b,c)).to_cnf()"
print Or(Not(a),Or(b,c)).to_cnf()
print

print "Implies(a,Or(b,c)).to_cnf()"
print Implies(a,Or(b,c)).to_cnf()
print
print "Implies(Or(b,c),a).to_cnf()"
print Implies(Or(b,c),a).to_cnf()
print
print "Iff(a,Or(b,c)).to_cnf()"
print Iff(a,Or(b,c)).to_cnf()
'''
############################################################
# Section 2: Logic Puzzles
############################################################

# Puzzle 1

# Populate the knowledge base using statements of the form kb1.tell(...)

kb1 = KnowledgeBase()

mythical = Atom("mythical")
mortal = Atom("mortal")
mammal = Atom("mammal")
horned = Atom("horned")
magical = Atom("magical")
kb1.tell(Implies(mythical,Not(mortal)))
kb1.tell(Implies(Not(mythical),And(mortal,mammal)))
kb1.tell(Implies(Or(mortal,mammal),horned))
kb1.tell(Implies(horned,magical))

# Write an Expr for each query that should be asked of the knowledge base
mythical_query = mythical
magical_query = magical
horned_query = horned


# Record your answers as True or False; if you wish to use the above queries,
# they should not be run when this file is loaded
is_mythical = False
is_magical = True
is_horned = True

# Puzzle 2

# Write an Expr of the form And(...) encoding the constraints
Ann = Atom("a")
John = Atom("j")
Mary = Atom("m")

party_constraints = And(Implies(Or(Ann,Mary),John),Implies(Not(Mary),Ann),Implies(Ann,Not(John)))
# Compute a list of the valid attendance scenarios using a call to
# satisfying_assignments(expr)
valid_scenarios = list(satisfying_assignments(party_constraints))

# Write your answer to the question in the assignment
puzzle_2_question = """
John and Mary will come.
"""

# Puzzle 3

# Populate the knowledge base using statements of the form kb3.tell(...)
kb3 = KnowledgeBase()

p1 = Atom("p1")
e1 = Atom("e1")
p2 = Atom("p2")
e2 = Atom("e2")
s1 = Atom("s1")
s2 = Atom("s2")


kb3.tell(Or(p1,p2))
kb3.tell(Or(e1,e2))
kb3.tell(Not(And(s1,s2)))
kb3.tell(Not(And(p1,p2)))
kb3.tell(Or(s1,s2))


#print [kb3.ask(x) for x in (p1,e1,p2,e2,s1,s2)]

# Write your answer to the question in the assignment; the queries you make
# should not be run when this file is loaded
puzzle_3_question = """
Sign 1 is true. Room1 contain the prize and room2 is empty. 
"""

# Puzzle 4

# Populate the knowledge base using statements of the form kb4.tell(...)
kb4 = KnowledgeBase()
Adams = Atom("ia")
Brown = Atom("ib")
Clark = Atom("ic")
k_Adams = Atom("ka")
k_Brown = Atom("kb")
k_Clark = Atom("kc")

kb4.tell(k_Brown)
kb4.tell(Not(k_Clark))


# Uncomment the line corresponding to the guilty suspect
# guilty_suspect = "Adams"
guilty_suspect = "Brown"
# guilty_suspect = "Clark"

# Describe the queries you made to ascertain your findings
puzzle_4_question = """
I created And clauses between two guys.
"""

############################################################
# Section 3: Feedback
############################################################

feedback_question_1 = """
It took me about 3 days to complete this assignment
"""

feedback_question_2 = """
I find the kb.ask() to be the most challenging in this assignment.
"""

feedback_question_3 = """
I like the cnf part of the assignment because it helped me to understand how to simplify logical expression into cnf.
"""
