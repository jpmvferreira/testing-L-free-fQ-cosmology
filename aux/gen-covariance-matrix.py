import numpy as np

def planck2013():
    sla = 0.18
    sR = 0.0094
    swb = 0.0003

    s = [sla, sR, swb]

    # data from Iker Leanizbarrutia PhD thesis
    Cnorm = [[1       , 0.5250  , -0.4235],
             [0.5250  , 1       , -0.6925],
             [-0.4235 , -0.6925 , 1      ]]

    C = [[np.nan , np.nan , np.nan],
         [np.nan , np.nan , np.nan],
         [np.nan , np.nan , np.nan]]

    for i in range(0, len(Cnorm)):
        for j in range(0, len(Cnorm[0])):
            C[i][j] = Cnorm[i][j]*s[i]*s[j]

    Cinv = np.linalg.inv(C)

    np.set_printoptions(suppress = True)
    print(Cinv)

    return

def planck2018():
    wb  = 0.022038
    swb = 0.00022

    As  = 2.0898 * 10**(-9)
    sAs = 0.034 * 10**(-9)

    ns  = 0.9641
    sns = 0.0058

    la  = 301.54
    sla = 0.1319

    R  = 1.7469
    sR = 0.0072

    # data from 2302.04807 which claims to use Planck 2018 TT+lowE
    Cnorm = [[1,0.1193,0.4926,-0.3014,-0.5546],
             [0.1193,1,0.0262,-0.0434,0.0240],
             [0.4926,0.0262,1,-0.3571,-0.7776],
             [-0.3014,-0.0434,-0.3571,1,0.4207],
             [-0.5546,0.0240,-0.7776,0.4207,1]]

    # remove As and ns
    Cnorm = [[1       , -0.3014 , -0.5546],
             [-0.3014 , 1       , 0.4207 ],
             [-0.5546 , 0.4207  , 1      ]]

    # exchange order
    # wb, la, R -> la, R, wb
    # 0, 1, 2 -> 1, 2, 0
    Cnorm2 = [[Cnorm[1][1] , Cnorm[1][2] , Cnorm[1][0]],
              [Cnorm[2][1] , Cnorm[2][2] , Cnorm[2][0]],
              [Cnorm[0][1] , Cnorm[0][2] , Cnorm[0][0]]]

    s = [sla, sR, swb]

    C = [[np.nan , np.nan , np.nan],
         [np.nan , np.nan , np.nan],
         [np.nan , np.nan , np.nan]]

    for i in range(0, len(Cnorm)):
        for j in range(0, len(Cnorm[0])):
            C[i][j] = Cnorm2[i][j]*s[i]*s[j]

    Cinv = np.linalg.inv(C)

    np.set_printoptions(suppress = True)
    print(Cinv)

    return

if __name__ == "__main__":
    # pick one!
    #planck2013()
    planck2018()
