from copy import deepcopy
from Predicate import Predicate
from Statement import Statement
from Constant import Constant as Const
import time


class Resolution:

    def __init__(self, query, knowledge_base_sentences) -> None:
        self.query = query # query to be put into KB after negation
        self.knowledge_base_sentences = knowledge_base_sentences
        self.KB = set()
        self.predicate_dictionary = {} # mapping each predicate is in which statement
        self.statement_to_object_hash = {} # for mapping statement string to object
        self.var_postfix = 1
    
    def add_query_to_KB(self):
        self.query = Predicate(self.query)
        self.query.negate_predicate()
        new_statement = Statement(self.query.return_predicate())
        self.KB.add(new_statement.statement_string)
        self.statement_to_object_hash[new_statement.statement_string] = new_statement


    def construct_predicate_dictionary(self):
        for statement in self.KB:
            for predicate in self.statement_to_object_hash[statement].predicate_set:
                if predicate.name in self.predicate_dictionary.keys():
                    self.predicate_dictionary[predicate.name] = self.predicate_dictionary[predicate.name].union(set([statement]))
                else:
                    self.predicate_dictionary[predicate.name] = set([statement])


    def inf_to_cnf(self):
        for sentence in self.knowledge_base_sentences:
            if Const.IMPLIES in sentence:
                parts = sentence.split(Const.IMPLIES)
                front_part = parts[0].strip().split(' & ')
                rear_part = parts[1].strip()
                initial = []
                for ele in front_part:
                    if Const.NOT in ele:
                        initial.append(ele[1:])
                    else:
                        initial.append(Const.NOT + ele)
                
                front_part = ' | '.join(initial)

                full_sentence = front_part + ' | ' + rear_part

            else:
                full_sentence = sentence
            
            full_sentence = self.standardize_sentence(full_sentence)
            self.KB.add(full_sentence)
            full_sentence = self.factoring_sentence(full_sentence)
            self.KB.add(full_sentence)
            

    def create_statement_object_hash(self):
        for ele in self.KB:
            new_statement = Statement(ele)
            self.statement_to_object_hash[new_statement.statement_string] = new_statement


    def FOL_resolution_unit(self):

        while True:
            new_statements = set()

            for statement1 in self.KB:

                if len(self.statement_to_object_hash[statement1].predicates) > 1:
                    continue
                resolving_clauses = self.statement_to_object_hash[statement1].get_resolving_clauses(self.predicate_dictionary)
                for statement2 in resolving_clauses:

                    if statement1 == statement2:
                        continue
                    resolvent = self.statement_to_object_hash[statement1].resolve(self.statement_to_object_hash[statement2])
                    if resolvent == False:
                        return True

                    new_statements = new_statements.union(resolvent)
            
            if new_statements.issubset(self.KB):
                return False
            
            new_statements = new_statements.difference(self.KB)

            for statement in new_statements:
                self.KB.add(statement)
                temp = Statement(statement)
                self.statement_to_object_hash[statement] = temp
                for predicate in temp.predicate_set:
                    self.predicate_dictionary[predicate.name] = self.predicate_dictionary[predicate.name].union(set([statement]))


    def standardize_sentence(self, sentence):
        var_hash = {}
        sentence = sentence.split(' | ')
        standrd_predlist = []
        for predicate in sentence:
            parts = predicate.split('(')
            pred_name = parts[0]
            pred_arguments = parts[1][:-1].split(',')

            for i in range(len(pred_arguments)):
                if pred_arguments[i].islower():
                    if pred_arguments[i] in var_hash.keys():
                        pred_arguments[i] = var_hash[pred_arguments[i]]
                    else:
                        newvar = Const.VARIABLE_PREFIX + str(self.var_postfix)
                        var_hash[pred_arguments[i]] = newvar
                        pred_arguments[i] = newvar
                        self.var_postfix += 1
            
            standrd_predlist.append(pred_name + '(' + ','.join(pred_arguments) + ')')
        
        return ' | '.join(standrd_predlist)


    def factoring_sentence(self, statement):
        tempstatement = Statement(statement)
        completed = False 

        while not completed:
            is_completed = True

            for pred1 in tempstatement.predicates:
                unif_found = False
                for pred2 in tempstatement.predicates:

                    if pred1 == pred2:
                        continue

                    unification = False

                    if (not ( pred1.negative ^ pred2.negative)) and pred1.name == pred2.name:
                        unification = pred1.unify_predicate(pred2)

                    if unification == False:
                        continue
                    
                    else:
                        other_preds = []
                        for pred in tempstatement.predicates:
                            if pred.predicate_string != pred1.predicate_string and pred.predicate_string != pred2.predicate_string:
                                other_preds.append(pred)
                        
                        final_preds = []
                        for preds in other_preds:
                            new_pred = deepcopy(preds)
                            final_preds.append(new_pred.substitute_in_predicate(unification))

                        new_pred = deepcopy(pred1)
                        final_preds.append(new_pred.substitute_in_predicate(unification))
                        new_statement = Statement()
                        new_statement.predicate_set_to_string(set(final_preds))
                        tempstatement = Statement(new_statement.statement_string)
                        unif_found = True
                        is_completed = False
                        break
                if unif_found:
                    break
        
            if is_completed:
                completed = True

        return tempstatement.statement_string


    def print_KB(self):
        print("KB: ")
        for ele in self.KB:
            print(ele)


def inputdata(path):
    with open(path) as file:
        input_lines = [line.strip() for line in file]

    queries = []
    knowledge_base_sentences = []
    counter = 1

    while counter <= int(input_lines[0]):
        queries.append(input_lines[counter])
        counter += 1

    last_line_number = int(input_lines[0]) + int(input_lines[counter]) + 1
    counter += 1

    while counter <= last_line_number:
        knowledge_base_sentences.append(input_lines[counter])
        counter += 1
    
    return queries, knowledge_base_sentences


def outputfile(result, path):
    with open(path, 'w') as file:
        result = '\n'.join(['TRUE' if ele else 'FALSE' for ele in result])
        file.write(result)


if __name__ == '__main__':

    queries, knowledge_base_sentences = inputdata(Const.input_file)
    result = []
    starttime = time.time()
    
    for query in queries:
        resolution = Resolution(query, knowledge_base_sentences)
        resolution.inf_to_cnf()
        resolution.create_statement_object_hash()
        resolution.add_query_to_KB()
        resolution.construct_predicate_dictionary()
        query_result = resolution.FOL_resolution_unit()
        result.append(query_result)
        
    outputfile(result, Const.output_file)