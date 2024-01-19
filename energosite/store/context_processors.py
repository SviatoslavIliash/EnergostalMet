from .models import Article, Category, PhoneNumber, CompanyInfo


def store_processor(request):
    result_context = {}
    result_context.update(collect_articles())
    result_context.update(collect_categories())
    result_context.update(collect_phone_numbers())
    result_context.update(collect_company())

    return result_context


def collect_articles():
    articles = Article.objects.all()
    top_articles = []
    footer_articles = []

    for article in articles:
        if article.in_top_navbar:
            top_articles.append(article)
        if article.in_footer:
            footer_articles.append(article)

    return {"top_articles": top_articles, "footer_articles": footer_articles}


def collect_phone_numbers():
    phone_numbers = PhoneNumber.objects.all()
    return {"phone_numbers": phone_numbers}


def collect_categories():
    categories = Category.objects.all()
    return {"categories": categories}


def collect_company():
    company = CompanyInfo.objects.first()
    return {"company": company}
