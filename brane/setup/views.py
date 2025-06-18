from django.shortcuts import render

from setup.forms import CreateBraneDBForm


# Create your views here.

def index_handle(request):
    context = {}
    return render(request,"setup/index/main.html",context)

def create_pod_handle(request):
    create_form = CreateBraneDBForm()
    context = {
        "create_form": create_form,
    }
    return render(request,"setup/index/create_pod.html",context)


def create_pod_validate_handle(request):
    create_form = CreateBraneDBForm(request.POST)
    context = {
        "create_form": create_form,
    }
    if not create_form.is_valid():
        return render(request, "setup/index/create_pod_invalid.html", context)
    create_form.fields["cidr"].widget.attrs["readonly"] = "readonly"
    create_form.fields["pgpasswd"].widget.attrs["readonly"] = "readonly"
    create_form.fields["pgdata"].widget.attrs["readonly"] = "readonly"
    create_form.fields["ctrlport"].widget.attrs["readonly"] = "readonly"
    return render(request,"setup/index/create_pod_validate.html",context)


def create_pod_execute_handle(request):
    create_form = CreateBraneDBForm(request.POST)
    context = {
        "create_form": create_form,
    }
    if not create_form.is_valid():
        return render(request, "setup/index/create_pod_invalid.html", context)
    cidr = create_form.cleaned_data.get("cidr")
    ctrlport = create_form.cleaned_data.get("ctrlport")
    pgpasswd = create_form.cleaned_data.get("pgpasswd")
    pgdata = create_form.cleaned_data.get("pgdata")
    context = {
        "cidr": cidr,
        "pgpasswd": pgpasswd,
        "pgdata": pgdata,
        "ctrlport": ctrlport,
    }


    return render(request,"setup/index/create_pod_execute.html",context)