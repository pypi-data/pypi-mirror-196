def compoundinterest():
    intial=int(input("Enter the intial amount :"))
    percentage_1=int(input("Enter the percentage per year or trade :"))
    percentage=percentage_1/100
    trades=int(input("Enter the number of years or trade :"))
    profit=0
    for i in range(trades):
       profit=intial*percentage
       intial+=profit
    print("Total amount after ",trades,"years or trades : ",intial)

compoundinterest()