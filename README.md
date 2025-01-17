## Projet GS15 : Un coffre-fort numérique simplifié

Le projet effectué en binome à l'UTT en automne 2024 par Lucas SAURON et Marielle CHARON, consiste à faire un coffre-fort numérique en Python. C'est un système sécurisé permettant de stocker et gérer des informations sensibles sous forme numérique. Il fonctionne comme un coffre-fort physique, mais protège des données, des documents, ou des fichiers numériques au lieu d'objets matériels. Ce type de solution est souvent utilisé pour des informations confidentielles telles que des mots de passe, des fichiers juridiques, des informations bancaires ou des contrats sensibles.

### Principales caractéristiques

Sécurisation des accès : Les utilisateurs accèdent au coffre-fort à l’aide de moyens d’authentification forts, tels que des mots de passe robustes, un couple de clés publique/privée, et l’authentification à deux facteurs (2FA).

Chiffrement des données : Les données stockées dans le coffre-fort numérique sont chiffrées pour garantir que seules les personnes autorisées puissent y accéder ou les lire.

Enrollement : Une personne doit se créer un compte en pratique cela reviendra à créer un répertoire et un couple de clés privée / publique. La clé publique sera le seul élément du coffre-fort qui ne sera pas chiffré.

Dérivation de la clé (KDF) : L’utilisateur ne rentre pas une clé publique directement, mais un mot de passe. Une fonction de dérivation de la clé est alors utilisée pour transformer ce mot de passe en une clé privée de grande taille, à l'aide d'un algorithme de hashage.

Authentification à double sens : Avant chaque utilisation du coffre-fort, l’utilisateur doit demander un certificat auprès du coffre-fort et le vérifier auprès de l’autorité de certification. Ensuite, l’utilisateur doit s'authentifier auprès du coffre-fort via une preuve de connaissance de la clé privée (ZPK : Zero-Knowledge-Proof).

Échange de clés : Une fois cette double authentification effectuée, le client et le serveur s’échangent une clé secrète de session en utilisant le protocole d’échange de clés de Diffie-Hellman.

Dépôt / consultation de fichiers : Les fichiers sont chiffrés avec la clé privée de l’utilisateur et stockés sur le serveur en utilisant l’algorithme de chiffrement asymétrique RSA. Les échanges entre client et serveur sont chiffrés avec une clé de session et chaque échange est authentifié avec un hashmac.

Visualisation : La visualisation des actions possibles se fait à l'aide d'une fenêtre "Windows" widget. Le chiffrement et toutes les opérations en arrière-plan sont visibles sur le terminal.

### Attention fonctionnement du projet

Le projet a été fait sous Pyhton 3.7.2 et sur VS Code

Deux librairies sont necessaires (en environnement local si on veut ) : 
PySide2
sympy
