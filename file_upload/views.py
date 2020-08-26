from django.shortcuts import render, redirect, reverse
from .models import File, PoisonData
from .forms import FileUploadForm, FileUploadModelForm
import os
import uuid
from django.http import JsonResponse
from django.template.defaultfilters import filesizeformat
from django.conf import settings

# Create your views here.


# Show file list
def file_list(request):
    files = File.objects.all().order_by("-id")
    return render(request, 'file_upload/file_list.html', {'files': files})


def poison_data(request, *args, **kwargs):
    file_id = kwargs.get("pk")
    file_obj = File.objects.filter(id=file_id).first()
    poisonData = PoisonData.objects.filter(file=file_obj).order_by("-tick")
    return render(request, 'file_upload/poison.html', {'files': poisonData})


# Regular file upload without using ModelForm
def file_upload(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # get cleaned data
            upload_method = form.cleaned_data.get("wcl_link")
            raw_file = form.cleaned_data.get("file")
            new_file = File()
            new_file.file = handle_uploaded_file(raw_file)
            new_file.wcl_link = upload_method
            new_file.absolute_file = raw_file
            new_file.save()
            return redirect("/file/")
    else:
        form = FileUploadForm()

    return render(request, 'file_upload/upload_form.html', {'form': form,
                                                            'heading': 'Upload files with Regular Form'})


def handle_uploaded_file(file):
    ext = file.name.split('.')[-1]
    file_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # file path relative to 'media' folder
    file_path = os.path.join('files', file_name)
    absolute_file_path = os.path.join('media', 'files', file_name)

    directory = os.path.dirname(absolute_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(absolute_file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return file_path


# Upload File with ModelForm
def model_form_upload(request):
    if request.method == "POST":
        form = FileUploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/file/")
    else:
        form = FileUploadModelForm()

    return render(request, 'file_upload/upload_form.html', {'form': form,
                                                            'heading': 'Upload files with ModelForm'})


# Upload File with ModelForm
def ajax_form_upload(request):
    form = FileUploadModelForm()
    return render(request, 'file_upload/ajax_upload_form.html', {'form': form,
                                                            'heading': 'File Upload with AJAX'})


# handling AJAX requests
def ajax_upload(request):
    if request.method == "POST":
        # 1. Regular save method
        # upload_method = request.POST.get("upload_method")
        # raw_file = request.FILES.get("file")
        # new_file = File()
        # new_file.file = handle_uploaded_file(raw_file)
        # new_file.upload_method = upload_method
        # new_file.save()

        # 2. Use ModelForm als ok.
        form = FileUploadModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            # Obtain the latest file list
            files = File.objects.all().order_by('-id')
            data = []
            for file in files:
                data.append({
                    "url": file.file.url,
                    "size": filesizeformat(file.file.size),
                    "upload_method": file.upload_method,
                    })
            return JsonResponse(data, safe=False)
        else:
            data = {'error_msg': "Only jpg, pdf and xlsx files are allowed."}
            return JsonResponse(data)
    return JsonResponse({'error_msg': 'only POST method accpeted.'})


# handle viscidus poison
def parse_viscidus_poison(file_id):
    file_obj = File.objects.filter(id=file_id).first()
    if not file_obj:
        return False

    if file_obj.parse_flag:
        return True

    file_path = '%s/%s' % (settings.MEDIA_ROOT, file_obj.file.name)
    f = open(file_path, mode='r+', encoding='utf-8')
    f.readline()
    line = f.readline()

    while line:
        print(line)
        data = line.split(',')
        username = data[0][1:-1]
        amount = int(data[1][1:-1].split('$')[0])
        hit_tick = data[3][1:-1]
        if data[2][1:-1] == '0' or data[2][1:-1] == "" or data[2][1:-1] is None:
            hit = 0
            tick = 0
        else:
            if '(' in hit_tick or ')' in hit_tick:
                hit = int(hit_tick.split('   ')[0])
                tick = int(hit_tick.split('   ')[1][1:-1])
            else:
                hit = int(hit_tick)
                tick = 0
        uptime = float(data[5][1:-1][:-1])
        poisonData = PoisonData()
        poisonData.file = file_obj
        poisonData.username = username
        poisonData.amount = amount
        poisonData.hit = hit
        poisonData.tick = tick
        poisonData.uptime = uptime
        poisonData.save()
        line = f.readline()

    f.close()
    # print(json.dumps(result_dict))

    file_obj.parse_flag = True
    file_obj.save()
    return True


def parse(request, *args, **kwargs):
    file_id = kwargs.get('pk')
    print(file_id)
    parse_viscidus_poison(file_id=file_id)
    # return reverse('poison', kwargs={'pk': file_id})
    file_id = kwargs.get("pk")
    file_obj = File.objects.filter(id=file_id).first()
    poisonDatas = PoisonData.objects.filter(file=file_obj).order_by("-tick")
    print(poisonDatas)
    return render(request, 'file_upload/poison.html', {'poisonDatas': poisonDatas})
    # return redirect('/file/')