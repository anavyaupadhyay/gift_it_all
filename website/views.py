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


    # def get_context_data(self, **kwargs):
    #     context = super(self.__class__, self).get_context_data(**kwargs)
    #     if cache.get('banner_image_objects'):
    #         context['banner_image_objects']=cache.get('banner_image_objects')
    #     else:    
    #         context['banner_image_objects'] = BannerImages.objects.filter(is_active=True)
    #         cache.set('banner_image_objects',context['banner_image_objects'])
    #     if cache.get('featured_product'): 
    #         context['featured_product']=cache.get('featured_product')
    #     else:
    #         context['featured_product'] = Product.objects.filter(is_featured=True).filter(structure='parent')[:4] 
    #         cache.set('featured_product',context['featured_product'])
    #     if cache.get('dietitions_and_nutritionists'):
    #         context['dietitions_and_nutritionists']=cache.get('dietitions_and_nutritionists')
    #     else:        
    #         context['dietitions_and_nutritionists'] = DietitionsAndNutritionists.objects.filter(dietitions_and_nutritionists='Dietitions')
    #         cache.set('dietitions_and_nutritionists',context['dietitions_and_nutritionists'])
    #     return context

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
            return HttpResponseRedirect(reverse('website:product_category', kwargs={'slug': category}))

        if category_slug and not Category.objects.filter(slug=category_slug).exists() and Product.objects.filter(slug=category_slug).exists():
            prod_obj = Product.objects.filter(slug=category_slug).first()
            if prod_obj and prod_obj.structure == "child" and prod_obj.parent:
                return HttpResponseRedirect(reverse('website:product_detail', kwargs={'slug': prod_obj.parent.slug}))
            else:
                return HttpResponseRedirect(reverse('website:product_detail', kwargs={'slug': category_slug}))   

        if category_slug and not Category.objects.filter(slug=category_slug).exists():
            return HttpResponseRedirect(reverse('website:product_list'))    

        return super().dispatch(request, *args, **kwargs)
    

    