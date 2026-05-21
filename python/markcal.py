m1=float(input("Enter the mark m1:"))
m2=float(input("Enter the mark m2:"))
m3=float(input("Enter the mark m3:"))
m4=float(input("Enter the mark m4:"))
m5=float(input("Enter the mark m5:"))
print("The value of m1:",m1)
print("The value of m2:",m2)
print("The value of m3:",m3)
print("The value of m4:",m4)
print("The value of m5:",m5)
if(m1>=50 and m2>=50 and m3>=50 and m4>=50 and m5>=50):
   result="pass"
   sum=m1+m2+m3+m4+m5
   avg=sum/5
   print("sum:",sum)
   print("average:",avg)
   if avg>=95:
     grade="A+"
   elif avg>=75:
     grade="A"
   elif avg>=60:
     grade="B"
   else:
     grade="C"
else:
    result="fail"
    grade="no grade"
print(result)
print("Grade:",grade)
