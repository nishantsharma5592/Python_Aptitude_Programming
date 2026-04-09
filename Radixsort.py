# This is an implementation of radixsort algorithm. Radixsort algorithm
# uses as a backbone a stable sort algorithm. [We use counting sort.] It's 
# implementation poses a challenge in the internal representation 
# [of the input array] that needs to be created for digit-wise sorting and 
# keeping track of changes per iteration

import copy

# k is the maximum digit in digits list
def auxilliaryRadixSort(digit_list, k):
    # As stable sort we use counting sort
    auxiliary_list = [0]*(k+1)
    output_list  = [0]*len(digit_list)
    for i in range(len(digit_list)):
        auxiliary_list[digit_list[i]] = auxiliary_list[digit_list[i]]+1
    for i in range(1,k+1):
        auxiliary_list[i] = auxiliary_list[i] + auxiliary_list[i-1]
    for i in range(len(digit_list)):
        output_list[auxiliary_list[digit_list[i]]-1] = digit_list[i]
        auxiliary_list[digit_list[i]] = auxiliary_list[digit_list[i]]-1
    return output_list

# For simplicity, all elements in the list have the same number of digits
def radixSort(input_list):
    # We store the following information in the internal_input_list: 
    # [the number, the remaining number to be processed,the current digit 
    # being processed (-1 initially), the current position of the overall 
    # number (-1 if not recent)]
    internal_input_list = [[input_list[i], input_list[i], -1,  i] for i in\
            range(len(input_list))]
    while(True):
        digit_list = []
        # Separate the two halves: The remaining number to be processed and 
        # the current digit being processed 
        for i in range(len(internal_input_list)):
            ele = internal_input_list[i][1]
            rem = ele%10
            ele = int(ele/10)
            digit_list += [rem]
            internal_input_list[i][1] = ele
            internal_input_list[i][2] = rem
        
        # Here we obtain the radix sorted digit list
        radix_sorted_digit_list = auxilliaryRadixSort(digit_list, \
                max(digit_list))
        
        # To keep the relative order of elements same when the current digit
        # being processed is the same among elements; we maintain the internal 
        # input list from the previous iteration
        prev_internal_input_list = copy.deepcopy(internal_input_list)
        
        # Reset the position of the elements for update in the current 
        # iteration
        for i in range(len(internal_input_list)):
            internal_input_list[i][3] = -1
 
        for i in range(len(radix_sorted_digit_list)):
            # Collect all elements where the current digit being processed 
            # from the radix sorted digit list occurs (at index 2) 
            # [that have yet not been updated in the recent cycle]
            elements  = [internal_input_list[j] for j in \
                    range(len(internal_input_list)) if \
                    (internal_input_list[j][2] == radix_sorted_digit_list[i])\
                    and (internal_input_list[j][3] == -1)]
            
            # We keep the relative positions of the elements that are clashing 
            # (in the occurrence of same digits) same as it was in the previous 
            # iteration. [We are looking for the minimum position (among such 
            # elements) where an un-updated element occurs] 

            updateable_element = None
            min_position = 99999
            for element in elements:
                for prev_element in prev_internal_input_list:
                    if (element[0] == prev_element[0]) and \
                            (prev_element[3] < min_position):
                        min_position = prev_element[3]
                        updateable_element = element
                        
            # Update one element at a time
            for k in range(len(internal_input_list)):
                if (internal_input_list[k][0] == updateable_element[0]) \
                        and (internal_input_list[k][3] == -1):
                    internal_input_list[k][3] = i
                    break
        # Here we see the internal input list after one cycle:    
        print("Internal input list with updated position:")
        print(internal_input_list)
        
        # Break when all digits of d-digit numbers have been processed
        if (all([internal_input_list[i][1]==0 for i in \
                range(len(internal_input_list))])):
            break
    print("Final internal input_list: ")
    print(internal_input_list)
    
    # We just return the list of sorted numbers in the end
    sorted_list = [-1]*len(internal_input_list)
    for i in range(len(internal_input_list)):
        sorted_list[internal_input_list[i][3]] = internal_input_list[i][0]
    return sorted_list
    
if __name__ == "__main__":
    # Assuming that all elements are d-digit
    input_list = [329, 457, 657, 839, 436, 720, 355]
    # input_list = [4121, 7663, 8652, 1829, 6652, 4536, 1827, 9871]
    print("Input list: ")
    print(input_list)
    sorted_list = radixSort(input_list)
    print("Radix sorted input list:")
    print(sorted_list)

