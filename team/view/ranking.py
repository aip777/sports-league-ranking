from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

# Create your views here.
from team.forms import RankingForm
from django.db.models import Count, Max
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect

from team.document.error_log import ErrorLog
from team.models import TeamRanking
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from utils.ranking_generator import ranking_generator
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

class TeamRankingView(LoginRequiredMixin,ListView):
    model = TeamRanking
    login_url = '/'
    template_name = 'ranking/ranking-list.html'
    def get_queryset(self, *args, **kwargs):
        qs = super(TeamRankingView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-id")
        return qs


class TeamRankingUpdateView(LoginRequiredMixin, UpdateView):
    model = TeamRanking
    login_url = '/'
    template_name = 'ranking/update-ranking.html'
    fields = [
        "first_team",
        "first_team_score",
        "second_team",
        "second_team_score",
    ]
    success_url = "/ranking-list"

@login_required(login_url='/')
def addRankingView(request):
    if request.method == "POST":
        form = RankingForm(request.POST, request.FILES)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.created_by = request.user
            form_data.last_updated_by = request.user
            form_data.save()
            messages.success(request, "Successfully added")
            return redirect("/ranking-list")
        else:
            messages.error(request, form.errors)
            return HttpResponseRedirect("#")
    else:
        ranking = RankingForm()

    context = {
        "form": ranking,
    }
    return render(request, "ranking/add-ranking.html", context)


@login_required(login_url='/')
def rankinglistView(request):
    ranking = TeamRanking.objects.all()
    context = {
        "ranking": ranking,
    }
    return render(request, "ranking/ranking-list.html", context)


@login_required(login_url='/')
def updateRankingView(request, id):
    rank = get_object_or_404(TeamRanking, id=id)
    if request.method == "POST":
        form = RankingForm(request.POST, request.FILES, instance=rank)

        if form.is_valid():
            form.last_updated_by = request.user
            form.save()
            messages.success(request, "Successfully updated")
            return redirect("/ranking-list")
        else:
            messages.error(request, form.errors)
            return HttpResponseRedirect("#")
    else:
        form = RankingForm(instance=rank)
    context = {
        "form": form,
    }
    return render(request, "ranking/update-ranking.html", context)


@login_required(login_url='/')
def deleteRakingView(request, id):
    ranking = get_object_or_404(TeamRanking, id=id)
    ranking.delete()
    messages.success(request, "Successfully deleted")
    return redirect("/ranking-list")

@login_required(login_url='/')
def csv_upload(request):
    if "GET" == request.method:
        ranking =ranking_generator()
        context = {
            "csvdata": ranking,
        }
        return render(request, "csv/upload_csv.html", context)
    try:
        csv_file_district = request.FILES["csv_file_district"]
        if len(csv_file_district) == 0:
            messages.error(request, "Empty File")
            return render(request, "csv/upload_csv.html")

        if not csv_file_district.name.endswith(".csv"):
            messages.error(request, "File is not CSV type")
            return render(request, "csv/upload_csv.html")

        if csv_file_district.multiple_chunks():
            messages.error(
                request,
                "Uploaded file is too big (%.5f MB)."
                % (csv_file_district.size / (100000 * 100000),),
            )
            return render(request, "csv/upload_csv.html")

        file_data = csv_file_district.read().decode("utf-8")

        lines = file_data.split("\n")
        for index, line in enumerate(lines):
            fields = line.split(",")
            if index == 0:
                if (
                    (fields[0] == "team_one_name")
                    and (fields[1] == "team_one_score")
                    and (fields[2] == "team_two_name")
                    and (fields[3] == "team_two_score")
                ):
                    pass
                else:
                    messages.error(request, "File is not Correct Headers")
                    return render(request, "csv/upload_csv.html")
                    break
            else:
                if (
                    (len(fields[0]) != 0)
                    and (len(fields[1]) != 0)
                    and (len(fields[2]) != 0)
                    and (len(fields[3]) != 0)
                ):
                    TeamRanking.objects.create(
                        first_team=fields[0],first_team_score=int(fields[1]),second_team=fields[2],second_team_score=int(fields[3])
                    )
        messages.success(request, "Successfully Uploaded CSV File")
        return redirect("/")

    except Exception as exp:
        ErrorLog(message=exp)
        return redirect("/")
