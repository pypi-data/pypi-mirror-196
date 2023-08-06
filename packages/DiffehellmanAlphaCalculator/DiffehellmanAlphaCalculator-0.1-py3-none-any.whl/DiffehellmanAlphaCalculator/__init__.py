def DiffehellmanAlphaCalculator(q):
    try:    
        while True:
            q = int(input("Enter a prime Number = "))
            l = []
            l1 = []
            n = 1
            for i in range(1, q):
                for z in range(1, q):
                    l1.append(z)            #colleting all values from 1 to q in l1
                for j in range(1, q):
                    s = i**j % q            #Formula for alpha genration
                    l.append(s)
                l.sort()
                # print(l,end='\n')
                if l == l1:
                    print(f"alpha = {i}")   #printing Alpha values using F-string
                    break
                l = []                      #empting both the list if l1 ! = l
                l1 = []
            print("\n")
    except Exception:
        DiffehellmanAlphaCalculatorexit()
