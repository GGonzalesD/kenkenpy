#!/usr/bin/python3

from ortools.sat.python import cp_model
import functools, operator

class Block:
    ADD, DIF, MUL, DIV, SET = range(5)
    def __init__(self, op, r, *coords):
        self.op = op
        self.r = r
        self.coords = list(coords)

        if self.op in (Block.DIF, Block.DIV) and len(self.coords) != 2:
            raise Exception(f"Operaciones de tipo DIF y DIV necesitan solo de 2 variables!")

        

def make_matrix(model:cp_model.CpModel, n, *blocks):
    setters = list(filter(lambda b:b.op==Block.SET, blocks))
    matrix = [[ model.NewIntVar(1, n, f"v_{i}_{j}")
            for i in range(n) ] for j in range(n)
    ]
    for s in setters:
        i, j = s.coords[0]
        matrix[j][i] = model.NewIntVar(s.r, s.r, f"v_{i}_{j}")
    return matrix

def generate_contraints(model:cp_model.CpModel, matrix, *blocks):
    for l in matrix:
        model.AddAllDifferent(l)
    for l in zip(*matrix):
        model.AddAllDifferent(l)

    for block in blocks:
        block:Block

        vars = [matrix[j][i] for i,j in block.coords]
        
        if block.op == Block.ADD:
            constraint = functools.reduce(operator.add, vars) == block.r
            model.Add(constraint)
        
        if block.op == Block.MUL:
            if len(vars) < 3:
                model.AddMultiplicationEquality(block.r, vars)
            elif len(vars) == 3:
                tmp = model.NewIntVar(1, int(1e9), "_tmp_")
                model.AddMultiplicationEquality(tmp, vars[:2])
                model.AddMultiplicationEquality(block.r, [tmp, vars[-1]])
            else:
                tmps = [model.NewIntVar(1, int(1e9), f"_tmp_{_}") for _ in range(len(vars)-2)]
                model.AddMultiplicationEquality(tmps[0], vars[:2])
                for i in range(0, len(tmps)-1):
                    model.AddMultiplicationEquality(tmps[i+1], [tmps[i], vars[i+2]])
                model.AddMultiplicationEquality(block.r, [tmps[-1], vars[-1]])

        if block.op == Block.DIV:
            va, vb = vars
            bools = [model.NewBoolVar(f"bool_{i}_{va.Name()}_{vb.Name()}") for i in range(2)]
            bool_a, bool_b = bools

            model.Add(va*block.r == vb).OnlyEnforceIf(bool_a)
            model.Add(vb*block.r == va).OnlyEnforceIf(bool_b)
            model.Add(sum(bools) == 1)

        if block.op == Block.DIF:
            va, vb = vars
            bools = [model.NewBoolVar(f"bool_{i}_{va.Name()}_{vb.Name()}") for i in range(2)]
            bool_a, bool_b = bools
            
            model.Add(va-vb == block.r).OnlyEnforceIf(bool_a)
            model.Add(vb-va == block.r).OnlyEnforceIf(bool_b)
            model.Add(sum(bools) == 1) 


def draw_matrix(matrix):
    for l in matrix:
        for v in l:
            print(v, end=" ")
        print()

def solve(raw_blocks, n):
    model = cp_model.CpModel()
    solver = cp_model.CpSolver()

    blocks = [
        Block(bloc['op'], bloc['r'], *bloc['coords']) for bloc in raw_blocks
        if len(bloc['coords']) > 0
    ]
    matrix = make_matrix(model, n, *blocks)
    generate_contraints(model, matrix, *blocks)

    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        return [
        [ solver.Value(matrix[j][i]) for i in range(n)] for j in range(n) ]
    else:
        return None

if __name__ == "__main__":
    
    model = cp_model.CpModel()
    solver = cp_model.CpSolver()

    n = 10
    blocks = [
        Block(Block.ADD, 14, (0, 0), (1, 0), (0, 1)),
        Block(Block.SET, 9, (0, 2)),
        Block(Block.ADD, 32, (0, 3), (0, 4), (1, 3), (1, 4), (2, 2), (2, 3)),
        Block(Block.ADD, 8, (0, 5), (0, 6)),
        Block(Block.ADD, 14, (0, 7), (1, 7)),
        Block(Block.ADD, 3, (0, 8), (0, 9)),
        Block(Block.ADD, 15, (1, 1), (1, 2), (2, 1)),
        Block(Block.ADD, 15, (1, 5), (2, 5)),
        Block(Block.ADD, 11, (1, 6), (2, 6)),
        Block(Block.DIF, 4, (1, 8), (1, 9)),
        Block(Block.MUL, 6, (2, 0), (3, 0)),
        Block(Block.DIF, 1, (2, 4), (3, 4)),
        Block(Block.ADD, 6, (2, 7), (2, 8)),
        Block(Block.MUL, 50, (2, 9), (3, 9)),
        Block(Block.SET, 1, (3, 1)),
        Block(Block.DIF, 3, (3, 2), (4, 2)),
        Block(Block.DIV, 7, (3, 3), (4, 3)),
        Block(Block.ADD, 15, (3, 5), (4, 5)),
        Block(Block.DIF, 1, (3, 6), (4, 6)),
        Block(Block.DIF, 6, (3, 7), (4, 7)),
        Block(Block.ADD, 13, (3, 8), (4, 8)),
        Block(Block.SET, 8, (4, 0)),
        Block(Block.SET, 10, (4, 1)),
        Block(Block.SET, 2, (4, 4)),
        Block(Block.SET, 4, (4, 9)),
        Block(Block.SET, 7, (5, 0)),
        Block(Block.ADD, 18, (5, 1), (5, 2), (6, 1)),
        Block(Block.ADD, 11, (5, 3), (5, 4)),
        Block(Block.ADD, 5, (5, 5), (6, 5)),
        Block(Block.ADD, 15, (5, 6), (5, 7)),
        Block(Block.ADD, 11, (5, 8), (5, 9)),
        Block(Block.DIF, 5, (6, 0), (7, 0)),
        Block(Block.MUL, 3600, (6, 2), (6, 3), (6, 4), (7, 2), (7, 3)),
        Block(Block.ADD, 36, (6, 6), (6, 7), (7, 5), (7, 6), (8, 5), (8, 6), (9, 5)),
        Block(Block.ADD, 8, (6, 8), (7, 8)),
        Block(Block.SET, 7, (6, 9)),
        Block(Block.MUL, 24, (7, 1), (8, 1)),
        Block(Block.ADD, 13, (7, 4), (8, 4)),
        Block(Block.ADD, 7, (7, 7), (8, 7)),
        Block(Block.DIF, 6, (7, 9), (8, 9)),
        Block(Block.DIF, 5, (8, 0), (9, 0)),
        Block(Block.MUL, 45, (8, 2), (8, 3), (9, 3)),
        Block(Block.SET, 6, (8, 8)),
        Block(Block.ADD, 8, (9, 1), (9, 2)),
        Block(Block.SET, 4, (9, 4)),
        Block(Block.DIF, 1, (9, 6), (9, 7)),
        Block(Block.DIV, 3, (9, 8), (9, 9))
    ]

    matrix = make_matrix(model, n, *blocks)
    generate_contraints(model, matrix, *blocks)

    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for i in range(n):
            for j in range(n):
                g = solver.Value(matrix[i][j])
                g = 'A' if g == 10 else g
                print(g, end=' ')
            print()
    else:
        print("SIN SOLUCION")