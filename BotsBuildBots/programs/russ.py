import random

import utilities

class Russ_Challenge:
    DIRS = ["north", "east", "south", "west"]
    VECS = [(0,1), (1,0), (0,-1), (-1,0)]

    def __init__(self):
        self.cur_dir = 0
        self.mode    = "start"
        self.succeed_count = 0

    def run(self, taskResponse):
        if taskResponse == False:
            # we failed to move.  We *might* have been in the initial
            # run toward the edge, or we might have attempted to move
            # while edge-tracing, and failed.  Either way, we turn
            # right, attempt to move in that new direction, remind
            # ourselves to turn *left* on the next step.
            self.mode = "after_dodge"    # most of the time, redundant
            self.succeed_count = 0
            self.cur_dir += 1
            self.cur_dir %= len(self.DIRS)
        else:
            # occasionally, a robot gets blocked, but not because of
            # a wall - it gets blocked by another robot.  This can cause
            # an infinite loop of "move, turn left".  This detects that
            # special case; if we do that 3 times in a row, then we'll
            # revert back to the start state.
            self.succeed_count += 1
            if self.succeed_count == 3:
                self.mode = "start"

            # we successfully just moved.  What we do next depends on
            # our mode.  If we are in "start" mode, then it means that
            # we've *NEVER* found an edge (yet).  So we keep searching
            # in that direction, no change.  But, if we're in the
            # "after_dodge" mode, then we know that our last move was
            # to turn right (perhaps twice?) and then move; we want to
            # turn left again, and see if there is now a space.  If so,
            # we move into it (going "around" the end of a wall); if
            # not, then we will fail a move, and do the "dodge" again.
            if self.mode != "start":
                self.cur_dir += len(self.DIRS)-1
                self.cur_dir %= len(self.DIRS)

        return { "task":       "move",
                 "parameters": self.DIRS[self.cur_dir]}



class Russ_Mapper:
    history = {}

    DIRS = ["north", "east", "south", "west"]
    VECS = [(0,1), (1,0), (0,-1), (-1,0)]

    def __init__(self):
        # these are RELATIVE positions - relative to the 
        self.x = 0
        self.y = 0
        #self.history = {(0,0): 1}
        self.cur_dir = None

        #self.id = random.randint(0,1000)
        #self.ids.add(self.id)

        #print(f"I am robot {self.id}.  I can see robots: {self.ids}")
        #input()
    
    def calc_dest(self, dir_):
        assert dir_ in range(4)
        return (self.x + self.VECS[dir_][0],
                self.y + self.VECS[dir_][1])

    def add_to_history(self, dest, val=1):
        if dest in self.history:
            self.history[dest] += val
        else:
            self.history[dest]  = val

    def get_history(self, dest):
        return self.history.get(dest, 0)

    def run(self, taskResponse):
        if taskResponse is None:
            # only happens on the first iteration.  Set up the initial
            # move.
            self.cur_dir = 0   # default to North, no particular reason why
        elif taskResponse == False:
            # we failed to move.  Record the location that we attempted
            # to enter as part of the history, so we'll never try to
            # move there again.
            #
            # Note that we add 5 at a time to make it *very* unlikely
            # that we'll come back here (just traversing a block only
            # adds 1)
            self.add_to_history(self.calc_dest(self.cur_dir), 5)
        else:
            # we succeed moving.  Update the location
            (self.x,self.y) = self.calc_dest(self.cur_dir)
            self.add_to_history((self.x, self.y))

        # which of the 4 directions has the lowest history value?  If
        # there's a tie, we'll choose the one that puts us furthest
        # from the center.  If there's a tie in that as well, then we'll
        # default to the lowest index.
        best_path    = 0
        dest         = self.calc_dest(best_path)
        cost_of_best = self.get_history(dest)
        dist_of_best = dest[0]**2 + dest[1]**2

        for d in range(1,len(self.DIRS)):
            dest = self.calc_dest(d)
            cost = self.get_history(dest)
            dist = dest[0]**2 + dest[1]**2

            if cost <  cost_of_best or \
               cost == cost_of_best and dist > dist_of_best:
                best_path    = d
                cost_of_best = cost
                dist_of_best = dist
        
        self.cur_dir = best_path

        return { "task":       "move",
                 "parameters": self.DIRS[self.cur_dir]}
