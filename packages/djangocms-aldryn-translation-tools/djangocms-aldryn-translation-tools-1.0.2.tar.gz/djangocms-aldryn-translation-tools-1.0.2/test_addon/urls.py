from django.urls import path, re_path

from .views import SimpleDetailView, SimpleListView, SimpleRootView, UntranslatedDetailView


app_name = 'simple'

urlpatterns = [
    path(r'empty-view', SimpleRootView.as_view(), name='simple-root'),
    path(r'simple/', SimpleListView.as_view(), name='simple-list'),

    # NOTE: We are allowing access by slug and pk here.
    re_path(r'^simple/(?P<pk>\d+)/$', SimpleDetailView.as_view(),
            name='simple-detail'),
    re_path(r'^simple/(?P<slug>\w[-\w]*)/$', SimpleDetailView.as_view(),
            name='simple-detail'),

    re_path(r'^untranslated/(?P<pk>\d+)/$', UntranslatedDetailView.as_view(),
            name='untranslated-detail'),
    re_path(r'^untranslated/(?P<slug>\w[-\w]*)/$', UntranslatedDetailView.as_view(),
            name='untranslated-detail'),
]
