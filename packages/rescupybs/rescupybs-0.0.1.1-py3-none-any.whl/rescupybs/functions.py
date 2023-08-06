import numpy as np
from rescupy.totalenergy import TotalEnergy

def exchange(array_a,array_b):
    l=len(array_a)
    m=np.arange(l)
    for i in range(2,l):
        fun1=np.polyfit(m[i-2:i], array_a[i-2:i], 1)
        fun2=np.polyfit(m[i-2:i], array_b[i-2:i], 1)
        p1=np.poly1d(fun1)
        p2=np.poly1d(fun2)
        if abs(p1(m[i])-array_a[i]) > abs(p1(m[i])-array_b[i]) or abs(p2(m[i])-array_b[i]) > abs(p2(m[i])-array_a[i]):
            array_a[i], array_b[i]=array_b[i], array_a[i]

def bs_json_read(bs_file):
    calc = TotalEnergy.read(bs_file)
    chpts = calc.system.kpoint.special_points
    labels = calc.system.kpoint.get_special_points_labels()
    eigenvalues = calc.energy.eigenvalues.T - calc.energy.efermi
    ispin = calc.system.hamiltonian.ispin
    formula = calc.system.atoms.formula
    ns = calc.system.hamiltonian.get_spin_num()
    filename = bs_file.rsplit('.', 1)[0]
    for i in range(0, len(chpts)-1):
        if chpts[i] + 1 == chpts[i+1] and labels[i] == labels[i+1]:
            j = chpts[i]
            eigenvalues = np.delete(eigenvalues, j, axis=1)
            del chpts[i]
            del labels[i]
            for k in range(i, len(chpts)):
                chpts[k] = chpts[k] - 1
        if i + 2 >= len(chpts):
            break
    labels = [i.replace('G', 'Γ') for i in labels]
    if ispin == 2:
        np.savetxt(filename+'_bs_up.dat',eigenvalues[0])
        np.savetxt(filename+'_bs_down.dat',eigenvalues[1])
    else:
        np.savetxt(filename+'_bs.dat',eigenvalues[0])
    with open('LABELS', "w") as f:
        f.writelines([str(i)+' ' for i in chpts]+['\n'])
        f.writelines([i+' ' for i in labels]+['\n'])
        f.writelines(formula)
    return eigenvalues, chpts, labels

def bs_dat_read(input):
    data = []
    for i in input:
        data.append(np.loadtxt(i))
    return np.array(data)

def labels_read(LABELS):
    with open(LABELS, "r") as main_file:
        lines = main_file.readlines()
    chpts = [int(i) for i in lines[0].split()]
    labels = [i for i in lines[1].split()]
    return chpts, labels
