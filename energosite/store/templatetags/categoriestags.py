from django import template
from django.utils.html import escape, mark_safe
from django.urls import reverse

register = template.Library()


def show_category_inline(category, last):
    output = []
    if category.children.all():
        output.append("<li class=\"dropdown\">")
        output.append(f"<a href=\"#\" class=\"dropdown-item dropdown-toggle\" data-bs-toggle=\"dropdown\" "
                      f"data-bs-auto-close=\"outside\" data-bs-offset=\"5,0\">"
                      f"{escape(category.name)}</a>")
        output.append(f"<ul class=\"dropdown-menu\">")
        for index, child in enumerate(category.children.all()):
            output += show_category_inline(child, index == len(category.children.all()) - 1)
        output.append("</ul>")
        output.append("</li>")

        # divider line
        if not last:
            output.append("<li><hr class=\"dropdown-divider\"/></li>")
    else:
        output.append(f"<li><a href=\"{escape(reverse('store:category_detail', args=[escape(category.name)]))}\" "
                      f"class=\"dropdown-item\">{escape(category.name)}</a></li>")
        # divider line
        if not last:
            output.append("<li><hr class=\"dropdown-divider\"/></li>")

    return output


@register.simple_tag # (takes_context=True)
def show_categories_tree(categories):
    output = ["<nav id=\"sidebarMenu\" class=\"collapse d-lg-block sidebar bg-white overflow-auto\">"]
    output.append("<div class=\"position-sticky\">")
    output.append("<div class=\"list-group list-group-flush mx-3 mt-4\">")
    for category in categories:
        if category.is_super_category():
            if category.children.all():
                output.append("<div class=\"dropdown-center list-group-item list-group-item-action py-2 ripple\" "
                              "aria-current=\"true\">")
                output.append(f"<a href=\"#\" class=\"btn dropdown-toggle\" data-bs-toggle=\"dropdown\" role=\"button\""
                              f"data-bs-auto-close=\"outside\" style=\"border:none\">"
                              f"{escape(category.name)}</a>")
                output.append(f"<ul class=\"dropdown-menu\">")

                for index, child in enumerate(category.children.all()):
                    output += show_category_inline(child, index == len(category.children.all()) - 1)

                output.append("</ul>")
                output.append("</div>")
            else:
                output.append(f"<a href=\"{escape(reverse('store:category_detail', args=[escape(category.name)]))}\" "
                              f"class=\"list-group-item list-group-item-action py-2 ripple\" "
                              f"aria-current=\"true\"><span>{escape(category.name)}</span></a>")

    output.append("</div>")
    output.append("</div>")
    output.append("</nav>")
    output = "".join(output)
    return mark_safe(output)
