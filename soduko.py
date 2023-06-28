import pprint        as pp
import printRoutines as pr
import initRoutines  as ir

#############################################################################

def flatten(x):
    y = []
    for el in x:
        try:
            for subEl in el:
                y.append(subEl)
        except:
            y.append(el)
    return y
#############################################################################

def genHistogram(inLst):
    hist = []
    for bin in range(min(inLst), max(inLst)+1):
        binHeight = len([1 for x in inLst if x==bin])
        if binHeight > 0:
            hist.append((bin, binHeight))
    return hist
#############################################################################

def findRowsColsInSquare(rIdx, cIdx):
    if rIdx % 3 == 0: rOffsets = [ 1, 2]
    if rIdx % 3 == 1: rOffsets = [-1, 1]
    if rIdx % 3 == 2: rOffsets = [-1,-2] 
    if cIdx % 3 == 0: cOffsets = [ 1, 2]
    if cIdx % 3 == 1: cOffsets = [-1, 1] 
    if cIdx % 3 == 2: cOffsets = [-1,-2] 
    rowsInSquare = [ rIdx+rOffsets[0], rIdx+rOffsets[1] ]
    colsInSquare = [ cIdx+cOffsets[0], cIdx+cOffsets[1] ]
    return rowsInSquare, colsInSquare
#############################################################################

def buildRowDupsLst(canidates):
    # Make a list containing info on naked pairs in each row.
    # e.g., if row 2 contains 2 naked pairs then rowDups could look like:
    # [ [], [], [[3,7],[5,9]], [], [], [], [], [], [] ]
    rowDups = []
    for rIdx,row in enumerate(canidates):
        dup1 = [ el for ii, el in enumerate(row) if el in row[:ii] ]
        dupNo0 = [ x for x in dup1 if x !=0 ]
        dupNo0Len2 = [x for x in dupNo0 if len(x)==2]
        rowDups.append(dupNo0Len2)

    # Now add the cols where the pairs exist.  Then it might look like this:
    # [ [], [],  [ [[3,7],[1,4]],[[5,9],[6,7] ],  [], [], [], [], [], [] ]
    # Read: In the canidates list, 
    # Row 2, cols 1 and 4 is [3,7] and Row 2, cols 6 and 7 is [5,9]
    for rIdx,currListOfDupPairs in enumerate(rowDups):
        if currListOfDupPairs != []:
            for idxOfCurrDupPair, currDupPair in enumerate(currListOfDupPairs):
                colsOfThisDupPair = \
                [col for col,el in enumerate(canidates[rIdx]) if el==currDupPair]
                rowDups[rIdx][idxOfCurrDupPair] = \
                [currDupPair,colsOfThisDupPair]
    return rowDups
#############################################################################

def pruneNakedPairs(canidates):

    print('\nFinding naked canidate pairs in rows.')

    # Make a list containing info on naked pairs in each row.
    rowDups = buildRowDupsLst(canidates)
    if rowDups == [[], [], [], [], [], [], [], [], []]:
        return(canidates)
    pr.printRowDupsLst(rowDups)

    # Print canidates before pruning wrt naked pairs.
    pr.prettyPrint3DArray(canidates)
    
    # Pruning wrt naked pairs.
    #print()
    numPruned = 0
    for rIdx,currListOfDupPairs in enumerate(rowDups):
        if currListOfDupPairs != []:
            for idxOfCurrDupPair,currDupPairAndCoord in enumerate(currListOfDupPairs):
                for ii in range(2):                           # 1st item is the pair, 2nd item is the cols its in.
                    print( '  Removing {} from all cols in row {} except for cols {} and {}'.
                        format(currDupPairAndCoord[0][ii], rIdx, currDupPairAndCoord[1][0],currDupPairAndCoord[1][1] ))
                    for jj in range(9):                       # Remove the value from all the cols except
                        if jj not in currDupPairAndCoord[1]:  # don't remove it from the cols where the dup itself lives.
                            try:                              # Can't remove it if it's not there.
                                canidates[rIdx][jj].remove(currDupPairAndCoord[0][ii])
                                numPruned += 1
                            except:
                                pass

    print('  numPruned = {}.\n'.format(numPruned))

    print('  Checking each pair to see if they are in the same square.' )
    for rIdx,currListOfDupPairs in enumerate(rowDups):
        if currListOfDupPairs != []:
            for idxOfCurrDupPair,currDupPairAndCoord in enumerate(currListOfDupPairs):
                for ii in range(2):                           # 1st item is the pair, 2nd item is the cols its in.
                    inSameSquare = ( currDupPairAndCoord[1][0]//3 == currDupPairAndCoord[1][1]//3 )
                    print( '  Pair {} is in cols {} of row {}. In same square = {}.'.\
                        format(currDupPairAndCoord[0], currDupPairAndCoord[1], rIdx, inSameSquare ) )

                    print( '  Removing {} from all cells in square containing cell {}. '.format(currDupPairAndCoord[0], currDupPairAndCoord[1] ) )
                    if inSameSquare:

                        for cIdx in currDupPairAndCoord[1]:

                            rowsInSquare, colsInSquare = findRowsColsInSquare(rIdx, cIdx)

                            for r in rowsInSquare:
                                for c in colsInSquare:
                                    for ii in range(9):
                                        if r != rIdx and c != cIdx:
                                            try:                              # Can't remove it if it's not there.
                                                canidates[r][c].remove(currDupPairAndCoord[0][ii])
                                                numPruned += 1
                                            except:
                                                pass

    print('  numPruned = {}.\n'.format(numPruned))
    # Print canidates after pruning wrt naked pairs.
    pr.prettyPrint3DArray(canidates)

    #exit()
    return(canidates)
#############################################################################

def updateCanidatesList(solution,canidates):
    #print('\nUpdating canidates list')
    Xpos = [ [ row[i] for row in solution] for i in range(len(solution[0]))]
    cols = [ x for x in Xpos ] 

    for rIdx,row in enumerate(solution):
        for cIdx,el in enumerate(row):
            prEn = False
            col = cols[cIdx]

            if el != 0:
                canidates[rIdx][cIdx] = 0
            else:
                for ii in [1,2,3,4,5,6,7,8,9]:

                    inRow = True
                    if row.count(ii) == 0: inRow = False

                    inCol = True
                    if col.count(ii) == 0: inCol = False

                    inSquare = False
                    rowsInSquare, colsInSquare = findRowsColsInSquare(rIdx, cIdx)

                    for ris in rowsInSquare:
                        for cis in colsInSquare:
                            if solution[ris][cis] == ii:
                                inSquare = True
                                break
                        if inSquare:
                            break

                    #print('   inRow={}, inCol={}, inSquare={}'.format(inRow, inCol, inSquare))
                    if( not inRow and not inCol and not inSquare):
                        #print('   Adding {} as canidate for {},{}'.format(ii,rIdx,cIdx))
                        if canidates[rIdx][cIdx] != 0: 
                            canidates[rIdx][cIdx].append(ii)
    return canidates
#############################################################################

def fillCellsVia_1_Canidate(solution, canidates):
    print('\nFilling solution cells that have only 1 item in canidate list.')
    numFilled = 0
    for rIdx,row in enumerate(solution):
        for cIdx,el in enumerate(row):
            if canidates[rIdx][cIdx] != 0 and len(canidates[rIdx][cIdx]) == 1:
                print('  Placing {} at {},{}'.\
                    format(canidates[rIdx][cIdx][0], rIdx,cIdx ))
                solution[rIdx][cIdx] = canidates[rIdx][cIdx][0]
                numFilled += 1
    print('  NumZeros = {}.'.format(sum(x.count(0) for x in solution) ))
    return numFilled,solution
#############################################################################

def fillCellsViaRowHistAnal(solution, canidates):
    print('\nFilling solution cells thru Row Hist Analysis.')
    numFilled = 0

    for r,row in enumerate(canidates):

        flatRow = flatten(row)
        histRow = genHistogram(flatRow)
        binsHeightOne = [ x[0] for x in histRow if x[1] == 1 and x[0] != 0]

        if len(binsHeightOne) > 0:
            valOfBinHeight1 = binsHeightOne[0]
            subListContainingThatVal = \
                [ x for x in row if x != 0 and valOfBinHeight1 in x]
            idxOfSubLst =  row.index(subListContainingThatVal[0])
            print('  Placing {} at {},{}'.format(valOfBinHeight1,r,idxOfSubLst))
            solution[r][idxOfSubLst] = valOfBinHeight1
            numFilled += 1
    print('  NumZeros = {}.'.format(sum(x.count(0) for x in solution) ))
    return numFilled,solution
#############################################################################

def fillCellsViaColHistAnal(solution, canidates):
    print('\nFilling solution cells thru Col Hist Analysis.')
    numFilled = 0
    Xpos = [[row[i] for row in canidates] for i in range(len(canidates[0]))]

    for c,col in enumerate(Xpos):

        flatCol = flatten(col)
        histCol = genHistogram(flatCol)
        binsHeightOne = [ x[0] for x in histCol if x[1] == 1 and x[0] != 0]

        if len(binsHeightOne) > 0:
            valOfBinHeight1 = binsHeightOne[0]
            subListContainingThatVal = \
                [ x for x in col if x != 0 and valOfBinHeight1 in x]
            idxOfSubLst =  col.index(subListContainingThatVal[0])
            print('  Placing {} at {},{}'.format(valOfBinHeight1,idxOfSubLst,c))
            solution[idxOfSubLst][c] = valOfBinHeight1
            numFilled += 1
    print('  NumZeros = {}.'.format(sum(x.count(0) for x in solution) ))
    return numFilled,solution
#############################################################################

def fillCellsViaSqrHistAnal(solution, canidates):
    print('\nFilling solution cells thru Square Hist Analysis')
    numFilled = 0
    squareNums = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]] 

    for squareNum in squareNums:
        rowsInSq = [ x+squareNum[0]*3 for x in [0,1,2] ]
        colsInSq = [ x+squareNum[1]*3 for x in [0,1,2] ]

        coordsInSq = [ [r,c] for r in rowsInSq for c in colsInSq ]
        canidatesSq = [ canidates[x[0]][x[1]] for x in coordsInSq ] 

        flatSq = flatten(canidatesSq)
        histSq = genHistogram(flatSq)
        binsHeightOne = [ x[0] for x in histSq if x[1] == 1 and x[0] != 0]

        if len(binsHeightOne) > 0:
            valOfBinHeight1 = binsHeightOne[0]
            subListContainingThatVal = \
                [ x for x in canidatesSq if x != 0 and valOfBinHeight1 in x]
            idxOfSubLst =  canidatesSq.index(subListContainingThatVal[0])
            r = rowsInSq[(idxOfSubLst // 3)]
            c = colsInSq[(idxOfSubLst %  3)]

            print('  Placing {} at {},{}'.format(valOfBinHeight1, r, c ))
            solution[r][c] = valOfBinHeight1
            numFilled += 1
    print('  NumZeros = {}.'.format(sum(x.count(0) for x in solution) ))
    return numFilled,solution
#############################################################################

def updatePuzzlesDictCntrs(puzzlesDict,k,  dicOfFuncs):
    puzzlesDict[k]['oC'] = dicOfFuncs['one']['calls'  ]
    puzzlesDict[k]['oR'] = dicOfFuncs['one']['replace'] 
    puzzlesDict[k]['rC'] = dicOfFuncs['row']['calls'  ] 
    puzzlesDict[k]['rR'] = dicOfFuncs['row']['replace'] 
    puzzlesDict[k]['cC'] = dicOfFuncs['col']['calls'  ] 
    puzzlesDict[k]['cR'] = dicOfFuncs['col']['replace'] 
    puzzlesDict[k]['sC'] = dicOfFuncs['sqr']['calls'  ] 
    puzzlesDict[k]['sR'] = dicOfFuncs['sqr']['replace'] 
    return puzzlesDict
#############################################################################

if __name__ == '__main__':
    from puzzles import puzzlesDict

    dicOfFuncs = {
        'one': { 'func': fillCellsVia_1_Canidate, 'calls': 0, 'replace': 0 },
        'row': { 'func': fillCellsViaRowHistAnal, 'calls': 0, 'replace': 0 },  
        'col': { 'func': fillCellsViaColHistAnal, 'calls': 0, 'replace': 0 },  
        'sqr': { 'func': fillCellsViaSqrHistAnal, 'calls': 0, 'replace': 0 }}

    for key in puzzlesDict:
        print(' Processing puzzle {}'.format(key))
        solution = [x[:] for x in puzzlesDict[key]['puzzle'] ]
        puzzlesDict[key]['start0s'] = sum(x.count(0) for x in solution)
        dicOfFuncs = ir.initDicOfFuncsCntrs(dicOfFuncs)
        while (1):
            numZerosBeforeAllFill = sum(x.count(0) for x in solution)
            for k in dicOfFuncs:
                if sum(x.count(0) for x in solution)==0: break
                numFilled = 1
                while (numFilled):
                    if sum(x.count(0) for x in solution)==0: break
                    canidates = ir.initCanidates()
                    canidates = updateCanidatesList(solution, canidates)
                    #canidates = pruneNakedPairs(canidates)
                    #canidates = pruneNakedPairs(canidates)
                    #canidates = pruneNakedPairs(canidates)
                    numFilled, solution = dicOfFuncs[k]['func']( solution, canidates )
                    dicOfFuncs[k]['calls']   += 1
                    dicOfFuncs[k]['replace'] += numFilled
                    if  numFilled == 0: break
                # end while loop on a single fill function
            # end for loop on all fill functions
            numZerosAfterAllFill = sum(x.count(0) for x in solution)
            if  numZerosAfterAllFill == numZerosBeforeAllFill or \
                numZerosAfterAllFill == 0: 
                break
            else: 
                numZerosBeforeAllFill = numZerosAfterAllFill
        # end while loop for this puzzle
        puzzlesDict[key]['end0s'] = numZerosAfterAllFill
        puzzlesDict = updatePuzzlesDictCntrs(puzzlesDict,key, dicOfFuncs)
        puzzlesDict[key]['solution'] = solution
        print('**********************************')
    # end for loop on all puzzles

    pr.printResults(puzzlesDict, 'all')
    pr.printResults(puzzlesDict, 'summary')
