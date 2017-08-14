from django.shortcuts import get_object_or_404

class ProductSlugMixin(object):
    model = None

    def get_object(self,*args,**kwargs):
        print(self.kwargs)
        slug = self.kwargs.get("slug")
        modelclass = self.model
        if slug is not None:
            try:
                obj = get_object_or_404(modelclass,slug=slug)
            except:
                obj = modelclass.objects.filter(slug=slug).orderby("title").first()
        else:
            obj = super(ProductSlugMixin,self).get_object(*args,**kwargs)
        return obj
