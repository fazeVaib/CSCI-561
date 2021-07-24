class Predicate:

    def __init__(self, predicate_string) -> None:
        
        self.negative = False
        self.predicate_string = predicate_string
        temp = predicate_string.split('(')
        self.name = temp[0]
        
        if '~' in temp[0]:
            self.name = temp[0][1:]
            self.negative = True
        
        self.arguments = temp[1][:-1].split(',')


    def unify_predicate(self, predicate):        
        if self.name == predicate.name and len(self.arguments) == len(predicate.arguments):
            substitution = {}
            return unify(self.arguments, predicate.arguments, substitution)
        else:
            return False


    def substitute_in_predicate(self, substitution):
        
        if substitution:
            for i, ele in enumerate(self.arguments):
                if ele in substitution:
                    self.arguments[i] = substitution[ele]
            self.update_predicate()
        
        return self

    def update_predicate(self):
        self.predicate_string = '~'[not self.negative:] + self.name + '(' + ','.join(self.arguments) + ')'
    

    def negate_predicate(self):
        self.negative = not self.negative
        self.update_predicate()


    def return_predicate(self):
        
        if self.negative:
            return '~' + self.name + '(' + ','.join(self.arguments) + ')'
        
        return self.name + '(' + ','.join(self.arguments) + ')'


def unify(p1_args, p2_args, substitution):

    if substitution == False:
        return False
    
    elif p1_args == p2_args:
        return substitution

    elif isinstance(p1_args, str) and p1_args.islower():
        return unify_var(p1_args, p2_args, substitution)
    
    elif isinstance(p2_args, str) and p2_args.islower():
        return unify_var(p2_args, p1_args, substitution)
    
    elif isinstance(p1_args, list) and isinstance(p2_args, list):
        if p1_args and p2_args:
            return unify(p1_args[1:], p2_args[1:], unify(p1_args[0], p2_args[0], substitution))
        else:
            return substitution
    
    else:
        return False


def unify_var(var, x, substitution):

    if var in substitution:
        return unify(substitution[var], x, substitution)
    
    elif x in substitution:
        return unify(var, substitution[x], substitution)
    
    else:
        substitution[var] = x
        return substitution