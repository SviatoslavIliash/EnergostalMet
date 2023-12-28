from .models import Article


def articles_processor(request):
    articles = Article.objects.all()
    top_articles = []
    footer_articles = []

    for article in articles:
        if article.in_top_navbar:
            top_articles.append(article)
        if article.in_footer:
            footer_articles.append(article)

    return {"top_articles": top_articles, "footer_articles": footer_articles}
