snacks=["chips","sandwich","pizza","burger"]
price=[20,50,80,70]
cart=[]
bill=[]
while True:
    print("=============FOOD ITEMS=========")
    for i in range(len(snacks)):
        print(i+1, " " ,snacks[i],"-RS. ",price[i])
    choice=int(input("enter the choice of snacks item:"))
    if choice >=1 and choice <=len(snacks):
        cart.append(snacks[choice -1])
        bill.append(price[choice -1])
        print(snacks[choice -1],"Added to the cart successfully!")
    else:
        print("invalid choice")
        continue
    
    more=input("do u want to add more snacks? (yes/no)")
    if more.lower()!="yes":
        break
print("\n==========YOUR ORDERED SNACKS=========")
for i in range(len(cart)):
        
        print(cart[i],"-RS.",bill[i])
print("----------------------------")
print("Total snacks bought by u:",len(cart))
print("Total amount:",sum(bill))
print("--------------------------")
        
confirm=input("Confirm order? (yes/no):")
if confirm.lower()=="yes":
    print("Print order placed successfully")
    print("Enjoy your snacks")
else:
    print("ordered cancelled")
