from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("", views.index,name="home"),
    path('about/',views.about,name="about"),
    path('service/',views.service,name="service"),
    path('service_details/',views.service_details,name="service_details"),
    path('faq/',views.faq,name="faq"),
    path('locations/',views.locations,name="locations"),
    path('shop/', views.shop, name='shop'),  # Show all products when no category is selected
    path('shop/<str:cat_name>/', views.shop, name='shop'),  # Show category-specific products
# <int:cat_id>/
    path('cart/',views.cart,name="cart"),
    path('wishlist/',views.wishlist,name="wishlist"),
    path('checkout/',views.checkout,name="checkout"),
    path('order_tracking/',views.order_tracking,name="order_tracking"),
    path('account/',views.account,name="account"),
    path('login/',views.login,name="login"),
   
    path('register/',views.register,name="register"),
    path('contact/',views.contact,name="contact"),
    path('blog/',views.blog,name="blog"),
    path('history/',views.history,name="history"),
    path('protfolio/',views.protfolio,name="portfolio"),
    path('login-register/',views.login_register,name="login-register"),
    path('blog-details/',views.blog_details,name="blog-details"),
    path('error/',views.error,name="error"),
    path('coming-soon/',views.coming_soon,name="coming-soon"),
    path('product-details/',views.product_details,name="product-details"),
    path('add-listing/',views.add_listing,name="add-listing"),
    path('portfolio-details/',views.protfolio_details,name="portfolio-details"),
   
    
   
    

    # path("contact/",views.contact,name="contactus"),
    # path("tracker/",views.tracker,name="tracker"),
    # path("search/",views.search,name="search"),
    # path("productview/",views.productview,name="productview"),
    # path("checkout/",views.checkout,name="checkout"),

]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)