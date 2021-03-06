import GameModels as g
import Heuristics as he
import time as t

def main():

    # It gives the user the option to choose the (odd) level up to where he will come to explore the minMax
    level = input("Choose the depth you want to get to explore the tree : ")
    # From the rules of Othello the starting player is always black
    # Remember: k--> black, w--> white, '-'--> empty cell
    turn = 'k'

    print("All the moves of the play are saved in the file.\n")

    # Each play is saved on a file
    file_name = input("Choose a name for the file: ")
    file_path = "output/{}.txt".format(file_name)
    print("Please, wait...\n")
    out = open(file_path, "w")
    start = t.time()

    out.write("Starting player is: {}\n".format(turn))
    out.write("Level: {}\n\n\n".format(level))

    heuristic = he.OthelloHeuristic()
    othello = g.OthelloGame(heuristic)

    # Initial state of the game
    ix = othello.state
    out.write("\nInitial configuration: \n {}\n\n".format(ix.representation.board))

    #Start the game
    while True:
        # Save the states that it's possible to reach from the current state knowing the current turn
        states = othello.neighbors(turn, ix)
        # Initial value gives to find a better heuristic value (it is valid only in the first iteration, in next
        # iterations will be save the best heuristic value compute)
        mx = -9999
        # Save the last state in ix on prev because we must denied to stay always in the same state at least it is the
        # only possible move
        prev = ix

        # Start to explore the states
        for s in states:
            # for each state in states
            # if the state is the previous one make it less valuable (so you will not choose always the same state at
            # least it is the only possible move)
            if s == prev:
                # set h to -500 (arbitrary low)
                h = -500
            # if the state is not equal to the previus one
            else:
                # compute the heuristic on the state s
                h = heuristic.MinMax(othello, s, level, turn)

            # if the returned value from the heuristic method is grather than mx
            if h > mx:
                # save the new value in mx
                mx = h
                # save the state associate to the best heuristic value found
                ix = s

        # Write the move's player on the file
        out.write("\nplayer {}, move:\n {}\n\n".format(turn, ix.representation.board))
        print("player {}, move:\n {}\n\n".format(turn, ix.representation.board))


        # Return the winner of the game
        winner = ix.is_final()

        # If ther's a winner
        if winner is not None:
            print("The game is finished! The winnwr is: {}".format(winner))
            # write the winner in the file
            out.write("The winner is player: {}\n".format(winner))
            end = t.time() - start
            # close file
            out.write("The time spent is: {}".format(end))
            out.close()

            print("The time spent is: {}".format(end))
            break
        # otherwise give the control to the other player
        turn = he.OthelloHeuristic.get_enemy_color(turn)


if __name__ == "__main__":
    main()
