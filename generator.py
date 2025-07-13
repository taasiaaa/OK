import random

def generate_k_mers(seq, k=7):
    oligos = set()
    for i in range(len(seq) - k + 1):
        tmp_k_mer = seq[i:i + k]
        oligos.add(tmp_k_mer)
    return oligos

def james_błond(k_mers, number_mutations):
    type_m = [0, 1]  # 0 - negatywna mutacja, 1 - pozytywna
    k_mers = list(k_mers)  

    for _ in range(number_mutations):
        typ = random.choice(type_m)
        if typ == 0 and k_mers:  # mutacja negatywna (usuń losowy k-mer)
            k_mers.pop(random.randint(0, len(k_mers) - 1))
        elif typ == 1:  # mutacja pozytywna (dodaj losowy k-mer)
            while True:
                tmp_k_mer = ''.join(random.choices("AGTC", k=7))
                if tmp_k_mer not in k_mers:
                    k_mers.append(tmp_k_mer)
                    break
    return k_mers

def generator(n=200, k=7, mutations=5):
    seq = ''.join(random.choices("ACTG", k=n))
    k_mers = list(generate_k_mers(seq, k))
    number_of_mutations = round((mutations / 100) * len(seq))
    k_mers_after_mutation = james_błond(k_mers, number_of_mutations)
    return k_mers_after_mutation
