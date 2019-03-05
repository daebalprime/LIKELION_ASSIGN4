from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.post_list, name='post_list'),
    # url(r'^post/(?P<post_pk>\d+)/comment/create/$', views.comment_create, name='comment_create'),
    # url(r'^post/write', views.post_create, name='post_create'),
    # url(r'^post/(?P<post_pk>\d+)/$', views.post_detail, name='post_detail'),
    # url(r'^(?P<post_pk>\d+)/like-toggle/$', views.post_like_toggle, name='post_like_toggle'),
# legacy ends here
    url(r'^oe/list/$', views.oe_haters_list, name='oe_haters_list'),
    url(r'^oe/list/byp/(?P<provider_pk>\d+)/', views.oe_haters_list_byprovider, name='oe_haters_list_byprovider'),
    url(r'^oe/list/bys/$', views.oe_haters_list_byscore, name='oe_haters_list_byscore'),

    url(r'^oe/ranking/(?P<order>\w+)/(?P<page_num>\d+)$', views.oe_haters_ranking, name='oe_haters_ranking'),

    url(r'^oe/(?P<food_pk>\d+)/$', views.oe_haters_detail, name='oe_haters_detail'),
    url(r'^oe/(?P<food_pk>\d+)/hate-toggle/$', views.oe_haters_hate_toggle, name='oe_haters_hate_toggle'),
    url(r'^oe/(?P<food_pk>\d+)/like-toggle/$', views.oe_haters_like_toggle, name='oe_haters_like_toggle'),
    url(r'^oe/(?P<food_pk>\d+)/food/comment/create/$', views.oe_food_comment_create, name='oe_food_comment_create'),
]
