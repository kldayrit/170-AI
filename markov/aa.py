def listsum(numlist, size):
    if size ==0:
        return 0
    if size ==1:
        return numlist[0]

    mid = size//2

    return listsum(numlist[0:mid], mid) + listsum(numlist[mid:], size-mid)

numbers = [3,5,4,1,7,2,9,8,0,6]
print(listsum(numbers,len(numbers)))