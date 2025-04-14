import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from app.models import Movie, Action
from sqlalchemy.orm import Session

def get_movie_recommendations(user_id: int, db: Session, top_n: int = 5):
    # Получаем все фильмы
    movies = db.query(Movie).all()
    movie_df = pd.DataFrame([{
        "id": m.id,
        "title": m.title,
        "tags": m.tags
    } for m in movies])

    if movie_df.empty:
        return []

    # Получаем лайкнутые фильмы пользователя
    liked_movie_ids = db.query(Action.movie_id).filter(
        Action.user_id == user_id,
        Action.action_type == "like"
    ).distinct().all()
    liked_movie_ids = [m[0] for m in liked_movie_ids]

    if not liked_movie_ids:
        return movie_df.head(top_n).to_dict(orient="records")

    # Content-based фильтрация по tags
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(movie_df["tags"].fillna(""))

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Индексы фильмов
    indices = pd.Series(movie_df.index, index=movie_df["id"]).drop_duplicates()

    # Считаем похожие фильмы
    sim_scores = {}
    for movie_id in liked_movie_ids:
        if movie_id in indices:
            idx = indices[movie_id]
            sim = list(enumerate(cosine_sim[idx]))
            for i, score in sim:
                sim_scores[i] = sim_scores.get(i, 0) + score

    # Сортируем по убыванию
    sim_scores = sorted(sim_scores.items(), key=lambda x: x[1], reverse=True)
    sim_scores = [i for i, score in sim_scores if movie_df.loc[i, "id"] not in liked_movie_ids]

    # Возвращаем топ-N рекомендаций
    recommended = movie_df.iloc[sim_scores[:top_n]]
    return recommended.to_dict(orient="records")
