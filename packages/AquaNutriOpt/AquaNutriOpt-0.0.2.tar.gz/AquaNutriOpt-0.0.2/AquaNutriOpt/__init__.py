import numpy as np
import pulp
import os
BigM = 9999
class EPA:
    def __init__(self):
        print('**************************************************************')
        print('**************************************************************')
        print('**** EPA Package -- Version 01.0 *****************************')
        print('**************************************************************')
        print('**************************************************************')
        self.Um = {}
        self.C = np.Inf

    # %%
    def Solve_SO_Det_Model(self, Budget=np.Inf):

        if Budget == np.Inf:
            pass
        else:
            self.C = Budget
        #self.Solver = Solver
        print('**************************************************************')
        print('**************************************************************')
        print('Building the model ... ***************************************')
        print('**************************************************************')
        print('**************************************************************')
        # Modeling
        MODEL = pulp.LpProblem("Deterministic Model", pulp.LpMinimize)
        # Variabels

        Fijm = pulp.LpVariable.dicts('F', [(i, j, m) for m in self.MM for i in self.NN for j in self.NNp_i[i]],
                                     lowBound=0)
        for m in self.MM:
            for i in self.NN:
                for j in self.NNp_i[i]:
                    if i[-1] == 'a':
                        Fijm[(i, j, m)].lowBound = None

        Xit = pulp.LpVariable.dicts('X', {(i, t) for i in self.NN for t in self.TTi[i]}, lowBound=0, upBound=1,
                                    cat=pulp.LpInteger)
        Yijmt = pulp.LpVariable.dicts('Y',
                                      {(i, j, m, t) for j in self.NN for i in self.NNn_i[j] for m in self.MM for t in
                                       self.TTi[j]}, lowBound=0)

        # Objective
        MODEL += pulp.lpSum([Fijm[(i, self.L, self.ZZ[0])] for i in self.NNn_i[self.L]]), 'Obj'

        # Constraints
        ## Cons. 1
        for j in self.NN:
            if len(self.NNp_i[j]) > 1:
                continue
            for m in self.MM:
                if j != self.L:
                    MODEL += (pulp.lpSum([Fijm[(i, j, m)] for i in self.NNn_i[j]])
                              - pulp.lpSum([Fijm[(j, i, m)] for i in self.NNp_i[j]])
                              - pulp.lpSum([self.ALPHAtm[(t, m)] * Yijmt[(i, j, m, t)] for t in self.TTi[j] for i in
                                            self.NNn_i[j]])
                              - pulp.lpSum(
                                [self.Pim[(j, m)] * self.ALPHAtm[(t, m)] * Xit[(j, t)] for t in self.TTi[j]]) <= -
                              self.Pim[(j, m)]), 'C1_{}_{}'.format(j, m)
        for j in self.NN:
            if len(self.NNp_i[j]) > 1:
                continue
            for i in self.NNn_i[j]:
                for m in self.MM:
                    for t in self.TTi[j]:
                        MODEL += Yijmt[(i, j, m, t)] <= Fijm[(i, j, m)], 'LC1_{}_{}_{}_{}'.format(i, j, m, t)
                        MODEL += Yijmt[(i, j, m, t)] <= BigM * Xit[(j, t)], 'LC2_{}_{}_{}_{}'.format(i, j, m, t)
                        MODEL += Yijmt[(i, j, m, t)] >= Fijm[(i, j, m)] - BigM * (
                                    1 - Xit[(j, t)]), 'LC3_{}_{}_{}_{}'.format(i, j, m, t)

        # Cons. 2
        for i in self.NN:
            MODEL += pulp.lpSum([Xit[(i, t)] for t in self.TTi[i]]) <= 1, 'C2_{}'.format(i)

        # Cons. 3
        for m in self.ZZp:
            MODEL += pulp.lpSum([Fijm[(i, self.L, m)] for i in self.NNn_i[self.L]]) <= self.Um[m], 'C3_{}'.format(m)

        # Cons. 4
        MODEL += pulp.lpSum([self.Cit[(i, t)] * Xit[(i, t)] for i in self.NN for t in self.TTi[i]]) <= self.C, 'C4'

        # Cons. 5
        for j in self.NNs:
            for k in self.NNp_i[j]:
                for m in self.MM:
                    MODEL += Fijm[(j, k, m)] == self.BETAij[(j, k)] * pulp.lpSum(
                        Fijm[(i, j, m)] for i in self.NNn_i[j]), 'C5_{}_{}_{}'.format(j, k, m)

        if self.C == np.Inf:
            print('**WARNING**: No budget is set for cost!!')

        print('**************************************************************')
        print('**************************************************************')
        print('Solving the model ... ****************************************')
        print('**************************************************************')
        print('**************************************************************')

        #solver = pulp.get_solver(self.Solver)
        Sol = MODEL.solve()

        print('**************************************************************')
        print('**************************************************************')
        print('Generating the results ... ***********************************')
        print('**************************************************************')
        print('**************************************************************')

        file = open('Res_BMPs.txt', 'w+')
        Counter = 0
        for i in self.NN:
            for t in self.TTi[i]:
                try:
                    if Xit[(i, t)].value() > .5:
                        file.write(i)
                        file.write(',')
                        file.write(t)
                        file.write('\n')
                except:
                    Counter = Counter + 1
        file.close()

        file = open('Res_Flow.txt', 'w+')
        #
        for j in self.NN:
            for i in self.NNn_i[j]:
                try:
                    #            print('{} ==> {} : {}'.format(i, j, Fijm[(i,j,'P')].value() ) )
                    file.write('{}_{} {}\n'.format(i, j, str(Fijm[(i, j, 'P')].value())))
                except:
                    pass

        file.close()
        print('**************************************************************')
        print('**************************************************************')
        print('Solution is done. Find the results in the directory.**********')
        print('**************************************************************')
        print('**************************************************************')

    # %%
    def Read_Data(self, Network, BMP_Tech):

        # Network ---------------------------------------------------------------
        if not os.path.exists(Network):
            print('The network file does not exist. Make sure you have entered the right directory')
            return

        if Network[-3:].lower() != 'csv':
            print('The network file must be a .csv file. Suffix is not csv!!!')
            return

        NetFile = open(Network)

        l = NetFile.readline()
        l = l.split(',')
        self.MM = []
        print('The list of imported measures is: ', end='')
        for i in range(4, len(l) - 1):
            self.MM.append(l[i])
            print(l[i], ', ', end='')
        print()

        self.NN = []
        self.NNs = []
        self.NNp_i = {}
        self.NNn_i = {}
        self.Pim = {}
        self.BETAij = {}
        self.TTi = {}  # Set of all Technologies that can be implemented in loaction i
        while True:
            l = NetFile.readline()
            if l == '':
                break
            l = l.split(',')
            self.NN.append(l[0])
            if l[1] != '':
                self.NNn_i[l[0]] = l[1].split(' ')
            else:
                self.NNn_i[l[0]] = []
            if l[2] != '':
                self.NNp_i[l[0]] = l[2].split(' ')
            else:
                self.NNp_i[l[0]] = []

            if len(self.NNp_i[l[0]]) > 1:
                self.NNs.append(l[0])
                temp = l[3].split(' ')
                assert (len(temp) == len(self.NNp_i[l[0]]))
                for j in range(len(temp)):
                    self.BETAij[(l[0], self.NNp_i[l[0]][j])] = float(temp[j])

            self.Pim[(l[0], 'P')] = float(l[4])
            self.Pim[(l[0], 'N')] = float(l[5])

            if l[6] != '\n':
                l[6] = l[6].strip(' \n')
                l[6] = l[6].strip('\n')
                self.TTi[l[0]] = l[6].split(' ')
            else:
                self.TTi[l[0]] = []

        NetFile.close()

        # Cost and effectiveness ---------------------------------------------------
        if not os.path.exists(BMP_Tech):
            print('The BMP/Technology information file does not exist. Make sure you have entered the right directory')
            return

        if BMP_Tech[-3:].lower() != 'csv':
            print('The BMP_Tech file must be a .csv file. The suffix is not csv!!!')
            return

        TBFile = open(BMP_Tech)
        l = TBFile.readline()
        l = l.strip('\n')
        Header = l.split(',')
        CostInd = 0
        for i in range(1, len(Header)):
            if Header[i].lower() == 'cost':
                CostInd = i
                break
        if CostInd == 0:
            print("Header of file '{}' has no attribute Cost".format(BMP_Tech))
            print(Header)
            return

        self.ALPHAtm = {};
        self.Cit = {};
        self.ALPHA_HATtm = {};
        while True:
            l = TBFile.readline()
            if l == '':
                break
            temp = {}
            l = l.split(',')
            # effectiveness
            for i in range(1, len(l)):
                if i == CostInd:
                    for j in self.NN:
                        if l[0] in self.TTi[j]:
                            self.Cit[(j, l[0])] = float(l[i])
                else:
                    ind = Header[i].find('_')
                    temp[(Header[i][0:ind], Header[i][ind + 1:])] = float(l[i]) / 100
            for m in self.MM:
                self.ALPHAtm[(l[0], m)] = (temp[(m, 'UB')] + temp[(m, 'LB')]) / 2
                self.ALPHA_HATtm[(l[0], m)] = temp[(m, 'UB')] - self.ALPHAtm[(l[0], m)]

        print('--------------------------------------------------------------')
        print('The data was successfully imported ***************************')
        print('--------------------------------------------------------------')

    # %% Set the budgets
    def Set_Cost_Budget(self, C):
        if C < 0:
            print('WARNING: the budget of the cost is negative.')
        self.C = C
        print('--------------------------------------------------------------')
        print('The cost budget was successfully set to {} ****************'.format(C))
        print('--------------------------------------------------------------')

    # %% Set the upper limit of measures
    def Set_Measure_Budget(self, Measure, Value):
        if type(Measure) == list:
            if (len(Measure) != len(Value)):
                print("ERROR: The number of entered measures and values does not match!!!")
                return
            else:
                if np.any(np.array(Value) < 0):
                    print("ERROR: Budget values cannot be negative")
                    print(Value)
                    return
                i = 0
                for m in Measure:
                    if not m in self.MM:
                        print(self.MM)
                        return
                    self.Um[m] = Value[i]
                    i += 1
        else:
            if not Measure in self.MM:
                print("ERROR: Measure '{}' is not among the imported measures:".format(Measure))
                print(self.MM)
                return
            elif Value < 0:
                print("ERROR: Budget values cannot be negative")
                return
            else:
                self.Um[Measure] = Value

            # %% Set the target location

    def Set_TargetLocation(self, location):
        if not (location in self.NN):
            if (self.NN == []):
                print("No network has been imported yet. Plaase read the network data using 'Read_Data'")
                return
            else:
                print(
                    "The entered location '{}' does exit not in the imported network. Make sure you enter a string.".format(
                        location))
                return
        self.L = location

    # %% Set the single Objective
    def Set_Objective(self, Objective_Measure):
        if not (Objective_Measure in self.MM):
            if self.MM == []:
                print(
                    "The list of measure has been imported yet. Plaase read the network data using 'Read_Data' first.")
                return
            else:
                print(
                    "The entered measure '{}' does exit not in the list of measures. Make sure you enter a string.".format(
                        Objective_Measure))
                print(self.MM)
                return
        self.ZZ = [Objective_Measure]  # Set of Objectives

    # %% Set the limits of the bounded objectives
    def Set_BoundedMeasures(self, Measures, Bounds):
        if not (IsSubset(Measures, self.MM)):
            if self.MM == []:
                print(
                    "The list of measure has been imported yet. Plaase read the network data using 'Read_Data' first.")
                return
            else:
                print(
                    "At least one of the entered measures '{}' does not exit in the list of measures. Make sure you enter a string.".format(
                        Measures))
                print(self.MM)
                return
        self.ZZp = Measures  # Set of bounded measures
        self.Um = {}
        for i in range(len(self.ZZp)):
            self.Um[self.ZZp[i]] = Bounds[i]

        # %% Set the solver
        def Set_Solver(solver):
            if not solver in pulp.listSolvers(onlyAvailable=True):
                print('ERROR: solver {} is not available on your system!'.format(solver))
                return
            self.Solver = solver
            print('Solver is properly set to {}'.format(solver))


# %%
def IsSubset(X, Y):
    return len(np.setdiff1d(X, Y)) == 0