from maze.cell import Cell

def test_cell_initialization():
    cell = Cell(2, 3)

    assert cell.row == 2
    assert cell.col == 3

def test_cell_has_all_walls():
    cell = Cell(0, 0)

    assert cell.walls["up"] is True
    assert cell.walls["down"] is True
    assert cell.walls["right"] is True
    assert cell.walls["left"] is True