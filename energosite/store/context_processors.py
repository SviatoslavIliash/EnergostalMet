from .models import Article, Category, PhoneNumber


def articles_processor(request):
    articles = Article.objects.all()
    p_numbers = PhoneNumber.objects.all()
    top_articles = []
    footer_articles = []
    phone_numbers = []

    for p_number in p_numbers:
        phone_numbers.append(p_number.phone_number)

    for article in articles:
        if article.in_top_navbar:
            top_articles.append(article)
        if article.in_footer:
            footer_articles.append(article)

    return {"top_articles": top_articles, "footer_articles": footer_articles, "phone_numbers": phone_numbers}


def categories_processor(request):
    categories = Category.objects.all()
    return {"categories": categories}
