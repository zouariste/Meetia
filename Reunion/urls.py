from django.conf.urls import url

from Reunion import views

# SET THE NAMESPACE!
app_name = "Reunion"
urlpatterns = [
    url(r"^all_meetings/$", views.all_meetings, name="all_meetings"),
    url(r"^all_pvs/$", views.all_pv, name="all_pvs"),
    url(r"^(?P<meeting_id>[0-9]+)/$", views.detail_meeting, name="detail_meeting"),
    url(r"^add_meeting/$", views.add_meeting, name="add_meeting"),
    url(
        r"^edit_meeting/(?P<meeting_id>[0-9]+)/$",
        views.edit_meeting,
        name="edit_meeting",
    ),
    url(
        r"^delete_meeting/(?P<meeting_id>[0-9]+)/$",
        views.delete_meeting,
        name="delete_meeting",
    ),
    url(
        r"^submit_meeting/(?P<meeting_id>[0-9]+)/$",
        views.submit_meeting,
        name="submit_meeting",
    ),
    url(
        r"^add_invitation/(?P<meeting_id>[0-9]+)/(?P<collaborateur_id>[0-9]+)/$",
        views.add_invitation,
        name="add_invitation",
    ),
    url(r"^all_invitations/$", views.all_invitations, name="all_invitations"),
    url(
        r"^detail_invitation/(?P<invitation_id>[0-9]+)/$",
        views.detail_invitation,
        name="detail_invitation",
    ),
    url(
        r"^delete_invitation/(?P<invitation_id>[0-9]+)/$",
        views.delete_invitation,
        name="delete_invitation",
    ),
    url(
        r"^delete_point/(?P<point_id>[0-9]+)/$", views.delete_point, name="delete_point"
    ),
    url(r"^edit_point/(?P<point_id>[0-9]+)/$", views.edit_point, name="edit_point"),
    url(
        r"^edit/(?P<meeting_id>[0-9]+)/$",
        views.detail_meeting_rapporteur,
        name="detail_meeting_rapporteur",
    ),
    url(r"^createPV/(?P<meeting_id>[0-9]+)/$", views.create_pv, name="create_pv"),
    url(r"^createpdf/(?P<meeting_id>[0-9]+)/$", views.pdfCreate, name="create_pdf"),
    url(
        r"^addRecord/(?P<meeting_id>[0-9]+)/(?P<point_id>[0-9]+)/$",
        views.add_record_point,
        name="add_record_point",
    ),
    url(
        r"^changeRecord/(?P<record_id>[0-9]+)/$",
        views.changeRecord,
        name="changeRecord",
    ),
    url(r"^submit_pv/(?P<meeting_id>[0-9]+)/$", views.submit_pv, name="submit_pv"),
]
