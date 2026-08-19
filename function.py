def calc_fibonacci(n):
    if n==0 or n==1:
        return n
    else:
          return calc_fibonacci(n-1)+calc_fibonacci(n-2)

def calc_factorial(n):
     fact=1
     for i in range(1,n+1):
          fact*=i
     return fact

def add(n):
     sum=0
     for i in range(1,n+1):
          sum+=i
     return sum
