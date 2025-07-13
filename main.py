import generator as g
import random
import itertools

# Parametry
number_of_permutations = 2000
k = 7
n = 300
population = 300
number_of_gen = 100

# Generowanie k-merów z mutacjami
spectrum = g.generator(n=n)
k_mers_used_spectrum = len(spectrum)

# Funkcja fitness
def fitnessiara(used, n, k):
    ratio = used / (n - k + 1)
    return 1 - ratio

# Liczenie nakładek
def james_nakładka(permutation, k):
    count = 1
    res = permutation[0]
    for s in permutation[1:]:
        o = max(i for i in range(len(s) + 1) if res.endswith(s[:i]))
        if o != 0:
            count += 1
            res += s[o:]
    return res, count

# Selekcja turniejowa
def tournament_selection(population, fitness_list):
    participants = random.sample(population, 6)
    scores = [fitness_list[population.index(p)] for p in participants]
    return participants[scores.index(max(scores))], max(scores)

# Krzyżowanie (crossing-over)
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return g.generate_k_mers(''.join(child1)), g.generate_k_mers(''.join(child2))

# Mutacja k-merów
def mutate_kmers(kmers, percentage):
    num = int(len(kmers) * (percentage / 100))
    selected = random.sample(kmers, num)
    mutated = []
    for kmer in selected:
        pos = random.randint(0, len(kmer) - 1)
        new_base = random.choice("ACTG")
        mutated.append(kmer[:pos] + new_base + kmer[pos + 1:])
    return list(set(mutated + [k for k in kmers if k not in selected]))

# Tworzenie początkowej populacji permutacji
overlaped_perm_list = []
overlaped_perm_count = []
first_gen_fitness = []
done_permutations = 0

for permutation in itertools.permutations(spectrum):
    res, count = james_nakładka(permutation, k)
    overlaped_perm_list.append(res)
    overlaped_perm_count.append(count)
    first_gen_fitness.append(fitnessiara(count, n, k))
    done_permutations += 1
    if done_permutations == number_of_permutations:
        break

print(f"Initial avg fitness: {sum(first_gen_fitness)/len(first_gen_fitness):.4f}")

# Ewolucja pokoleń
for gen in range(number_of_gen):
    fitness_list = [fitnessiara(c, n, k) for c in overlaped_perm_count]
    new_population = []
    new_population_score = []

    while len(new_population) < population:
        winner, score = tournament_selection(overlaped_perm_list, fitness_list)
        new_population.append(winner)
        new_population_score.append(score)

    offspring = []
    for _ in range(population // 2):
        r1 = random.randint(0, len(new_population) - 1)
        tmp1 = new_population.pop(r1)
        r2 = random.randint(0, len(new_population) - 1)
        tmp2 = new_population.pop(r2)
        ch1, ch2 = crossover(list(tmp1), list(tmp2))
        offspring.append(list(ch1))
        offspring.append(list(ch2))

    mutated_offspring = [mutate_kmers(of, 5) for of in offspring]

    mutated_offspring_overlapped = []
    mutated_offspring_count = []
    for seq in mutated_offspring:
        x, y = james_nakładka(seq, k)
        mutated_offspring_overlapped.append(x)
        mutated_offspring_count.append(y)

    fitness_scores = [fitnessiara(f, n, k) for f in mutated_offspring_count]
    print(f"Gen {gen+1} avg fitness: {sum(fitness_scores)/len(fitness_scores):.4f}")
