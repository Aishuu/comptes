#! /usr/bin/env python

import sys

if len(sys.argv) < 2:
    sys.stderr.write("Usage : %s filename\n" % sys.argv[0])
    sys.exit (1)

with open(sys.argv[1]) as f:
    names = []
    days = []
    cur_day = []
    l = 0
    for line in f:
        l += 1
        words = line.split()
        if len (words) == 0:
            continue
        if words[0][0] == "#":
            if len(names) <= 1: 
                sys.stderr.write ("You must specify at least two names...\n")
                sys.exit (1)
            break
        name = []
        for w in words:
            if w in name:
                continue
            name.append(w)
            for n in names:
                for nn in n:
                    if nn == w:
                        sys.stderr.write ("%s designates two different persons (%s and %s)...\n" % (w, name[0], n[0]))
                        sys.exit (1)
        names.append(name)

    for line in f:
        l += 1
        words = line.split()
        if len (words) == 0:
            continue
        if words[0][0] == "#":
            days.append(cur_day)
            cur_day = []
        else:
            found = False
            for i in range(len(names)):
                for nn in names[i]:
                    if words[0] == nn:
                        cur_day.append ((i, int(100*float(words[1]))))
                        found = True
                        break
                if found:
                    break

            if not found:
                sys.stderr.write ("Unknown participant %s on line %d\n" % (words[0], l))
                sys.exit (1)

    days.append(cur_day)

    tot = []
    print "+------------------------+"
    print "|  TOTAL                 |"
    for n in range(len(names)):
        tot.append ([n, 0])
        for d in days:
            for p in d:
                if p[0] == n:
                    tot[-1][1] += p[1]
        print  "+--------------+---------+"
        print ("| %12s | %3.2fE |" % (names[n][0], tot[-1][1]/100.))
    print  "+--------------+---------+"

    passed_d = 0
    future_d = 0
    for d in days:
        if len(d) > 0:
            passed_d += 1
        else:
            future_d += 1

    glob_tot = 0
    for t in tot:
        glob_tot += t[1]

    print
    print "Total              : %4.2fE" % (glob_tot/100.)
    print "Per day            : %4.2fE" % (glob_tot/passed_d/100.)
    print "Per day per person : %4.2fE" % (glob_tot/passed_d/len(names)/100.)
    if future_d > 0:
        print "Prevision          : %4.2fE" % ((glob_tot/passed_d * (passed_d+future_d))/100.)
    print
    print "To balance :"

    glob_tot /= len(names)

    tot = sorted (tot, lambda k1, k2: k1[1]-k2[1])
    while tot[0][1] != glob_tot:
        due = glob_tot - tot[0][1]
        for i in range (len(names)) [::-1]:
            d = min (due, tot[i][1] - glob_tot)
            due -= d
            tot[i][1] -= d
            print "%12s --- %3.2fE ---> %s" % (names[tot[0][0]][0], d/100., names[tot[i][0]][0])
            if due == 0:
                break
        tot[0][1] = glob_tot
        tot = sorted (tot, lambda k1, k2: k1[1]-k2[1])

