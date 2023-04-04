def csv_upload(request):
    if "GET" == request.method:
        _list = TeamRanking.objects.all().order_by("-point")
        paginator = Paginator(_list, 10)
        page = request.GET.get("page")
        try:
            csvdata = paginator.page(page)
        except PageNotAnInteger:
            csvdata = paginator.page(1)
        except EmptyPage:
            csvdata = paginator.page(paginator.num_pages)
        return render(request, "csv/upload_csv.html", {"csvdata": csvdata})
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
                    first_team, created = Team.objects.get_or_create(
                        name__iexact=fields[0]
                    )

                    if first_team:
                        first_team.name = fields[0]
                        first_team.save()
                        TeamRanking.objects.create(
                            team__id=first_team.id
                        )
                        rank.team = first_team
                        rank.point += int(fields[1])
                        rank.rank += int(fields[1])
                        rank.save()

                    second_team, created = Team.objects.get_or_create(
                        name__iexact=fields[2]
                    )
                    if second_team:
                        second_team.name = fields[2]
                        second_team.save()
                        rank, created = TeamRanking.objects.get_or_create(
                            team__id=second_team.id
                        )
                        rank.team = second_team
                        rank.point += int(fields[3])
                        rank.rank += int(fields[3])
                        rank.save()
        messages.success(request, "Successfully Uploaded CSV File")
        return redirect("/upload/csvfile/")

    except Exception as exp:
        ErrorLog(message=exp)
        return redirect("/upload/csvfile/")