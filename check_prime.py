def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def are_coprime(a, b):
    return gcd(a, b) == 1

#Valeur de la clé obtenue après le hash de mon mots de passe
key = 209600814899375789563467296699744873855402989445855827328508865119759641574107585084370945819011968916466924203486273100218614816254591304919141699023403080951454350175019997136555796939565284755

#les deux nombre premiers que j'ai choisit pour former n = m x p trouvé sur https://fr.wikipedia.org/wiki/Plus_grand_nombre_premier_connu
m = 2**521 - 1
p = 2**127 - 1

# si key n'est pas premier avec m-1 et p-1 alors on ne peut pas calculer l'inverse modulaire

print("Key and prime_number_1 are coprime:", are_coprime(key, m-1))
print("Key and prime_number_2 are coprime:", are_coprime(key, p-1))

# dans le premier exemple la valeur de notre key est impaire , si cette dernière est paire elle est forcément non premiere avec les 2 
print("La valeur de key est impaire si celle si est pair elle ne peut pas être premiere avec m-1 et p-1")
print("Key-1 and prime_number_1 are coprime:", are_coprime(key-1, m-1))
print("Key-1 and prime_number_2 are coprime:", are_coprime(key-1, p-1))
