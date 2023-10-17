from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
)

from oscar.core.loading import get_class, get_model

Product = get_model('catalogue', 'product')
Category = get_model('catalogue', 'category')

# Create your views here.

class HomePageView(TemplateView):
    """
    homepage view
    """
    template_name = 'website/homepage.html'

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['products']=Product.objects.all()
        return context      

class ProductListView(ListView):
    model = Product
    template_name = 'website/product_list.html'
    paginate_by = 20
    total_product = 0


    def dispatch(self, request, *args, **kwargs):
        category = self.request.GET.get('category', None)
        category_slug = self.kwargs.get('slug', None)
        # 302 redirection in case of incorect url enter
        if category and Category.objects.filter(slug=category, depth=1, is_active=True).exists():
            return HttpResponseRedirect(reverse('catalogue:product_category', kwargs={'slug': category}))

        if category_slug and not Category.objects.filter(slug=category_slug).exists() and Product.objects.filter(slug=category_slug).exists():
            prod_obj = Product.objects.filter(slug=category_slug).first()
            if prod_obj and prod_obj.structure == "child" and prod_obj.parent:
                return HttpResponseRedirect(reverse('website:product_detail', kwargs={'slug': prod_obj.parent.slug}))
            else:
                return HttpResponseRedirect(reverse('website:product_detail', kwargs={'slug': category_slug}))   

        if category_slug and not Category.objects.filter(slug=category_slug).exists():
            return HttpResponseRedirect(reverse('website:product_list'))    

        return super().dispatch(request, *args, **kwargs)
    
class ProductDetailView(TemplateView):
    """
    A view for display all the product in a website
    """
    template_name =  'website/product_detail.html'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'   
   
    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        context['product']=Product.objects.get(slug=self.kwargs['slug'])
        return context 
    
class LoginView(TemplateView):
     template_name =  'website/login.html'



class ContactView(TemplateView):
     template_name =  'website/contact_us.html'



class CartView(TemplateView):
     template_name =  'website/cart.html'
