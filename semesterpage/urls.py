from django.conf.urls import include, url
from django.contrib import admin

from semesterpage import views

urlpatterns = [
    url(r'^$', views.homepage, name='semesterpage-homepage'),
    url(r'^www/$', views.homepage),

    # Overwrite the django admin login url in order to respect next parameters
    url(r'^oppdater/login/', views.admin_login),

    # Users with lacking permissions are redirected to the root url of the
    # admin backend. Redirect users to the homepage instead.
    url(r'^oppdater/$', views.homepage),

    # Overwrite history view, only allowing superusers to inspect and change
    # model object history
    url(r'^oppdater/semesterpage/course/(\d+)/history/$', views.admin_course_history, name='semesterpage-course-history'),

    # Admin page for contributors
    url(r'^oppdater/', include(admin.site.urls)),

    # For autocompletion of Courses in admin, with django-autocomplete-light
    url(r'^course-autocomplete/$', views.CourseAutocomplete.as_view(), name='semesterpage-course-autocomplete'),

    url(r'^accounts/profile/', views.profile, name='semesterpage-profile'),
    url(r'^kalender/(?P<calendar_name>[-\w]+)/$', views.calendar, name='semesterpage-calendar'),

    # View for updating a course homepage url from user input
    url(r'^ny_faghjemmeside/(?P<course_pk>\d+)/$', views.new_course_url, name='semesterpage-new_homepage_url'),

    # View for removing course from student page
    url(r'^fjern_fag/(?P<course_pk>\d+)/$', views.remove_course, name='semesterpage-remove_course'),

    # URL patterns for semester view
    url(r'^(?P<study_program>[-\w]+)/(?P<semester_number>[1-9]|10|11|12)/$', views.semester_view, name='semesterpage-semester'),
    url(r'^(?P<study_program>[-\w]+)/(?P<main_profile>[-\w]+)/(?P<semester_number>[1-9]|10|11|12)/$', views.semester_view, name='semesterpage-semester'),

    # URL for a specific main profile related to a study program
    url(r'^(?P<study_program>[-\w]+)/(?P<main_profile>[-\w]+)/$', views.semester_view, name='semesterpage-mainprofile'),

    # URL for a specific study program
    url(r'^(?P<study_program>[-\w]+)/$', views.semester_view, name='semesterpage-studyprogram'),
]
