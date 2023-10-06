from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from  django.http import Http404, HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from Reunion.forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .algorithms import *
from django.shortcuts import redirect


exitFlag = 0
@login_required
def all_meetings(request):
    if hasattr(request.user, 'employe_dirigeant_related'):
        a = request.user.employe_dirigeant_related.reunion_set.all()
        paginator = Paginator(a, 4)
        page = request.GET.get('page')
        try:
            meetings = paginator.page(page)
        except PageNotAnInteger:
            meetings = paginator.page(1)
        except EmptyPage:
            meetings = paginator.page(paginator.num_pages)

        context = {'meetings': meetings}
        return render(request, 'meetings/all_meetings.html', context)
    elif hasattr(request.user, 'employe_rapporteur_related'):
        a = request.user.employe_rapporteur_related.reunion_set.all().filter(soumise=True)
        paginator = Paginator(a, 4)
        page = request.GET.get('page')
        try:
            meetings = paginator.page(page)
        except PageNotAnInteger:
            meetings = paginator.page(1)
        except EmptyPage:
            meetings = paginator.page(paginator.num_pages)

        context = {'meetings': meetings}
        return render(request, 'meetings/all_meetings_rapporteur.html', context)
    elif hasattr(request.user, 'employe_collaborateur_related'):
        invitations = request.user.employe_collaborateur_related.collaborateur_invitations.all()
        meetings=[]
        for inv in invitations:
            if inv.meeting.soumise==True:
                meetings.append(inv.meeting)

        paginator = Paginator(meetings, 4)
        page = request.GET.get('page')
        try:
            meetings1 = paginator.page(page)
        except PageNotAnInteger:
            meetings1 = paginator.page(1)
        except EmptyPage:
            meetings1 = paginator.page(paginator.num_pages)

        context = {'meetings': meetings1}
        return render(request, 'meetings/all_meetings_rapporteur.html', context)

    return HttpResponse("You don't have access to this page")


@login_required
def add_meeting(request):
    form = MeetingForm()
    if hasattr(request.user, 'employe_dirigeant_related'):
        if request.method == "POST":
            form = MeetingForm(request.POST,)
            if form.is_valid():
                meeting = form.save(commit=False)
                meeting.date = form.cleaned_data['date']
                meeting.time = form.cleaned_data['time']
                meeting.place = form.cleaned_data['place']
                meeting.dirigeant=request.user.employe_dirigeant_related
                meeting.save()
                return HttpResponseRedirect('/meeting/all_meetings/')

        return render(request, "meetings/addMeeting.html", {
            "form": form,
        })
    else:
        raise PermissionDenied
@login_required
def detail_meeting(request,meeting_id):
    form = PointForm()
    meeting=get_object_or_404(Reunion, pk=meeting_id)
    points = meeting.points.all().order_by('ordre')
    invitations = meeting.meeting_invitations.all()

    if hasattr(request.user, 'employe_dirigeant_related') and meeting.dirigeant==request.user.employe_dirigeant_related:

        if not meeting.soumise:
            if request.method == "POST":
                form = PointForm(request.POST, )
                if form.is_valid():
                    point = form.save(commit=False)
                    point.reunion = meeting
                    point.save()
            try:
                collaborateurs = Collaborateur.objects.all()
                for inv in invitations:
                    collaborateurs=collaborateurs.exclude(id=inv.collaborateur_id)
                context = {'meeting': meeting,'all_invitations':invitations,'collaborateurs_not_invited':collaborateurs,'points':points,'form':form}

            except Reunion.DoesNotExist:
                raise Http404("Meeting does not exist!")
        else:
            context = {'meeting': meeting, 'all_invitations': invitations,'points': points,}
        return render(request, 'meetings/detail_meeting.html', context)

    elif request.user.isCollaborateur and meeting.meeting_invitations.all().filter(meeting=meeting,collaborateur=request.user.employe_collaborateur_related):
        context = {'meeting': meeting, 'all_invitations': invitations, 'points': points, }
        return render(request, 'meetings/detail_meeting_collaborateur.html', context)
    else:
        raise PermissionDenied


@login_required
def edit_meeting(request,meeting_id):
    meeting = get_object_or_404(Reunion, pk=meeting_id)
    if hasattr(request.user, 'employe_dirigeant_related') and meeting.soumise==False and meeting.dirigeant==request.user.employe_dirigeant_related:
        if request.method == "POST":
            form = MeetingForm(request.POST,instance=meeting)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/meeting/' + str(meeting_id) + '/')
        form = MeetingForm(instance=meeting)

        return render(request, "meetings/editMeeting.html", {
            "form": form,
        })
    else:
        raise PermissionDenied



@login_required
def delete_meeting(request,meeting_id):
    meeting = get_object_or_404(Reunion, pk=meeting_id)

    if hasattr(request.user, 'employe_dirigeant_related') and meeting.dirigeant==request.user.employe_dirigeant_related and not meeting.soumise:
                meeting.delete()
    return HttpResponseRedirect('/meeting/all_meetings/')
@login_required
def submit_meeting(request,meeting_id):
    meeting = get_object_or_404(Reunion, pk=meeting_id)

    if hasattr(request.user, 'employe_dirigeant_related') and meeting.dirigeant==request.user.employe_dirigeant_related:
                meeting.soumise=not meeting.soumise
                meeting.save()
    return HttpResponseRedirect('/meeting/' + str(meeting_id) + '/')



@login_required
def add_invitation(request,meeting_id,collaborateur_id):
    meeting = get_object_or_404(Reunion, pk=meeting_id)
    collaborateur=get_object_or_404(Collaborateur,pk=collaborateur_id)

    if hasattr(request.user, 'employe_dirigeant_related') and meeting.dirigeant==request.user.employe_dirigeant_related and  not meeting.soumise:
        inv=Invitation.objects.filter(collaborateur=collaborateur,meeting=meeting)
        if  not inv.exists():
            invitation = Invitation.objects.create(collaborateur=collaborateur, meeting=meeting, )
            invitation.save()

        return HttpResponseRedirect('/meeting/' + str(meeting_id) + '/')

@login_required
def all_invitations(request):
    if hasattr(request.user, 'employe_dirigeant_related'):
        meetings = request.user.employe_dirigeant_related.reunion_set.all().filter(soumise=True)
        invitations=[]
        for meeting in meetings:
            for invitation in meeting.meeting_invitations.all():
                invitations.append(invitation)
        paginator = Paginator(invitations, 8)
        page = request.GET.get('page')
        try:
            inv = paginator.page(page)
        except PageNotAnInteger:
            inv = paginator.page(1)
        except EmptyPage:
            inv = paginator.page(paginator.num_pages)

        context = {'invitations': inv}
        return render(request, 'meetings/all_invitations.html', context)
    return HttpResponse("You don't have access to this page")

@login_required
def detail_invitation(request,invitation_id):

    invitation=get_object_or_404(Invitation, pk=invitation_id)
    if hasattr(request.user, 'employe_dirigeant_related') and invitation.meeting.dirigeant==request.user.employe_dirigeant_related and invitation.meeting.soumise==True:
            context = {'invitation': invitation,}
            return render(request, 'meetings/detail_invitation.html', context)
    else:
        raise PermissionDenied




@login_required
def delete_invitation(request,invitation_id):
    invitation = get_object_or_404(Invitation, pk=invitation_id)
    if hasattr(request.user, 'employe_dirigeant_related')  and invitation.meeting.dirigeant==request.user.employe_dirigeant_related and  not invitation.meeting.soumise:
                invitation.delete()
    return HttpResponseRedirect('/meeting/'+str(invitation.meeting.id)+'/')
@login_required
def edit_point(request,point_id):
    point = get_object_or_404(Point, pk=point_id)

    if hasattr(request.user, 'employe_dirigeant_related')  and point.reunion.dirigeant==request.user.employe_dirigeant_related and  not point.reunion.soumise:
        if request.method == "POST":
            form = PointForm(request.POST,instance=point)
            if form.is_valid():

                form.save()
                return HttpResponseRedirect('/meeting/{0}/'.format(str(point.reunion.id)))
        form = PointForm(instance=point)

        return render(request, "points/editPoint.html", {
            "form": form,
        })
    elif request.user.isRapporteur  and point.reunion.rapporteur==request.user.employe_rapporteur_related :
            if point.reunion.hasPV and point.reunion.pv.soumis==True:
                return HttpResponseRedirect('/meeting/edit/{0}/'.format(str(point.reunion.id)))
            if request.method == "POST":
                form = EditPoint(request.POST,instance=point)
                if form.is_valid():
                    form.save()
                    if point.reunion.hasPV:
                        point.reunion.pv.delete()
                    pv = PV.objects.create(reunion=point.reunion)
                    html2pdf(point.reunion, point.reunion.meeting_invitations.all(), point.reunion.points.all())
                    pv.file.name = 'pv/meeting{0}.pdf'.format(point.reunion.id)
                    print (pv.file.path)
                    pv.save()
                    return HttpResponseRedirect('/meeting/edit/{0}/'.format(str(point.reunion.id)))

            form = EditPoint(instance=point)

            return render(request, "points/editPoint.html", {
                "form": form,
            })
    else:
        raise PermissionDenied

@login_required
def delete_point(request,point_id):
    point = get_object_or_404(Point, pk=point_id)
    if hasattr(request.user, 'employe_dirigeant_related')  and point.reunion.dirigeant==request.user.employe_dirigeant_related and  not point.reunion.soumise:
                point.delete()
    return HttpResponseRedirect('/meeting/'+str(point.reunion.id)+'/')

@login_required
def add_record_point(request,meeting_id,point_id):

    meeting = Reunion.objects.get(id=meeting_id)
    point = Point.objects.get(id=point_id,reunion=meeting )
    form = RecordForm()
    if hasattr(request.user, 'employe_rapporteur_related') and meeting.rapporteur==request.user.employe_rapporteur_related:
        if request.method == "POST":
                form = RecordForm(request.POST, request.FILES)
                if form.is_valid():
                    record = form.save(commit=False)
                    record.point=point
                    point.hasChanged=True
                    point.save()
                    record.save()
                return HttpResponseRedirect('/meeting/edit/' + str(meeting.id) + '/')
        return render(request, 'meetings/addRecord.html', {'form':form})

@login_required
def changeRecord(request,record_id):
    record = get_object_or_404(Enregistrement, pk=record_id)
    if request.user.isRapporteur  and record.point.reunion.rapporteur==request.user.employe_rapporteur_related:
        if request.method == "POST":
            form = RecordForm(request.POST,request.FILES,instance=record)
            if form.is_valid():
                changedRecord=form.save(commit=False)
                record.point.hasChanged=True
                record.point.save()
                changedRecord.save()
                return HttpResponseRedirect('/meeting/edit/' + str(record.point.reunion.id) + '/')
        form = RecordForm(instance=record,)

        return render(request, "meetings/changeRecord.html", {
            "form": form,
        })
    else:
        raise PermissionDenied



@login_required
def detail_meeting_rapporteur(request,meeting_id):
    meeting = Reunion.objects.get(id=meeting_id)
    if request.user.isRapporteur and meeting.rapporteur==request.user.employe_rapporteur_related:
        points = meeting.points.all().order_by('ordre')
        pointsHaveRecord=0
        createPV=False
        changed=False
        pointchanged=0
        for point in points:
            if point.hasRecord:
                pointsHaveRecord+=1
        if pointsHaveRecord==len(points):
            createPV=True
        for point in points:
            if point.hasChanged:
                pointchanged+=1
        if pointchanged:
            changed=True
        invitations = meeting.meeting_invitations.all()
        context = {'meeting': meeting, 'all_invitations': invitations,'points': points,'createPV':createPV,'changed':changed}
        return render(request, 'meetings/detail_meeting_rapporteur.html', context)
    else:
        return HttpResponse("The meeting that you search isn't associated to you")


@login_required
def create_pv(request,meeting_id):
    meeting = Reunion.objects.get(id=meeting_id)

    if request.user.isRapporteur and meeting.rapporteur == request.user.employe_rapporteur_related:
        points = meeting.points.all().filter(hasChanged=True).order_by('ordre')
        if(meeting.hasPV):
            meeting.pv.delete()
            meeting.save()
        n=len(points)
        print("nombre des points qui sont changes={0}".format(n))
        resumes=["" for p in range(0,n) ]
        texts = ["" for p in range(0, n)]
        threads=[]
        for p in range(0,n):
            enregistrement = Enregistrement.objects.get(point=points[p])
            thread=MonThread(enregistrement.audio_file.url,texts,resumes,p)
            thread.start()
            threads.append(thread)
        for p in range(0,n):
            threads[p].join()
        for p in range(0,n):
            points[p].resume=resumes[p]
            points[p].text = texts[p]
            points[p].hasChanged=False
            points[p].save()

        return HttpResponseRedirect('/meeting/edit/' + str(meeting_id) + '/')
    else:
        raise PermissionDenied

@login_required()
def pdfCreate(request,meeting_id):
    reunion = Reunion.objects.get(id=meeting_id)
    invitations = reunion.meeting_invitations.all()
    points = reunion.points.all().order_by('ordre')
    if reunion.hasPV:
        reunion.pv.delete()
    if request.user.isRapporteur and reunion.rapporteur == request.user.employe_rapporteur_related and not reunion.hasPV:
        pv=PV.objects.create(reunion=reunion)
        html2pdf(reunion,invitations,points)
        pv.file.name='pv/meeting{0}.pdf'.format(reunion.id)
        print (pv.file.path)
        pv.save()
    return HttpResponseRedirect('/meeting/edit/' + str(meeting_id) + '/')

@login_required
def submit_pv(request,meeting_id):
    pv = get_object_or_404(PV, pk=meeting_id)

    if request.user.isRapporteur and pv.reunion.rapporteur==request.user.employe_rapporteur_related:
                pv.soumis=not pv.soumis
                pv.save()
    return HttpResponseRedirect('/meeting/edit/' + str(meeting_id) + '/')

@login_required
def all_pv(request):
    if request.user.isDirigeant:
        all_pvs = PV.objects.all().filter(soumis=True)
        pvs=[]
        for a in all_pvs:
            if a.reunion.dirigeant==request.user.employe_dirigeant_related:
                pvs.append(a)

        paginator = Paginator(pvs, 4)
        page = request.GET.get('page')
        try:
            pvs1 = paginator.page(page)
        except PageNotAnInteger:
            pvs1 = paginator.page(1)
        except EmptyPage:
            pvs1 = paginator.page(paginator.num_pages)

        context = {'pvs': pvs1}
        return render(request, 'meetings/all_pv.html', context)
    elif request.user.isRapporteur:
        all_pvs = PV.objects.all()
        pvs = []
        for a in all_pvs:
            if a.reunion.rapporteur == request.user.employe_rapporteur_related:
                pvs.append(a)

        paginator = Paginator(pvs, 4)
        page = request.GET.get('page')
        try:
            pvs1 = paginator.page(page)
        except PageNotAnInteger:
            pvs1 = paginator.page(1)
        except EmptyPage:
            pvs1 = paginator.page(paginator.num_pages)

        context = {'pvs': pvs1}
        return render(request, 'meetings/all_pv.html', context)

    return HttpResponse("You don't have access to this page")

