from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('download',views.download_page,name="download_page"),
    path('download_pdf\<str:fname>',views.download,name="download_pdf"),
    path("editpage\<str:fname>",views.edit_page,name="edit_page"),
    path("save_edit",views.save_edit,name="save_edit"),
]