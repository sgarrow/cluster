import time
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

# Pretty Print bcl.
def printbcl( inbcl ):
    for ii,c in enumerate(inbcl):
        print('{:4d}: '.format(ii), end = '')
        for bp in c:
            print(bp, end='')
        print()
    print()
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

    bcl = []

    for currBp in bpl:

        pixBelongs2Clstrs = []

        # Find the clusters to which he belongs, max 2.
        for ii in range ( len( bcl ) ):
            if( iBelong( currBp, bcl[ ii ]  ) ):
                pixBelongs2Clstrs.append( ii )
                if len( pixBelongs2Clstrs ) == 2:
                    break

        # Insert this BP into a new Cluster.  
        if len( pixBelongs2Clstrs ) == 0:
            bcl.append( [ currBp ] )
            #myStr = 'pixel {} creates new cluster {}'
            #print(myStr.format( currBp, len(bcl)-1 ))

        # Add this pixel into a single existing cluster. 
        elif len( pixBelongs2Clstrs ) == 1:
            bcl[pixBelongs2Clstrs[ 0 ]].append( currBp )
            #myStr = 'pixel {} inserted into cluster {}'
            #print(myStr.format( currBp, pixBelongs2Clstrs[ 0 ] ))

        # Combine clusters, add pixel to combined, 
        # delete old clusters, add new cluster to bcl.
        elif len( pixBelongs2Clstrs ) == 2:

            set1 = set( bcl[ pixBelongs2Clstrs[ 0 ] ] ) # Combine.
            set2 = set( bcl[ pixBelongs2Clstrs[ 1 ] ] )
            set3 = set1.union( set2 )
            tmpLst  = list( set3 )

            tmpLst.append( currBp )                     # Append pixel.
            bcl.append( tmpLst )                        # Append cluster.

            del bcl[ pixBelongs2Clstrs[ 0 ] ]           # Delete.
            del bcl[ pixBelongs2Clstrs[ 1 ] - 1 ]

            #myStr = 'pixel {} caused a combine/append/delete action of  clusters {} and {}'
            #print(myStr.format( currBp, pixBelongs2Clstrs[ 0 ], pixBelongs2Clstrs[ 1 ] ))

        #print( 'bcl after handling pixel {} is:'.format(currBp))
        #printbcl(bcl)
        #x = input()

    return bcl

#############################################

if __name__ == '__main__':

    from bpm import *

    # Key to understanding this program is knowing the 'shape' of the data.
    # 
    # A Bad-Pixel-Map (bpm) is a 2D array of ints, like this:
    # 
    #           0  1  2  3   
    #       [ [ 0, 0, 0, 0  ],   # 0
    #         [ 0, 0, 0, 1  ],   # 1
    #         [ 0, 0, 0, 1  ],   # 2
    #         [ 0, 0, 0, 0  ], ] # 3
    # 
    # A Bad-Pixel-List (bpl) is a 1D array of Tuples, like this:
    #       [ (1, 3), (1, 4), (2, 3), (2, 4),
    #         (5, 5), (5, 6), (6, 5), (6, 6) ]
    # 
    # A Bad-Cluster-List (bcl) is a 2D array of Tuples, like this:
    # 
    #       [ [ (1, 3), (1, 4), (2, 3), (2, 4) ], 
    #         [ (5, 5), (5, 6), (6, 5), (6, 6)] ]

    for jj, currGbpm in enumerate(gBpm):

        startTime = time.process_time()
        mBpl = makeBplFromBpm( currGbpm )
        mBcl = makeBclFromBpl( mBpl )
    
        numClustersLenEq1 = sum(1 for c in mBcl if len(c) == 1)
        numClustersLenGt1 = sum(1 for c in mBcl if len(c)  > 1)

        if len(mBcl):  # Cover case where there are no bad pixels.
            maxClusterSize = max(len(c) for c in mBcl)
        else:
            maxClusterSize = 0
        endTime = time.process_time()
        elapsedTime = endTime - startTime
    
        hist = [0]*(maxClusterSize+1)
        for c in mBcl:
            hist[len(c)] += 1
    
        print()
            
        myStr1 = ( ' ' + '*' * 5 + ' SUMMARY TEST CASE: {:2d}.  EXECUTION TIME: {:7.3f} SECONDS. ' + 
                   '*' * 5).format(jj,elapsedTime)
        print(myStr1)

        print( ' * ')
        print( ' *         Total Number of Bad Pixels: {:4d} '.format( len(mBpl)         ))
        print( ' *       Number of Singleton Clusters: {:4d} '.format( numClustersLenEq1 ))
        print( ' *   Number of Non-Singleton Clusters: {:4d} '.format( numClustersLenGt1 ))
        print( ' *           Total Number of Clusters: {:4d} '.format( len(mBcl)         ))
        print( ' *               Largest Cluster Size: {:4d} '.format( maxClusterSize    ))
        print( ' * ')
        print( ' *   Histogram = \n *' )
    
        for ii in range(1,len(hist)):
            if hist[ii] > 0:
                print( ' * {:5d} Clusters contain {:4d} Pixels.'.format( hist[ii], ii ))
        print( ' * ')
    
        print( ' ' + '*' * 68 )

# 102 Clusters contain    1 Pixels
#  10 Clusters contain    2 Pixels
#   9 Clusters contain    3 Pixels
#   7 Clusters contain    4 Pixels
#   4 Clusters contain    5 Pixels
#   1 Clusters contain    6 Pixels
#   2 Clusters contain   10 Pixels
#   1 Clusters contain   13 Pixels
#   1 Clusters contain   15 Pixels
#   1 Clusters contain   17 Pixels
#   1 Clusters contain   23 Pixels
#   1 Clusters contain   25 Pixels
