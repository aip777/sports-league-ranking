from team.document.error_log import ErrorLog
from django.shortcuts import render


def error_log(request):
    log = ErrorLog.objects.all()
    context = {"log": log}
    for l in log:
        print(l.message)
    return render(
        request,
        "log/error-log.html",
        context,
    )
