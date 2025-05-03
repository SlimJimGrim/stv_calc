# VoD STV Cawcuwatow

import math
import csv
import random

INPUT_FILE = 'example_input.csv'
NUM_SEATS = 13

STANDINGS_EVERY_ELECTED = True
STANDINGS_EVERY_ELIM    = True


# Ballot class
class Ballot:

    def __init__(self, ranks):
        self.ranks = ranks
        self.weight = 1
        self.top = -1
    
    def remove_candidate(self, index):
        
        self.top = -1
        self.ranks.pop(index)

    def top_candidate(self):

        # Skip if already known
        if self.top != -1:
            return self.top

        min_val = None
        min_ind = -1

        for i, x in enumerate(self.ranks):
            if x != 0 and (min_val is None or x < min_val):
                min_val = x
                min_ind = i
        
        self.top = min_ind
        return min_ind
    
    def reweight(self, weight_factor):
        self.weight *= weight_factor

    def get_weight(self):
        return self.weight

# Ballot management class
class Election:
    def __init__(self):

        self.candidates, self.ballots = self.__fill_ballots()
        self.quota = self.calc_quota()

    def __int_filter(self, num_string):
        if num_string == '':
            return 0
        
        return int(num_string)

    def __fill_ballots(self):
        ballot_list = []

        try:
            with open(INPUT_FILE, 'r', encoding="utf-8", errors='ignore') as file:
                csvFile = csv.reader(file)

                candidates = next(csvFile)

                for row in csvFile:
                    ballot_list.append(Ballot(list(map(self.__int_filter, row))))
        
        except Exception as exc:
            print(f"Unabwe tuwu wead fiwe {INPUT_FILE} TwT")
            print(exc)
            exit(1)

        return candidates, ballot_list

    def calc_quota(self):
        
        return math.floor(len(self.ballots) / (NUM_SEATS + 1) + 1)
        #return len(self.ballots) / (NUM_SEATS + 1) + 1


    def num_remaining(self):
        return len(self.candidates)

    def remove_candidate(self, index):

        for ballot in self.ballots:
            ballot.remove_candidate(index)
        
        return self.candidates.pop(index)

    def calc_reweight_factor(self, num_votes):
        return ((num_votes - self.quota) / num_votes)

    def reweight_ballots(self, index, weight):

        for ballot in self.ballots:
            if ballot.top_candidate() == index:
                ballot.reweight(weight)

    # Change tiebreaker function depending on law
    def tiebreak(self, list):

        return random.choice(list)
    
    def get_ranks(self):

        cand_score = [0]*len(self.candidates)

        for ballot in self.ballots:
            index = ballot.top_candidate()
            if index != -1:
                cand_score[index] += ballot.get_weight()

        return cand_score

    def get_round(self):
        
        cand_score = self.get_ranks()

        # print(cand_score)

        top_score = max(cand_score)
        
        if top_score >= self.quota:
            # Candidate is elected
            top_cand = self.tiebreak([i for i, val in enumerate(cand_score) if val == top_score])
            top_cand_name = self.get_candidate_name(top_cand)

            reweight = self.calc_reweight_factor(top_score)
            self.reweight_ballots(top_cand, reweight)

            self.remove_candidate(top_cand)

            return 1, top_cand_name

        else:
            # No candidate is elected
            lowest_score = min(cand_score)
            #print(f"Lowest Score: {lowest_score}")
            elim_cand = self.tiebreak([i for i, val in enumerate(cand_score) if val == lowest_score])
            elim_cand_name = self.get_candidate_name(elim_cand)

            self.remove_candidate(elim_cand)

            if (lowest_score < 0.01):
                return -1, elim_cand_name

            return 0, elim_cand_name
        
    def get_remaining_cand(self):
        return self.candidates
    
    def get_candidate_name(self, index):
        return self.candidates[index]
    
    def get_curr_standings(self):

        ranks = self.get_ranks()

        # Pair lists
        pairs = [(self.candidates[i], ranks[i]) for i in range(len(ranks))]

        pairs.sort(key=lambda x: x[1], reverse=True)

        return pairs

def print_tuples(tuples, align):
    print("\ncuwwent standings:")
    for i, tuple, in enumerate(tuples):
        spaces = " "*(align - len(tuple[0])- len(str(i+1)))
        print(f"  {i + 1}. {tuple[0]}{spaces}({tuple[1]})")


def print_tuples_diff(tuples, prev, align):
    print("\ncuwwent standings:")
    for i, tuple, in enumerate(tuples):
        prev_tup = next(filter(lambda x: x[0] == tuple[0], prev))

        spaces = " "*(align - len(tuple[0]) - len(str(i+1)))

        if (tuple[1] - prev_tup[1] > 0.001):
            print(f"  {i + 1}. {tuple[0]}{spaces}({tuple[1]:.2f}) (+{(tuple[1] - prev_tup[1]):.2f})")
        else:
            print(f"  {i + 1}. {tuple[0]}{spaces}({tuple[1]:.2f})")
    print()


def main():

    print(f"Cawcuwating stv...")

    num_elected = 0
    elected = []
    election = Election()

    print(f"Numbew of votes: {len(election.ballots)}")
    print(f"Qwuota: {election.quota}")

    # Get initial first ranks
    prev_tup = election.get_curr_standings()
    print_tuples(prev_tup, 40)
    print("\n"+"-"*80)

    print(f"\nWound {num_elected + 1}:")

    while (election.num_remaining() + num_elected > NUM_SEATS) and (num_elected < NUM_SEATS):
        is_elected, cand_name = election.get_round()

        if is_elected == 1:
            print("\n"+"#"*64)
            print(f"# {cand_name} iws ewected!!!! OwO")
            print("#"*64)
            elected.append(cand_name)
            num_elected += 1

            if STANDINGS_EVERY_ELECTED:
                curr_tuff = election.get_curr_standings()
                print_tuples_diff(curr_tuff, prev_tup, 40)
                prev_tup = curr_tuff
                print("\n"+"-"*80)

            if num_elected != NUM_SEATS:
                print(f"\nWound: {num_elected + 1}")

        else:
            print("\n"+"~"*64)
            print(f"~ {cand_name} iws ewiminated TwT")
            print("~"*64)

            if STANDINGS_EVERY_ELIM and STANDINGS_EVERY_ELECTED and is_elected != -1:
                curr_tuff = election.get_curr_standings()
                print_tuples_diff(curr_tuff, prev_tup, 40)
                prev_tup = curr_tuff
    
    if num_elected != NUM_SEATS:
        print(f"\nWinnews by defauwt:")
        for cand in election.get_remaining_cand():
            elected.append(cand)
            print(f"  {cand} iws ewected by defauwt!!!! OwO")

    print(f"\nThe fowwowing candidates have bewn ewected:")
    for i, cand in enumerate(elected):
        print(f"  {i+1}.\t{cand}")

    print(f"\nAww done! uwu")
    




if __name__ == "__main__":
    main()

