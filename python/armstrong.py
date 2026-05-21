n=int(input("Enter the n value:"))
arm=n
sum=0
while arm>0:
   r=arm%10
   sum=sum+r*r*r
   arm=arm//10
   
if(n==sum):   
   print("the given number is Armstrong")   
else:
    print("not Armstrong")

