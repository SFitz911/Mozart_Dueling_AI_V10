#!/usr/bin/env python3
"""
Basic Mozart AI Review Example

This example demonstrates how to perform a simple code review
using Mozart AI V10 with basic configuration.
"""

import sys
import os

# Add the parent directory to the path to import mozart_monitorV10
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def basic_review_example():
    """
    Example of basic Mozart AI usage for code review.
    
    This would typically be done through the GUI, but this shows
    the underlying function calls.
    """
    
    # Example code to review
    code_to_review = '''
def calculate_fibonacci(n):
    if n <= 1:
        return n
    else:
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

# Usage
result = calculate_fibonacci(10)
print(f"Fibonacci of 10 is: {result}")
    '''
    
    goal = "Review this Fibonacci implementation for performance and correctness"
    context = "Python function that should efficiently calculate Fibonacci numbers"
    criteria = ["correctness", "performance", "clarity"]
    
    print("=== Mozart AI Basic Review Example ===")
    print(f"Goal: {goal}")
    print(f"Context: {context}")
    print(f"Selected Criteria: {', '.join(criteria)}")
    print(f"Code Length: {len(code_to_review)} characters")
    print("\nCode to Review:")
    print("-" * 40)
    print(code_to_review)
    print("-" * 40)
    
    print("\n📝 To run this review:")
    print("1. Start Mozart AI: python mozart_monitorV10.py")
    print("2. Paste the goal, context, and code above")
    print("3. Select 'correctness', 'performance', and 'clarity' criteria")
    print("4. Choose Fast Mode or Full Mode")
    print("5. Click 'Evaluate'")
    
    print("\n🎯 Expected Analysis Areas:")
    print("- Correctness: Recursive logic implementation")
    print("- Performance: Exponential time complexity issues")
    print("- Clarity: Function naming and documentation")

if __name__ == "__main__":
    basic_review_example()