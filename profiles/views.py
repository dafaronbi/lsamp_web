from django.shortcuts import render
from django.db.models import Q
from django.core.files import File
from .models import user
import requests
import os
from collections import Counter

def update_database():
    #delete old model
    user.objects.all().delete()

    #get all sheet values
    smartsheet = requests.get("https://api.smartsheet.com/2.0/sheets/976201423579012", headers={'Authorization': 'Bearer R3xflmbloIqxFh6JfBfjWgT01RB2Sx5AOCewZ'})

    # count number of occurences of name
    count = Counter()

    for person in smartsheet.json()['rows']:
        # create new object in user model
        new_user = user()

        # get name
        name = person['cells'][2]['value'].lower() + " " + person['cells'][3]['value'].lower()
        count.update([name])

        new_user.picture = name + str(count[name]) + '.jpg'

        try:
            new_user.latin = person['cells'][0]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Latin")
        try:
            new_user.hawaiian = person['cells'][1]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Hawaiian")
        try:
            new_user.fName = person['cells'][2]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for First Name")
        try:
            new_user.lName = person['cells'][3]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Last Name")
        try:
            new_user.pronouns = person['cells'][4]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Pronouns")
        try:
            new_user.lsampAliance = person['cells'][5]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for LSAMP Aliance")
        try:
            new_user.uInstitution = person['cells'][6]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Undegraduate Institution")
        try:
            new_user.uYear = person['cells'][7]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Undegraduat Graduation Year")
        try:
            new_user.uMajor = person['cells'][8]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Undegraduate Major")
        try:
            new_user.email = person['cells'][9]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Email")
        try:
            new_user.ccTransfer = person['cells'][10]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Comunity College Transfer")
        try:
            new_user.city = person['cells'][11]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for City")
        try:
            new_user.state = person['cells'][12]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for State")
        try:
            new_user.phone = person['cells'][13]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Phone")
        try:
            new_user.organization = person['cells'][14]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Organization")
        try:
            new_user.status = person['cells'][15]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Status")
        try:
            new_user.title = person['cells'][16]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Title")
        try:
            new_user.pInterest = person['cells'][17]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Personal Interest")
        try:
            new_user.mentorship = person['cells'][18]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Mentorship")
        try:
            new_user.areaOfInterest = person['cells'][19]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Area of Interest")
        try:
            new_user.areaOfExpertise = person['cells'][20]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Area of Expertise")
        try:
            new_user.pastResearch = person['cells'][21]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Past Research")
        try:
            new_user.pastClubs = person['cells'][22]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Past Clubs")
        try:
            new_user.linkedin = person['cells'][23]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Linkedin")
        try:
            new_user.twitter = person['cells'][24]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Twitter")
        try:
            new_user.instagram = person['cells'][25]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Instagram")
        try:
            new_user.website = person['cells'][26]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Website")
        try:
            new_user.dateCreated = person['cells'][27]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Date Created")
        try:
            new_user.createdBy = person['cells'][28]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Created By")
        try:
            new_user.ccTransfer2 = person['cells'][29]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Comunity College Transfer 2")
        try:
            new_user.ccInstitution = person['cells'][30]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Community College Institution")
        try:
            new_user.address = person['cells'][31]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for Address")
        try:
            new_user.state2 = person['cells'][32]['value']
        except:
            print("DATA WARNING: there is no smartsheet entry for State 2")
        new_user.save(force_insert=True)



def list_view(request):
    update_database()
    all = user.objects.order_by('lName')

    if request.method == "POST":
        searched = request.POST['searched']
        if searched != "":
            all = all.filter(Q(fName__contains=searched) | Q(lName__contains=searched) | Q(title__contains=searched) | Q(organization__contains=searched))
    return render(request, 'user_profiles.html',{'user_data':all})

def bio_view(request,picture_string):
    item = user.objects.get(picture=picture_string)
    return render(request, 'bio.html',{'data':item})

