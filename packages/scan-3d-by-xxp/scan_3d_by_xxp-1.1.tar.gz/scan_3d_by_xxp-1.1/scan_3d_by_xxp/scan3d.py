import numpy as np
import time

def scan3d(arr):
    x_dim, y_dim, z_dim = arr.shape
    ans = []
    
    #collect all (x,y) whose z has at least one 1 
    xy_have_one = np.any(arr == 1, axis = 2)
    #xy_indices = np.argwhere(xy_have_one == 1)
    xy_indices = np.transpose( np.where(xy_have_one) )

    for x, y in xy_indices:
        z_data = arr[x, y, : ]
        #remove the layer along the z-axis where z=0
        #add 0 to the top of the array
        z_data1 = np.append( z_data[ 1 : ], 0 )
        z_xor = np.bitwise_xor( z_data, z_data1 )
        #np.nonzero takes time
        z_indices = np.nonzero( z_xor )[0]
        z_num = len(z_indices)
        if z_num % 2 == 0:
            for i in range( z_num//2 ):
                ans.append( [x, y] + [ z_indices[2 * i] + 1 ] + [ z_indices[ 2 * i + 1 ] ] )
        else:
            ans.append([x, y] + [0] + [ z_indices[0] ] )
            for i in range( z_num//2 ):
                ans.append( [x, y] + [ z_indices[2 * i + 1] + 1 ] + [ z_indices[ 2 * i + 2 ] ] )
    return ans

"""
def head(ans, n):
    for i in range(n):
        print(ans[i])

if __name__ == "__main__":
    arr = np.ones((1000, 1000, 1000), dtype = int)
    #record the time
    start_time = time.time()
    #compute time
    ans = scan3d(arr)
    end_time = time.time()
    #display some results
    print("First 20 results: ")
    head(ans, 20)
    print("Size of results is ", len(ans) )
    #compute the runing time
    print("Time elapsed when using the data of size", arr.shape, " is",  end_time - start_time, "seconds")

"""
