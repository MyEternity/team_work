from articles.models import ArticleLike, CommentLike


def user_rating(user_id):
    rating_multiplier = 4
    articles_modifier = ArticleLike.get_like_rating(user_id).get('event_counter__sum', 0) * rating_multiplier
    comments_modifier = CommentLike.get_like_rating(user_id).get('event_counter__sum', 0)
    return articles_modifier + comments_modifier
