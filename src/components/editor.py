# To make sure there is no same entity in one position
taken_positions = set()

class EntityPlaceholder:
    def __init__(self, id, args):
        self.id = id
        self.args = args

    def setup(self):
        global taken_positions
        # For storage in the taken positon, x: 5, y: 7, pos: 50000007
        pos = self.entity.x * 10000000 + self.entity.y
        if not pos in taken_positions:
            taken_positions.add(pos)
        else:
            self.entity.delete_self()

    def breakdown(self):
        global taken_positions
        pos = self.entity.x * 10000000 + self.entity.y
        if pos in taken_positions:
            taken_positions.remove(pos)
        