class SokobanMoving:

    """
    Sokoban-moving presenter

    Description
        This module defines "position index" as marked number that represents each cell's position in Sokoban map.
        If a shape of Sokoban map is (4, 5), then position indexes are as below.
            [[0, 1, 2, 3, 4],
             [5, 6, 7, 8, 9],
             [10, 11, 12, 13, 14],
             [15, 16, 17, 18, 19]]

    Parameters
    ----------
    nrow : int
        Height of Sokoban map.
    ncol : int
        Width of Sokoban map.
    storage_position : list[int]
        Position index for storage (a destination of boxes).
    wall_position : list[int]
        Position index for wall (neither player nor boxes can get in). It is not necessary to include the walls of the border area.
    """

    def __init__(self, nrow, ncol, storage_position, wall_position):
        self.nrow = nrow
        self.ncol = ncol
        self.storage_position = storage_position
        self.wall_position = wall_position
        self.directions = {'up': -self.ncol, 'down': self.ncol, 'left': -1, 'right': 1}
        return

    def do_action(self, player_position, box_position, direction):

        """
        Returns the position change of the structures (player and boxes),
        according to the movement direction of the player on the map.

        Parameters
        ----------
        player_position : int
            Position index for player.
        box_position : list[int]
            Position index for boxes.
        direction : str
            One of 'up', 'down', 'left', and 'right'. A direction for player to go.
        
        Returns
        -------
        movable : bool
            Boolean indicating whether the player can move designated direction.
        next_pos : int
            Position index for player after moving.
        next_box : list[int]
            Position index for boxes after moving.
        """

        movable = self.is_movable(player_position, box_position, direction)
        if movable:
            next_pos = player_position + self.directions[direction]
            next_box = [box + self.directions[direction] if next_pos == box else box for box in box_position]
        else:
            next_pos = player_position
            next_box = box_position.copy()
        return movable, next_pos, next_box

    def is_movable(self, player_position, box_position, direction):
        if self.is_corner(player_position, direction):
            result = False
        else:
            forward = self.directions[direction]
            next_pos = player_position + forward
            if next_pos in self.wall_position:
                result = False
            elif next_pos in box_position:
                if self.is_corner(next_pos, direction):
                    result = False
                else:
                    next2_pos = next_pos + forward
                    if next2_pos in self.wall_position or next2_pos in box_position:
                        result = False
                    else:
                        result = True
            else:
                result = True
        return result

    def is_corner(self, pos, direction):
        if direction == 'up' and pos < self.ncol:
            result = True
        elif direction == 'down' and pos >= self.nrow * self.ncol - self.ncol:
            result = True
        elif direction == 'left' and pos % self.ncol == 0:
            result = True
        elif direction == 'right' and (pos + 1) % self.ncol == 0:
            result = True
        else:
            result = False
        return result

    def is_boxes_stuck(self, box_position):

        """
        Seeing at the location of the boxes on the map, it checks if any of the boxes are in an immovable position.

        Parameters
        ----------
        box_position : list[int]
            Position index for boxes.
        """

        is_stuck = False
        for box in box_position:
            if self.is_box_stuck(box, box_position):
                is_stuck = True
                break
        return is_stuck

    def is_box_stuck(self, box, box_position):
        not_pushable = {direction: not self.is_box_pushable(box, box_position, direction, [])
                        for direction in self.directions.keys()}
        if box in self.storage_position:
            is_stuck = False
        else:
            is_stuck = (not_pushable['up'] or not_pushable['down']) and (not_pushable['left'] or not_pushable['right'])
        return is_stuck

    def is_box_pushable(self, box, box_position, direction, searched_boxes):
        neighbor = box + self.directions[direction]
        if neighbor in searched_boxes:
            is_pushable = False
        elif self.is_corner(box, direction) or neighbor in self.wall_position:
            is_pushable = False
        elif neighbor in box_position:
            if direction in ['up', 'down']:
                is_pushable = self.is_box_pushable(neighbor, box_position, 'left', [box] + searched_boxes) and \
                              self.is_box_pushable(neighbor, box_position, 'right', [box] + searched_boxes)
            else:
                is_pushable = self.is_box_pushable(neighbor, box_position, 'up', [box] + searched_boxes) and \
                              self.is_box_pushable(neighbor, box_position, 'down', [box] + searched_boxes)
        else:
            is_pushable = True
        return is_pushable
