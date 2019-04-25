from django.db import models


class InvitationMeetingManager(models.Manager):
    def all(self):
        return self.meeting_invitations.all()
