import matplotlib.pyplot as plt
import pandas as pd

# Créer un DataFrame pandas avec des valeurs d'exemple
data = {'Langage de programmation': ['Python', 'Java', 'C++', 'JavaScript', 'R'],
        'Part de marché': [32.7, 16.2, 6.9, 8.4, 3.3]}
df = pd.DataFrame(data)

# Définir les couleurs à utiliser pour chaque tranche du camembert
colors = ['#4CAF50', '#2196F3', '#FFC107', '#E91E63', '#9C27B0']

# Dessiner le graphique en camembert
plt.pie(df['Part de marché'], labels=df['Langage de programmation'], colors=colors, autopct='%1.1f%%')
plt.axis('equal')  # Ajuster les axes pour obtenir un cercle parfait
plt.title('Répartition des parts de marché des langages de programmation')  # Ajouter un titre

# Afficher le graphique
plt.show()