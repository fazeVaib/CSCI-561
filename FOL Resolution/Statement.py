from Predicate import Predicate
from Constant import Constant as Const 
from copy import deepcopy

class Statement:

    def __init__(self, statement_string = None) -> None:
                
        if statement_string:
            self.statement_string = statement_string
            self.predicates = []
            self.string_to_predicates()
            self.predicate_set = set(self.predicates)
        else:
            self.predicate_set = None
            self.statement_string = None


    def string_to_predicates(self):

        for ele in self.statement_string.split(' | '):
            self.predicates.append(Predicate(ele))
    
    def predicate_set_to_string(self, predicate_set):

        self.predicate_set = predicate_set
        all_pred_strings = map(lambda x : x.predicate_string, predicate_set)
        self.statement_string = ' | '.join(all_pred_strings)


    def resolve(self, statement):
        new_statements = set()
        
        for pred1 in self.predicates:
            
            for pred2 in statement.predicates:
                unification = False
                
                if (pred1.negative ^ pred2.negative) and pred1.name == pred2.name:
                    unification = pred1.unify_predicate(pred2)
                
                if unification == False:
                    continue
                
                else:
                    statement_p1 = []
                    statement_p2 = []

                    for predicate in self.predicate_set:
                        if predicate.predicate_string != pred1.predicate_string:
                            statement_p1.append(predicate)
                    
                    for predicate in statement.predicate_set:
                        if predicate.predicate_string != pred2.predicate_string:
                            statement_p2.append(predicate)
                    
                    if not statement_p1 and not statement_p2:
                        return False
                    
                    other_predicates = []

                    for predicate in statement_p1:
                        deepcopy_pred = deepcopy(predicate)
                        other_predicates.append(deepcopy_pred.substitute_in_predicate(unification))
                    
                    for predicate in statement_p2:
                        deepcopy_pred = deepcopy(predicate)
                        other_predicates.append(deepcopy_pred.substitute_in_predicate(unification))

                    temp_statement = Statement()
                    temp_statement.predicate_set_to_string(set(other_predicates))
                    new_statements.add(temp_statement.statement_string)

        return new_statements

    
    def get_resolving_clauses(self, predicate_dictionary):
        resolving_clauses = set()
        
        for predicate in self.predicate_set:
            if predicate.name in predicate_dictionary.keys():
                resolving_clauses = resolving_clauses.union(predicate_dictionary[predicate.name]) 
        
        return resolving_clauses


    def return_statement(self):
        
        return " | ".join([x.return_predicate() for x in self.predicates])
