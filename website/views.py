from django.views.generic import (
    TemplateView,
    DetailView,
)

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
