import numpy as np
import pdb

#TODO
    # add discount and halting conditions

grid = [["", "", "", "", "", ""],
        ["", "", "", "+10", "blocked", ""],
        ["blocked", "blocked", "", "", "blocked", ""],
        ["+100", "blocked", "", "", "blocked", "+20"],
        ["", "blocked", "+5", "", "blocked", ""],
        ["", "", "", "", "", ""]]

arrow_grid = [["   ", "   ", "   ", "   ", "   ", "   "],
                ["   ", "   ", "   ", "   ", "   ", "   "],
                ["   ", "   ", "   ", "   ", "   ", "   "],
                ["   ", "   ", "   ", "   ", "   ", "   "],
                ["   ", "   ", "   ", "   ", "   ", "   "],
                ["   ", "   ", "   ", "   ", "   ", "   "]]

gamma = 1.0

pdb.set_trace()
for i in range(5):
    for j in range(len(grid)):
        for k in range(len(grid[0])):
            vals = []
            if grid[j][k] != "blocked":
                # if k == 2:
                #     pdb.set_trace()

                if grid[j][k] == "":
                    val_stay = 0
                else:
                    val_stay = float(grid[j][k])
                val_to_stay_still = 0.1 * val_stay
                vals.append(val_to_stay_still)

                # -------------------------------------------------

                if j > 0 and grid[j-1][k] != "blocked":
                    if arrow_grid[j-1][k] == " v ":
                        prob_up = 0.2
                    else:
                        prob_up = 0.7

                    if grid[j-1][k] == "" or grid[j-1][k] == "blocked":
                        val_up = 0
                    else:
                        val_up = float(grid[j-1][k])

                    val_to_go_up = prob_up * val_up
                    vals.append(val_to_go_up)
                else:
                    vals.append(0)

                # -------------------------------------------------

                if k < len(grid[0])-1 and grid[j][k+1] != "blocked":
                    if arrow_grid[j][k+1] == " < ":
                        prob_right = 0.2
                    else:
                        prob_right = 0.7

                    if grid[j][k+1] == "" or grid[j][k+1] == "blocked":
                        val_right = 0
                    else:
                        val_right = float(grid[j][k+1])

                    val_to_go_right = prob_right * val_right
                    vals.append(val_to_go_right)
                else:
                    vals.append(0)

                # -------------------------------------------------

                if j < len(grid)-1 and grid[j+1][k] != "blocked":
                    if arrow_grid[j+1][k] == " ^ ":
                        prob_down = 0.2
                    else:
                        prob_down = 0.7

                    if grid[j+1][k] == "" or grid[j+1][k] == "blocked":
                        val_down = 0
                    else:
                        val_down = float(grid[j+1][k])

                    val_to_go_down = prob_down * val_down
                    vals.append(val_to_go_down)
                else:
                    vals.append(0)

                # -------------------------------------------------

                if k > 0 and grid[j][k-1] != "blocked":
                    if arrow_grid[j][k-1] == " > ":
                        prob_left = 0.2
                    else:
                        prob_left = 0.7

                    if grid[j][k-1] == "" or grid[j][k-1] == "blocked":
                        val_left = 0
                    else:
                        val_left = float(grid[j][k-1])

                    val_to_go_left = prob_left * val_left
                    vals.append(val_to_go_left)
                else:
                    vals.append(0)

                values = np.array(vals)
                new_value = val_stay + gamma * np.amax(values)
                grid[j][k] = str(new_value)
                policy = np.argmax(values)

                if policy == 0:
                    arrow_grid[j][k] = " s "
                elif policy == 1:
                    arrow_grid[j][k] = " ^ "
                elif policy == 2:
                    arrow_grid[j][k] = " > "
                elif policy == 3:
                    arrow_grid[j][k] = " v "
                else:
                    arrow_grid[j][k] = " < "

            for row in arrow_grid:
                print row
            print "\n"
            for row in grid:
                print row
            print "\n"
