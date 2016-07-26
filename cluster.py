import pprint
# Make a Bad-Pixel-List from a Bad-Pixel-Map.
def makeBplFromBpm( bpm ):
    rows = len( bpm )
    cols = len( bpm[0] )
    bpl  = []
    for ii in range( rows ):
        for jj in range( cols ):
            if bpm[ii][jj]==0:
                bpl.append( (ii,jj) )
    return bpl
#############################################

# Determine if the passed in pix touches any pix in the passed in cluster.
def iBelong( currBp, currCL ):
    rtnVal = 0 # Assume it doesn't touch anybody till proven otherwise.
    for pixelInClust in currCL:
        delX = currBp[ 0 ] - pixelInClust[ 0 ]
        delY = currBp[ 1 ] - pixelInClust[ 1 ]
        if (abs(delX) < 2) and (abs(delY) < 2):
            rtnVal = 1
            break
    return rtnVal
#############################################

# Make a Bad-Cluster-List from a Bad-Pixel-List.
def makeBclFromBpl( bpl ):

    # Insert this bad pix into all clusters to which he belongs,
    bcl = []
    for currBp in bpl:
        pixelHandled = 0
        for currCluster in bcl:
            if( iBelong(currBp, currCluster)):
                currCluster.append( currBp )   # Add this BP into this Cluster. 
                pixelHandled += 1
                if pixelHandled == 2:          # Will never be part of more than 2 clusters.
                    break
        if not pixelHandled:
            bcl.append( [ currBp ] )           # Insert this BP into a NEW Cluster.

    # Build Cluster Dictionary.
    # { (1,2): [9,10]) } means pixel 1,2 is a member of clusters 9 and 10.
    pixelClustDict = {}
    for currBp in bpl:
        pixelClustDict[currBp] = []
        for ii in range(len(bcl)):
            if currBp in bcl[ii]:
                pixelClustDict[currBp].append(ii)

    # Build a list of clusters that need to be combined.
    clustersToCombine = [ pixelClustDict[myKey] for myKey in pixelClustDict if len(pixelClustDict[myKey]) > 1 ]

    # Elminate duplicates from clusters that need to be combined. 
    # { (1,2): [9,10]) } means pixel 1,2 is a member of clusters 9 and 10.
    # { (2,3): [9,10]) } means pixel 2,3 is a member of clusters 9 and 10.
    # Don't want to combine clusters 9 and 10 twice.
    clustersToCombineNoDups = []
    for i in clustersToCombine:
       if i not in clustersToCombineNoDups:
          clustersToCombineNoDups.append(i)

    # Sort (will make collapsing, below, easier).
    clustersToCombineNoDupsSorted = sorted(clustersToCombineNoDups, key=lambda x: x[0])
    pprint.pprint( clustersToCombineNoDupsSorted )

    # Collapse Bcl.
    c2cnds = clustersToCombineNoDupsSorted
    collapsedBcl   = []

    combineMaxIdx  = len( c2cnds ) - 1
    currCombineIdx = 0

    bclMaxIdx      = len( bcl ) - 1
    currBclIdx     = 0

    while currBclIdx < bclMaxIdx:
        if currBclIdx == c2cnds[currCombineIdx][0]:
            print('combining clusters', c2cnds[currCombineIdx] )
            currCombineIdx += 1 
            currBclIdx     += 2
        else:
            print('copying clusters {} '.format(currBclIdx))
            currBclIdx += 1



    #return collapsedBcl
    return bcl

# [[4, 5],
# [9, 10],
# [41, 42],
# [52, 56],
# [53, 57],
# [54, 56],
# [61, 62],
# [69, 70],
# [91, 92],
# [121, 123],
# [125, 126],
# [144, 146]]
#############################################

if __name__ == '__main__':

    from bpm import *

    # Key to understanding this program is knowing the 'shape' of the data.
    # 
    # A Bad-Pixel-Map (bpm) is a 2D array of ints, like this:
    # 
    #           0  1  2  3  4  5  6  7  
    #       [ [ 0, 0, 0, 0, 0, 0, 0, 0 ],  # 0
    #         [ 0, 0, 0, 1, 1, 0, 0, 0 ],  # 1
    #         [ 0, 0, 0, 1, 1, 0, 0, 0 ],  # 2
    #         [ 0, 0, 0, 0, 0, 0, 0, 0 ],  # 3
    #         [ 0, 0, 0, 0, 0, 0, 0, 0 ],  # 4
    #         [ 0, 0, 0, 0, 0, 1, 1, 0 ],  # 5
    #         [ 0, 0, 0, 0, 0, 1, 1, 0 ],  # 6
    #         [ 0, 0, 0, 0, 0, 0, 0, 0 ] ] # 7
    # 
    # A Bad-Pixel-List (bpl) is a 1D array of Tuples, like this:
    #       [ (1, 3), (1, 4), (2, 3), (2, 4),
    #         (5, 5), (5, 6), (6, 5), (6, 6) ]
    # 
    # A Bad-Cluster-List (bcl) is a 2D array of Tuples, like this:
    # 
    #       [ [ (1, 3), (1, 4), (2, 3), (2, 4) ], 
    #         [ (5, 5), (5, 6), (6, 5), (6, 6)] ]

    for currGbpm in gBpm:

        mBpl = makeBplFromBpm( currGbpm )
        mBcl = makeBclFromBpl( mBpl )
    
        numClustersLenEq1 = sum(1 for c in mBcl if len(c) == 1)
        numClustersLenGt1 = sum(1 for c in mBcl if len(c)  > 1)
        maxClusterSize = 0
        if len(mBcl):  # Cover case where there are no bad pixels.
            maxClusterSize    = max(len(c) for c in mBcl)
    
        hist = [0]*(maxClusterSize+1)
        for c in mBcl:
            hist[len(c)] += 1
    
        print()    
        print( ' ************* SUMMARY ********************************************')
        print( ' * ')
        print( ' * Total Number of Bad Pixels: {:4d}'.format(len(mBpl)))
        print( ' * ')
        print( ' *       Number of Singleton Clusters: {:4d} '.format( numClustersLenEq1 ))
        print( ' *   Number of Non-Singleton Clusters: {:4d} '.format( numClustersLenGt1 ))
        print( ' *           Total Number of Clusters: {:4d} '.format(len(mBcl)))
        print( ' * ')
        print( ' *               Largest Cluster Size: {:4d} '.format( maxClusterSize ))
        print( ' * ')
        print( ' ******************************************************************')
        print( ' ************* HISTOGRAM ******************************************')
    
        for ii in range(1,len(hist)):
            if hist[ii] > 0:
                print( ' * {:4d} Clusters contain {:4d} Pixels. *'.format( hist[ii], ii ))
    
        print( ' ******************************************************************')
    
        singletonCnt = 0
        for ii in range(len(mBcl)):
            if len(mBcl[ii])>0:
                pass
#                print( '   Cluster {:3} has {:3} pixels: {}'.format( ii, len(mBcl[ii]), mBcl[ii]) )