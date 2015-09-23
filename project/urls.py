from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

from tastypie.api import Api
from project.notifications.api import NotificationResource
v1_api = Api(api_name='v1')
v1_api.register(NotificationResource())


# rest_framework
from rest_framework import routers
from project.client.views import PurchasesViewSet, OrganizersViewSet, PopularPromoViewSet, NewPromoViewSet, HotPurchasesViewSet, CategoriesViewSet, SearchViewSet, ProductsViewSet, CatalogsViewSet, BenefitsViewSet, QuestionsViewSet, AnswersViewSet, UsersViewSet

router = routers.DefaultRouter()
router.register(r'api/v1/purchases', PurchasesViewSet)
router.register(r'api/v1/organizers', OrganizersViewSet)
router.register(r'api/v1/popular-promos', PopularPromoViewSet)
router.register(r'api/v1/new-promos', NewPromoViewSet)
router.register(r'api/v1/hot-purchases', HotPurchasesViewSet, base_name="hot-purchases")
router.register(r'api/v1/categories', CategoriesViewSet)
router.register(r'api/v1/search', SearchViewSet)
router.register(r'api/v1/products', ProductsViewSet)
router.register(r'api/v1/catalogs', CatalogsViewSet)
router.register(r'api/v1/benefits', BenefitsViewSet)
router.register(r'api/v1/questions', QuestionsViewSet)
router.register(r'api/v1/answers', AnswersViewSet)
router.register(r'api/v1/users', UsersViewSet)


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^forum/', include('pybb.urls', namespace='pybb')),
    url(r'^pristroy', include('project.pristroy.urls')),
    # url(r'^api/', include(v1_api.urls)),
    url(r'^notice/', include('project.notifications.urls')),
    url(r'^', include('project.core.urls')),
    url(r'^', include('project.cart.urls')),

    url(r'^', include('project.client.urls')),
    url(r'^api/v2/', include('project.client.api_v2_urls')),

    url(r'^', include('project.calendar_js.urls')),
    url(r'^', include('project.documentation.urls')),
    url(r'^profile/', include('project.accounts.urls')),

    # url(r'^api/', include('project.client.urls')),
    url(r'^', include(router.urls)),
    url(r'^rest-api/', include('rest_framework.urls', namespace='rest_framework'))
)


if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(
            r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}
        ),

        url(
            r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}
        ),
    )
