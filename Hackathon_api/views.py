from datetime import datetime
from django.forms import URLField
from .models import *
from django.http import JsonResponse 
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import json
from .decorators import authorized_users_only
from django.contrib.auth import authenticate

# Create your views here.

@csrf_exempt
@authorized_users_only(1,allowed_roles=['authorized_user'])
def Create_hackathon(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    json_data = json.loads(request.POST['testvalues'])
    title = json_data.get('title')
    description = json_data.get('description')
    submission_type = json_data.get('submission_type')
    start_date = json_data.get('start_date')
    end_date = json_data.get('end_date')
    reward_prize = json_data.get('reward_prize')
    github_repository = json_data.get('github_repository')
    other_links = json_data.get('other_links')

    background_imagefile = request.FILES.get('backgroundimage')
    logo_imagefile = request.FILES.get('logoimage')
    if not (background_imagefile and logo_imagefile):
        return JsonResponse({'error': 'Background and logo images are required'}, status=400)

    background_imagefile_path = default_storage.save(background_imagefile.name, background_imagefile)
    logo_imagefile_path = default_storage.save(logo_imagefile.name, logo_imagefile)

    try:
        hackathon = Create_hackathons.objects.create(
            title=title,
            description=description,
            background_image=background_imagefile_path,
            hackathon_image_logo=logo_imagefile_path,
            submission_type=submission_type,
            start_date=datetime.strptime(start_date, "%Y-%m-%d"),
            end_date=datetime.strptime(end_date, "%Y-%m-%d"),
            reward_prize=reward_prize,
            github_repository=github_repository,
            other_links=other_links
        )
        response = {'response': serializers.serialize('python', [hackathon])[0]['fields']}

        return JsonResponse(response,safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@authorized_users_only(0,allowed_roles=['user'])
def Upload_Submission(request):

    submission_json       = json.loads(request.POST['submission'])
    credentials_json      = json.loads(request.POST['credentials'])

    participant = authenticate(username = credentials_json.get('username'),
                                password  = credentials_json.get('password') )
    
    enrolled_hackathon = submission_json.get('enrolled_hackathon')
    submission_name = submission_json.get('submission_name')
    submission_summary= submission_json.get('submission_summary')
    favourite_submission = submission_json.get('favourite')
    if favourite_submission == 'true':
        favourite = True
    else:
        favourite = False
    submission_type = Create_hackathons.objects.get(title = enrolled_hackathon).submission_type
    # submission_type = 'file' # test

    if submission_type == 'file':
            submissions_as_file = request.FILES.get('challenge_submissions',False)
            if submissions_as_file:
                submissions_as_file_path = default_storage.save(submissions_as_file.name,submissions_as_file)
                Submission_responce = Submissions.objects.create(participant = participant,
                                                                enrolled_hackathon = enrolled_hackathon,
                                                                submission_name = submission_name,
                                                                submission_summary = submission_summary,
                                                                submission_as_file = submissions_as_file_path,
                                                                favourite = favourite,
                                                                submission_type = 'file',
                                                                )
                

                response = serializers.serialize('python',[Submission_responce],fields=['enrolled_hackathon',
                                                                                        'submission_name',
                                                                                        'submission_summary',
                                                                                        'submission_as_file',
                                                                                        'date_of_submission'])[0]['fields']
                return JsonResponse({'response':response},safe=False)
            else:
                return JsonResponse({"invalidfile":"Please check your file "},status=400 )
            
    else: 
        challenge_link = submission_json.get('challenge')
        challenge_link_check = validate_url(challenge_link)
        if challenge_link_check:
            Submission_responce = Submissions.objects.create(participant = participant,
                                                             enrolled_hackathon = enrolled_hackathon,
                                                             submission_name = submission_name,
                                                             submission_summary = submission_summary,
                                                             submission_as_link = challenge_link,
                                                             submission_type = 'link')
            
            
            response = serializers.serialize('python',[Submission_responce],fields=['enrolled_hackathon',
                                                                                        'submission_name',
                                                                                        'submission_summary',
                                                                                        'submission_as_link',
                                                                                        'date_of_submission'])[0]['fields']
            return JsonResponse({'response':response},safe=False)
        else:
             return JsonResponse({"invalidlink":"Please Check your link"},status=400 )
    
def validate_url(url):
    url_form_field = URLField()
    try:
        url = url_form_field.clean(url)
    except Exception:
        return False
    return True

@csrf_exempt   
@authorized_users_only(0,allowed_roles=['user'])
def Registration(request):
    credentials_json      =  json.loads(request.POST['credentials'])
    participant           =  authenticate(username = credentials_json.get('username'),
                                          password  = credentials_json.get('password') )
    
    Registration_json = json.loads(request.POST['Registration'])
    enrolled_hackathon = Registration_json.get('enrolled_to')
    email = Registration_json.get('email')

    Registration = Hackathon_Registeration.objects.create(participant = participant,
                                                      participant_name = credentials_json.get('username'),
                                                      enrolled_hackathon = enrolled_hackathon,
                                                      email = email)
    
    response = serializers.serialize('python',[Registration],fields=['participant_name',
                                                                     'enrolled_hackathon',
                                                                     'date_of_registration',
                                                                     'email'])[0]['fields']
    return JsonResponse({"response":response},safe=False)
    
@csrf_exempt 
def User_enrolled_hackathons(request):
    context = {}
    credentials_json = json.loads(request.POST['credentials'])
    username = credentials_json.get('username')
    password = credentials_json.get('password')
    user = authenticate(username = username,
                        password = password)
    enrolled_query_set = reversed(Hackathon_Registeration.objects.filter(participant = user))
    hackathon_list = {}
    key = 0
    for hackathon in enrolled_query_set:
        
        enrolled_hackathon_serialized = get_hackathon_data(hackathon.enrolled_hackathon,'User_enrolled_hackathons')
        hackathon_list[key] = {'title':enrolled_hackathon_serialized['title'],
                                     'backgroundimage':enrolled_hackathon_serialized['background_image'],
                                     'hackathan_image_logo':enrolled_hackathon_serialized['hackathon_image_logo'],
                                     'description':enrolled_hackathon_serialized['description'],
                                     'enrolled_on':hackathon.date_of_registration} 
        key +=1
    context[username] = hackathon_list
    return JsonResponse(context,safe=False)


@csrf_exempt 
def All_Submissions(request):
    context = {}
    credentials_json = json.loads(request.POST['credentials'])
    username = credentials_json.get('username')
    password = credentials_json.get('password')
    user = authenticate(username = username,
                        password = password)
    
    submits_query_set = reversed(Submissions.objects.filter(participant = user))
    submits_list = {}
    key = 0
    for submit in submits_query_set:
        if submit.submission_type == 'file':
            set_submission = 'submission_as_file'
        else:
            set_submission = 'submission_as_link'

        submits_list[key] = serializers.serialize('python',[submit],fields=['enrolled_hackathon',
                                                                            set_submission,
                                                                            'date_of_submission',
                                                                            'submission_type'])[0]['fields']
        
        hackathon_serialized = get_hackathon_data(submit.enrolled_hackathon,'All_Submissions')
    
        submits_list[key]['data'] = {'title':hackathon_serialized['title'],
                                     'backgroundimage':hackathon_serialized['background_image'],
                                     'hackathan_image_logo':hackathon_serialized['hackathon_image_logo'],
                                     'description':hackathon_serialized['description']} 
        key +=1
    context[username] = submits_list
    return JsonResponse(context,safe=False)


def get_hackathon_data(title,flag):
    if flag == 'All_Submissions':
        hackathon = Create_hackathons.objects.get(title = title)
        # print(hackathon,'*****************************')
        return serializers.serialize('python',[hackathon])[0]['fields']
    
    elif flag == 'on_click_of_allsubmission':
        hackathon = Create_hackathons.objects.get(title = title)
        return serializers.serialize('python',[hackathon],fields=['title',
                                                                  'background_image',
                                                                  'hackathon_image_logo',
                                                                  'description',
                                                                  'start_date',
                                                                  'end_date',
                                                                  'reward_prize',
                                                                  'github_repository',
                                                                  'other_links'])[0]['fields']
    
    elif flag == 'User_enrolled_hackathons':
        hackathon = Create_hackathons.objects.get(title = title)
        return serializers.serialize('python',[hackathon])[0]['fields']
    


def Hackathon_list(request):
    context = {}
    hackathon_queryset = reversed(Create_hackathons.objects.all())
    hackathon_data={}
    key = 0
    for hackathon in hackathon_queryset:
        hackathon_data[key] = serializers.serialize('python',[hackathon],fields=['title',
                                                                                 'background_image',
                                                                                 'hackathon_image_logo',
                                                                                 'start_date',
                                                                                 'end_date',
                                                                                 'reward_prize',
                                                                                 'submission_type'])[0]['fields']
        key +=1
    context['Hackathon_list'] = hackathon_data
    return JsonResponse(context,safe=False)


@csrf_exempt
def click_on_submission(request):
    title_data = json.loads(request.POST['title'])
    title =  title_data.get('title')
    Hackathon = get_hackathon_data(title,'on_click_of_allsubmission')
    respose = {'response': Hackathon}
    return JsonResponse(respose,safe=False)


@csrf_exempt
def Favourite_submissions(request):
    context = {}
    credentials_data = json.loads(request.POST['credentials'])
    user = authenticate(username = credentials_data.get('username'),
                        password = credentials_data.get('password'))
    Favourites = Submissions.objects.filter(participant = user,favourite = True)
    if not Favourites:
        return JsonResponse({'response':'no favourites selected'})
    Submissions_list = {}
    key = 0
    for submissions in Favourites:
        Submissions_list[key] = serializers.serialize('python',[submissions])[0]['fields']
        key +=1
    context['Favourite_submissions'] = Submissions_list
    return JsonResponse(context,safe=False)

