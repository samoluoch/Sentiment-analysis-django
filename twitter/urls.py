from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$',  views.LineChartJSONView.as_view(), name='line_chart_json'),
    # url(r'^analyse/$', views.analyse, name='analyse'),
    url(r'^$', views.index, name='index'),
    url(r'^pdf/$', views.Pdf.as_view(), name='pdf'),
    # url(r"^(\d+)/$", Pdf.views.BerichtListView.as_view()),
    # url(r'^pdf(\d+)/$', views.Pdf, name='pdf')
    url(r'^analyse/$', views.analyse, name='analyse'),
    url(r'^query/$', views.query, name='home'),
    url(r'^signup/', views.register, name='signup'),
    url(r'^user/(?P<username>\w+)', views.profile, name='profile'),

]
