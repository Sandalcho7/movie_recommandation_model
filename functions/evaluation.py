import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from sklearn.metrics import mean_squared_error, ndcg_score


def rate(
    predict_df,
    cleaned_df,
    opt_mse=True,
    opt_top_10=True,
    opt_bottom_10=True,
    opt_ndcg=True,
):
    """
    Create indicators on the Movielens DB.

    Inputs:
    - the prediction DF
    - the cleaned rating DF

    Options:
    - mse indicator : the Mean Squared Error
    - top_10 : compare top 10 movies form the prediction to the user ratings (5)
    - bottom_10 : compare worse 10 movies form the prediction to the user ratings (2)
    - ndcg : Compute Normalized Discounted Cumulative Gain.
    """
    compare_df = pd.merge(
        predict_df, cleaned_df, how="inner", on=["user_id", "movie_id"]
    )
    sorted_df = compare_df.sort_values(
        by=["user_id", "predict"], ascending=[True, False]
    ).groupby("user_id")

    db = []

    if opt_mse:
        mse = mean_squared_error(compare_df["rating"], compare_df["predict"])
        delta_mse = np.sqrt(mse)
        db.append((delta_mse, mse))

    if opt_top_10:
        average_top_rating = (sorted_df.head(10))["rating"].mean()
        diff_top_rating_5 = 5 - average_top_rating
        db.append(diff_top_rating_5)

    if opt_bottom_10:
        average_worse_rating = (sorted_df.tail(10))["rating"].mean()
        diff_worse_rating_2 = average_worse_rating - 2
        db.append(diff_worse_rating_2)

    if opt_ndcg:
        ndcg = ndcg_score([compare_df["rating"].values], [compare_df["predict"].values])
        db.append(ndcg)

    return db


def format_rate_results(rating_train, rating_test):
    """
    Formate les résultats des métriques d'évaluation dans un DataFrame pour une visualisation claire.

    Args:
    - rating_train (list): Résultats des métriques pour l'ensemble d'entraînement.
    - rating_test (list): Résultats des métriques pour l'ensemble de test.

    Returns:
    - pd.DataFrame: Tableau structuré des résultats.
    """
    metrics = ["RMSE", "MSE", "Top 10 Diff", "Bottom 10 Diff", "NDCG"]

    train_values = [
        rating_train[0][0],  # RMSE
        rating_train[0][1],  # MSE
        rating_train[1],  # Différence Top 10
        rating_train[2],  # Différence Bottom 10
        rating_train[3],  # NDCG
    ]

    test_values = [
        rating_test[0][0],  # RMSE
        rating_test[0][1],  # MSE
        rating_test[1],  # Différence Top 10
        rating_test[2],  # Différence Bottom 10
        rating_test[3],  # NDCG
    ]

    results_df = pd.DataFrame(
        {"Metric": metrics, "Train": train_values, "Test": test_values}
    )

    return results_df


def visualize_rate_results(results):
    """
    Crée un graphique à barres pour visualiser les résultats de la fonction rate().

    Args:
    results (list): Liste des résultats retournés par la fonction rate().

    Returns:
    None: Affiche le graphique.
    """
    metrics = ["RMSE", "MSE", "Top 10 Diff", "Bottom 10 Diff", "NDCG"]

    values = [
        results[0][0],  # RMSE (racine carrée de MSE)
        results[0][1],  # MSE
        results[1],  # Différence Top 10
        results[2],  # Différence Bottom 10
        results[3],  # NDCG
    ]

    fig, ax = plt.subplots(figsize=(12, 6))

    bars = ax.bar(
        metrics, values, color=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#ff99cc"]
    )

    ax.set_ylabel("Valeurs")
    ax.set_title("Métriques de performance du modèle de recommandation")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{height:.4f}",
            ha="center",
            va="bottom",
        )

    plt.tight_layout()

    plt.show()
