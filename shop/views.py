from django.shortcuts import render, get_object_or_404, redirect
from .models import Type, Product, ProductReview
from django.core.paginator import Paginator, EmptyPage, InvalidPage

# Create your views here.
def prod_list(request, type_id=None):
    type = None
    products = Product.objects.filter(available=True)
    if type_id:
        type = get_object_or_404(Type, id=type_id)
        products = Product.objects.filter(type=type, available=True)

        paginator = Paginator(products, 6)
        try:
            page = int(request.GET.get('page', '1'))
        except: 
            page = 1
        try:
            products = paginator.page(page)
        except (EmptyPage,InvalidPage):
            products = paginator.page(paginator.num_pages)

    return render(request, 'shop/type.html', {'type':type, 'prods':products})



def product_reviews(request, product_id):
    reviews = ProductReview.objects.filter(product_id=product_id).order_by('-date_added')
    return render(request, 'product_reviews.html', {'reviews': reviews})


def product_detail(request, type_id, product_id):
    product = get_object_or_404(Product, type_id=type_id, id=product_id)

    if request.method == 'POST':
        stars = request.POST.get('stars', 3)
        content = request.POST.get('content', '')

        review = ProductReview.objects.create(product=product, stars=stars, content=content)

    return render(request, 'shop/product.html', {'product':product})
