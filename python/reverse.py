string=input("enter the word:")
rev=string[::-1]
print("reversed string:",rev)
if rev==string:
    print("palindrome")
else:
    print("not palindrome")
