from Products.models import Category

def CategoryList(request):
    category = Category.objects.all()

    return {
        'category': category
    }