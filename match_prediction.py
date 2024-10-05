import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def compute_correlations_with_p1_wins(df):
    # Load the Excel file into a DataFrame

    # Exclude the 'id' column
    df = df.drop(columns=["id"])

    # Compute the correlation matrix with respect to 'p1_wins'
    correlation_matrix = df.corrwith(df["p1_wins"]).sort_values(ascending=False)
    return correlation_matrix


def generate_correlation_heatmap(excel_path):
    # Load the Excel file into a DataFrame
    df = pd.read_excel(excel_path)

    # Exclude the 'id' column
    df = df.drop(columns=["id"])

    # Compute the full correlation matrix
    full_correlations = df.corr().sort_values(by="p1_wins")

    # Plot the heatmap
    plt.figure(figsize=(20, 15))
    sns.heatmap(full_correlations, annot=True, cmap="YlGnBu")
    plt.title("Symmetric Correlation Matrix")
    # plt.show()


# Provide the path to your Excel file
excel_path = "final_updated_game_details.xlsx"
df = pd.read_excel(excel_path)
correlations = compute_correlations_with_p1_wins(df)
print(correlations)

generate_correlation_heatmap(excel_path=excel_path)

from sklearn.model_selection import train_test_split

df_selected = df.drop(columns=["id"])

X, y = df_selected.drop(["p1_wins"], axis=1), df_selected["p1_wins"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
print(len(X_train))

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.fit_transform(X_test)
knn = KNeighborsClassifier()
knn.fit(X_train_scaled, y_train)
print(knn.score(X_test_scaled, y_test))

from sklearn.model_selection import RandomizedSearchCV

param_grid = {"n_neighbors": list(range(5, 17, 2)), "weights": ["uniform", "distance"]}
knn_2 = KNeighborsClassifier(n_jobs=4)

clf = RandomizedSearchCV(knn_2, param_grid, n_jobs=4, n_iter=3, verbose=2, cv=3)
clf.fit(X_train_scaled, y_train)
knn_2 = clf.best_estimator_
print("best estimator: ", knn_2, " scored: ", knn_2.score(X_test_scaled, y_test))

from sklearn.ensemble import RandomForestClassifier

forest = RandomForestClassifier(n_jobs=4)
forest.fit(X_train_scaled, y_train)
print("forest score: ", forest.score(X_test_scaled, y_test))


from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Predict the test set results
y_pred = knn.predict(X_test_scaled)

# 2. Compute the confusion matrix
cm = confusion_matrix(y_test, y_pred)

# 3. Visualize the matrix using Seaborn
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.show()

y_pred_knn = knn_2.predict(X_test_scaled)
y_pred_forest = forest.predict(X_test_scaled)

# 2. Calcola le matrici di confusione per entrambi i modelli
cm_knn = confusion_matrix(y_test, y_pred_knn)
cm_forest = confusion_matrix(y_test, y_pred_forest)

plt.figure(figsize=(8, 6))
sns.heatmap(cm_knn, annot=True, fmt="d", cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix - Best KNN")
plt.show()

# Matrice di confusione per Random Forest
plt.figure(figsize=(8, 6))
sns.heatmap(cm_forest, annot=True, fmt="d", cmap="Greens")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix - Random Forest")
plt.show()


from tensorflow import keras

model = keras.models.Sequential()
model.add(keras.layers.Input(shape=(18,)))
model.add(keras.layers.Dense(200, activation="relu"))
model.add(keras.layers.Dense(100, activation="relu"))
model.add(keras.layers.Dense(100, activation="relu"))
model.add(keras.layers.Dense(1, activation="sigmoid"))

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
early_stopping_cb = keras.callbacks.EarlyStopping(
    patience=10
)  # stops at 5 epochs without improvement

X_train_scaled_train, X_valid, y_train_train, y_valid = train_test_split(
    X_train_scaled, y_train, test_size=0.15
)

model.fit(
    X_train_scaled_train,
    y_train_train,
    epochs=30,
    callbacks=[early_stopping_cb],
    validation_data=(X_valid, y_valid),
)

print(model.evaluate(X_test_scaled, y_test))
