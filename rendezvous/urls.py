# Django
from django.conf.urls import patterns, include, url
from django.contrib import admin

# Project views
from rendezvous.views import home, about, scheme_search, user_search, test
from users.views import register_view, login_view, logout_view, profile_view_private, profile_view_public, update_profile, list_all, get_user, profile_view_ajax
from skills.views import get_skills, manage_skills, search_users_by_skills
from messaging.views import show_inbox, send_message, delete_message, reply, show_scheme_messaging, show_application, reply_application
from schemes.views import index, new_scheme, detail, detail_ajax, manage_schemes, delete, modify, add_user_to_scheme
from messaging.views import send_application
from geolocation.views import get_location

# Social Auth
import social_auth
from linkedin_integration.views import error, login_new, login_success

admin.autodiscover()
urlpatterns = patterns('',
	url(r'', include('social_auth.urls')),
    url(r'^$', home, name='home'),
	url(r'^about/$', about, name='about'),

	#User
	url(r'^user/update_profile/$', update_profile),
	url(r'^register/$', register_view),
	#url(r'^login/$', login_view, name='login_view'),
	url(r'^login(?P<next_page>.*)$', login_view, name='login_view'),
	url(r'^logout/$', logout_view, name='logout'),
	url(r'^user/profile/$', profile_view_private),
	url(r'^user/list_all/$', list_all),
	url(r'^user/get_user/$', get_user),
	url(r'^users/(?P<userprofile_username>\w+)/$', profile_view_public),
	url(r'^users/(?P<userprofile_id>\d+)/ajax/$', profile_view_ajax, name='profile_view_ajax'),
	url(r'^users/data/get_by_skills/$', search_users_by_skills),
	
	# Search
	url(r'search/schemes/$', scheme_search),
	url(r'search/users/$', user_search),

	# Skills
	url(r'^user/skills/manage/$', manage_skills),
	url(r'^skills/get_skills/$', get_skills),

	# Geolocation
	url(r'^geo/(?P<location_type>\w+)/$', get_location),	
	
	# Schemes
	url(r'^schemes/$', index, name='index'),
	url(r'^schemes/new/$', new_scheme, name='new'),
	url(r'^schemes/manage/$', manage_schemes, name='manage_schemes'),
	url(r'^schemes/(?P<scheme_id>\d+)/$', detail, name='detail'),
	url(r'^schemes/(?P<scheme_id>\d+)/ajax/$', detail_ajax, name='detail_ajax'),
	(r'^comments/', include('django.contrib.comments.urls')),
	url(r'^schemes/(?P<scheme_id>\d+)/delete/$', delete, name='delete'),
	url(r'^schemes/(?P<scheme_id>\d+)/modify/$', modify, name='modify'),
	url(r'^schemes/(?P<scheme_id>\d+)/applications/user=(?P<sender>\w+)_position=(?P<position>[\w|\W]+)_status=(?P<status>\w+)', add_user_to_scheme),
	url(r'^schemes/(?P<scheme_id>\d+)/join/$', send_application, name='send_application'),

	# Messaging
	url(r'^inbox/$', show_inbox),
	url(r'^inbox/schemes/$', show_scheme_messaging),
	url(r'^inbox/applications/(?P<application_id>\d+)/$', show_application),
	url(r'^inbox/applications/(?P<application_id>\d+)/reply/$', reply_application),
	url(r'^inbox/(?P<message_id>\d+)/delete/$', delete_message),
	url(r'^inbox/(?P<message_id>\d+)/reply/$', reply),
	url(r'^users/(?P<userprofile_username>\w+)/message/$', send_message),
	
	#Django Social Auth
	url(r'^error/$', error, name='error'),
	url(r'^linkedin/$', login_new, name='new_account'),
	url(r'^login/linkedin/$', login_success, name='linkedin_login_success'),

	# Test view
	url(r'^test/$', test, name='test'),

    # Admin
	url(r'^admin/', include(admin.site.urls)),
	
	# Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)