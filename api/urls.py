from django.urls import path
from api.views import LogListView, LogDetailView, LogAnalysisRun


urlpatterns = [
    path('/loglist', LogListView.as_view()),
    path('/logdetail', LogDetailView.as_view()),
    path('/runtask', LogAnalysisRun.as_view())
]
