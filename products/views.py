from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django .utils import timezone

def home(request):
    products=Product.objects
    return render(request,'products/home.html',{'product':products})
@login_required(login_url='/accounts/login')
def create(request):
    if request.method=='POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['image'] and request.FILES['icon']:
            p=Product()
            p.title=request.POST['title']
            p.body=request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                p.url=request.POST['url']
            else:
                p.url = 'http://'+ request.POST['url']
            p.image=request.FILES['image']
            p.icon=request.FILES['icon']
            p.pub_date=timezone.datetime.now()
            p.hunter=request.user
            p.save()
            return redirect('/products/' + str(p.id))


        else:
            return render(request, 'products/create.html',{'error':'All fields are mandatory'})

    else:
        return  render(request,'products/create.html')

def details(request,product_id):
    product=get_object_or_404(Product,pk=product_id)
    return render(request,'products/details.html',{'product':product})

@login_required(login_url='/accounts/signup')
def upvote(request,product_id):
    if request.method=='POST':
        product=get_object_or_404(Product,pk=product_id)
        product.votes_total+=1
        product.save()
        return redirect('details' ,str(product.id))
