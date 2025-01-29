import pandas as pd


def import_collection(users):
    data = []

    for user in users:
        user_id = user["_id"]
        for movie in user["movies"]:
            data.append(
                {
                    "user_id": user_id,
                    "movie_id": movie["movieid"],
                    "rating": movie["rating"],
                    "timestamp": movie["timestamp"],
                }
            )

    return pd.DataFrame(data)


def clean_whole_df(df):
    return df.loc[df.sum(axis=1) > 0]


def clean_test_df(train_df, test_df):
    movies_train = set(train_df["movie_id"])
    movies_test = set(test_df["movie_id"])
    movies_common = list(movies_train.intersection(movies_test))

    users_train = set(train_df["user_id"])
    users_test = set(test_df["user_id"])
    users_common = list(users_train.intersection(users_test))

    df_test_filtered_user = test_df[test_df["user_id"].isin(users_common)]
    df_test_filtered = df_test_filtered_user[
        df_test_filtered_user["movie_id"].isin(movies_common)
    ]

    return df_test_filtered


def filter_df(
    merged_df,
    movies_threshold=35,
    users_threshold=45,
    min_mean_rating=1.5,
    max_mean_rating=4.5,
    movies_few_notes=True,
    users_few_notes=True,
    users_no_discriminating=True,
    users_constant_dt=True,
):
    if movies_few_notes:
        # Compter le nombre de ratings par film
        movies_counts = merged_df["movie_id"].value_counts()

        # Supprimer les films ayant un nombre d'avis inférieur au seuil
        merged_df = merged_df[
            merged_df["movie_id"].isin(
                movies_counts[movies_counts > movies_threshold].index
            )
        ]

    if users_few_notes:
        # Compter le nombre de ratings par utilisateur
        users_counts = merged_df["user_id"].value_counts()
        print("Nombre de ratings par utilisateur :")
        print(users_counts.describe())
        print("\n")
        # Supprimer les utilisateurs ayant donné un nombre d'avis inférieur au seuil
        merged_df = merged_df[
            merged_df["user_id"].isin(
                users_counts[users_counts > users_threshold].index
            )
        ]

    if users_no_discriminating:
        # Filtrer les utilisateurs basés sur la note moyenne
        merged_df = merged_df.groupby("user_id").filter(
            lambda x: x["rating"].mean() > min_mean_rating
            and x["rating"].mean() < max_mean_rating
        )

    if users_constant_dt:
        # Éliminer les avis déposés au même moment par le même utilisateur
        merged_df = merged_df.drop_duplicates(
            subset=["user_id", "timestamp"], keep=False
        )

    return merged_df
