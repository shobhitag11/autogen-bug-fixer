
def divide_numbers(a, b):
    """Divide two numbers"""
    result = a / b  # Bug: No check for division by zero
    return result

def calculate_average(numbers):
    """Calculate average of a list of numbers"""
    total = sum(numbers)
    count = len(numbers)  # Bug: No check for empty list
    return total / count

def find_maximum(numbers):
    """Find maximum number in list"""
    max_num = numbers[0]  # Bug: No check for empty list
    for num in numbers[1:]:
        if num > max_num:
            max_num = num
    return max_num

def fibonacci(n):
    """Generate fibonacci sequence"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

# Test the functions (this will cause errors)
if __name__ == "__main__":
    print("Testing divide_numbers:")
    print(divide_numbers(10, 2))
    print(divide_numbers(10, 0))  # This will cause ZeroDivisionError
    
    print("Testing calculate_average:")
    print(calculate_average([1, 2, 3, 4, 5]))
    print(calculate_average([]))  # This will cause ZeroDivisionError
    
    print("Testing find_maximum:")
    print(find_maximum([1, 5, 3, 9, 2]))
    print(find_maximum([]))  # This will cause IndexError
