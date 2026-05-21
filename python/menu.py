print("Addition")
print("subtraction")
print("multiplication")
print("division")
print("modulo")
a=int(input("Enter the a value"))
b=int(input("Enter the b value"))
choice=input("Enter the choice")
if choice=="addition":
    print("add:",a+b)
elif choice=="subtraction":
    print("sub:",a-b)
elif choice=="multiplication":
    print("mul:",a*b)
elif choice=="division":
    print("div:",a/b)
elif choice=="modulo":
    print("mod:",a%b)
else:
    print("none")
