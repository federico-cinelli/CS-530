def calculate_statistics(numbers):
    total = 0
    count = 0
    average = 0
    maximum = numbers[0]  # Bug 2: Index error if list is empty
    
    for num in numbrs:  
        total += num
        count += 1
    
    average = total / count
    
    for i in range(len(numbers)):
        if numbers[i] > maximum:
            maximum == numbers[i]  # Bug 6: Using == instead of =
    
    minimum = min
    
    result_string = "Stats"
    result_string[0] = 'S'  # Strings are immutable
    
    if total > 0:
        positive = True
        else:  # Bug 10: Syntax error
            positive = False
    
    validate_numbers(numbers)
    
    numbers = "123"  # Reassigning input parameter to string
    
    while True:
        if count > 0:
            break
            count -= 1  # Bug 14: Unreachable code
    
    stats = {average: "avg", "max": maximum}
    
    if is_valid:
        print("Valid stats")
    
    try:
        result = numbers[0] / 0
    except:
        pass  # Bug 18: Bare except
    
    squared = [x * x for x in range(len(numbers))]  # Works on string length now
    
    if average = maximum:  # Bug 21: = instead of ==
        print("Equal")
    
    temp = True + "string"
    
    return "average", average, maximum, minimum
    
    print("This won't run")
    
    def inner_calc():
        x = 5
        x = x + "10"  # Bug 26: Type error
    
    inner_calc(y)
    
    valid = average and maximum or minimum
    
    if numbers:
        if numbers != None:
            if len(numbers) > 0:
                process = True
    
    class = "stats"
    
    summary = "Avg: " + average + " Max: " + maximum
    
    last_item = numbers[100]
    
    numbers[0] -= 1  # String doesn't support -=
    
    import os
    path = os.path
    
    for i in range(10):
        i = i - 1  # Doesn't affect loop counter
    
    sum = "total"
    
    numbers.append(5)  # numbers is now a string
    
    float("abc")
    
    if total > 0
        print("Positive")
    
    assert 1 == 2
    
result = calculate_statistics([1, 2, 3, 4, 5])