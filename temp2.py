m.addConstrs((B1[i] <= a_p[i]+b1_p[i]*dlist_test[n][i//8][i%8][1] for i in range(64)), 'c2')
    m.addConstrs((B2[i] <= a_p[i]+b2_p[i]*dlist_test[n][i//8][i%8][2] for i in range(64)), 'c3')
    m.addConstrs((B3[i] <= a_p[i]+b3_p[i]*dlist_test[n][i//8][i%8][3] for i in range(64)), 'c4')
    m.addConstrs((B4[i] <= a_p[i]+b4_p[i]*dlist_test[n][i//8][i%8][4] for i in range(64)), 'c5')
    m.addConstrs((B5[i] <= a_p[i]+b5_p[i]*dlist_test[n][i//8][i%8][5] for i in range(64)), 'c6')
    m.addConstrs((B0[i] >= a_p[i]+b0_p[i]*dlist_test[n][i//8][i%8][0]-1 for i in range(64)), 'c7')
    m.addConstrs((B1[i] >= a_p[i]+b1_p[i]*dlist_test[n][i//8][i%8][1]-1 for i in range(64)), 'c8')
    m.addConstrs((B2[i] >= a_p[i]+b2_p[i]*dlist_test[n][i//8][i%8][2]-1 for i in range(64)), 'c9')
    m.addConstrs((B3[i] >= a_p[i]+b3_p[i]*dlist_test[n][i//8][i%8][3]-1 for i in range(64)), 'c10')
    m.addConstrs((B4[i] >= a_p[i]+b4_p[i]*dlist_test[n][i//8][i%8][4]-1 for i in range(64)), 'c11')
    m.addConstrs((B5[i] >= a_p[i]+b5_p[i]*dlist_test[n][i//8][i%8][5]-1 for i in range(64)), 'c12')