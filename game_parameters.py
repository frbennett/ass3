

class set_game_paramters():
    def __init__(self):
        self.levels = []

        # set up first frame parameters
        current_frame = {}
        current_frame['counts'] = [5, 5, 5, 5]
        current_frame['dead_cells'] = {(2, 2), (2, 3), (2, 4),
                      (3, 2), (3, 3), (3, 4),
                      (4, 2), (4, 3), (4, 4),
                      (0, 7), (1, 7), (6, 7), (7, 7)}
        current_frame['moves']=20
        current_frame['size']=(8,8)
        current_frame['basic_dots'] = 10
        current_frame['wild_dots'] = 1

        self.levels.append(current_frame)

        # set up second frame parameters
        current_frame = {}
        current_frame['counts'] = [10, 15, 25, 25]
        current_frame['dead_cells'] = {(2, 2), (2, 3), (2, 4),
                                       (3, 2), (3, 3), (3, 4),
                                       (4, 2), (4, 3), (4, 4),
                                       (0, 7), (1, 7), (6, 7), (7, 7)}
        current_frame['moves'] = 20
        current_frame['size'] = (12, 12)
        current_frame['basic_dots'] = 10
        current_frame['wild_dots'] = 1

        self.levels.append(current_frame)

        # set up third frame parameters
        current_frame = {}
        current_frame['counts'] = [10, 15, 25, 25]
        current_frame['dead_cells'] = {(2, 2), (2, 3), (2, 4),
                                       (3, 2), (3, 3), (3, 4),
                                       (4, 2), (4, 3), (4, 4),
                                       (0, 7), (1, 7), (6, 7), (7, 7)}
        current_frame['moves'] = 20
        current_frame['size'] = (12, 12)
        current_frame['basic_dots'] = 10
        current_frame['wild_dots'] = 1

        self.levels.append(current_frame)



