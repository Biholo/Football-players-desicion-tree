import pandas as pd
from sklearn import tree
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import plot_tree
from sklearn.impute import SimpleImputer

# Load the dataset
data = pd.read_csv('final_data.csv')

# Drop specified columns not needed for the analysis
data = data.drop(columns=['days_injured', 'games_injured', 'yellow cards',
                          'second yellow cards', 'player', 'red cards',
                          'team', 'name', 'position'])

X = data.drop(columns=['current_value'])
y = data['current_value']

imputer = SimpleImputer(strategy="mean")
X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

# Binning 'current_value' into labeled ranges
value_bins = [0, 1e6, 1e7, 5e7, 1e8, max(y)]
value_labels = ['Low Value', 'Moderate Value', 'High Value', 'Very High Value', 'Top Value']
y_binned = pd.cut(y, bins=value_bins, labels=value_labels)

# Remove any NaN values in y_binned after binning
y_binned = y_binned.dropna()

# Match X to the indices of non-NaN values in y_binned
X = X.loc[y_binned.index]

X_train, X_test, y_train, y_test = train_test_split(X, y_binned, test_size=0.2, random_state=42)

clf = tree.DecisionTreeClassifier(max_depth=3, random_state=42)
clf.fit(X_train, y_train)

# Plot the decision tree with labeled classes
plt.figure(figsize=(20, 10))
plot_tree(clf, feature_names=X.columns, class_names=value_labels, filled=True, rounded=True)
plt.show()
