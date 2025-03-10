def binary_search(lst:list, key:int, sort_func):
    size = len(lst)
    lst = sort_func(lst)
    count = 0
    found = False
    low = 0
    hi = size-1
    while (low <= hi) and (not found):
        mid = round((low+hi)/2)
        if key == lst[mid]:
            found = True
            count += 1
        else:
            if key < lst[mid]:
                hi = mid - 1
                count += 1
            else:
                low = mid + 1
                count += 1               
    if found:
        index = mid
    else:
        index = -1
        
    return index

def selection_sort(unsorted_lst : list):
    unsorted_lst = unsorted_lst.copy()
    size = len(unsorted_lst)
    if size < 2:
        print("No element to sort")
    for i in range(0, size):
        lowindex = i
        for j in range(size-1, i, -1):
            if unsorted_lst[j]<unsorted_lst[lowindex]:
                lowindex = j
                
            if i != lowindex:
                unsorted_lst[i],unsorted_lst[j] = unsorted_lst[j],unsorted_lst[i]
                lowindex = i
    
    return unsorted_lst
        
def menu(lim_size = 10, sort_algo = sorted): 
    index = None
    input_lst = []
    while True:
        ans = input('Enter 1 : Add data\nEnter 2 : Search data\nEnter n : Exit\nEnter : ')
        if ans == 'n':
            break
        if ans in ['1', '2', 'n']: 
            match ans:
                case '1':
                    while True:
                        input_int = int(input("Enter number : "))
                        if input_int == 0 or len(input_lst) >= lim_size:
                            print('Exit add data')
                            break
                        input_lst.append(input_int)
                        print(input_lst)
                case '2':
                    while True:
                        key = int(input('Enter key : '))
                        index = binary_search(input_lst, key, sort_algo)
                        print(f"    Key index is {index}")
                        sub_ans = input('Continue? yes : y | no : n\n    Enter : ')
                        if sub_ans == 'n':
                            break
        else:
            print('please select valid choice')        
            
if __name__ == "__main__":
    menu(lim_size =10, sort_algo = selection_sort)
