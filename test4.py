"""
   *
  ***
 *****
*******
*********
***********
*************
***************
*****************
a = 9
"""


def make_pyramid(n):
    a = 2*n-2
    for i in range(n):
        for j in range(a):
            print(end=" ")
        a = a-1
        for j in range(i+1):
            print("* ", end=" ")
        print("\r")


if __name__ == '__main__':
    make_pyramid(9)
