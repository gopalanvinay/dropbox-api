from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import UserDetail
import requests
import json

def home(request, template='home.html'):
    return render(request, template, {})

#####################################################################################################

def redirect(request):

    """ CONSTRUCT REDIRECT URI TO oAUTH """
    client_id = "dntza0a177su3p3"
    response_type = "code"
    state = "041b48ea"
    redirect_uri = "https://evening-coast-74577.herokuapp.com/get-access"
    uri = "https://www.dropbox.com/oauth2/authorize?"

    uri += "client_id=" + client_id
    uri += "&response_type=" + response_type 
    uri += "&redirect_uri=" + redirect_uri
    uri += "&state=" + state 

    return HttpResponseRedirect(uri)

#####################################################################################################

def get_access(request):

    """ IF USER DOES NOT PRESS 'CANCEL' """
    if request.GET.get('code'):

        """ TO GET ACCESS TOKEN """
        code = request.GET.get('code')
        redirect_uri = "https://evening-coast-74577.herokuapp.com/get-access"
        client_id = "dntza0a177su3p3"
        client_secret = "2v0zjawwysbiew3"
        url = "https://api.dropboxapi.com/oauth2/token"
        postdata = {
            'grant_type' : 'authorization_code',
            'code' : code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret,
        }

        response = requests.post(url, data=postdata)
        ACCESS_TOKEN = response.json()['access_token']

        # Helpful string
        Bearer = "Bearer " + ACCESS_TOKEN


        """ TO GET USER DETAILS """ 
        USER_DETAILS = requests.post("https://api.dropboxapi.com/2/users/get_current_account",
            headers={'Authorization': Bearer}
            ).json()

        USER_NAME = USER_DETAILS['name']['given_name'].lower()
        USER_EMAIL = USER_DETAILS['email']

        """ CREATE NEW USER IF THIS USER IS NOT SAVED"""
        if not(UserDetail.objects.filter(user_name=USER_NAME)):
            new_user = UserDetail(user_name=USER_NAME, user_email=USER_EMAIL, access_token=ACCESS_TOKEN)
            new_user.save()

        """ REDIRECT TO CONTENTS """        
        new_redirect_uri = '/user-info?username=' + USER_NAME
        return HttpResponseRedirect(new_redirect_uri)

    else:
        new_redirect_uri = "https://evening-coast-74577.herokuapp.com"
        return HttpResponseRedirect(new_redirect_uri)        
    
#####################################################################################################

def user_info(request, template='success.html'):

        """ GET USER_NAME AND ACCESS TOKEN """
        user_name = request.GET.get('username')
        access_token = UserDetail.objects.get(user_name=user_name).access_token

        # Helpful String
        Bearer = "Bearer " + access_token

        """ USE DROPBOX API TO LIST ALL FILES IN BASE FOLDER """
        user_file_list = requests.post('https://api.dropboxapi.com/2/files/list_folder',
        headers={'Authorization': Bearer},
        json={
                "path": "",
            }).json()['entries']
        

        return render(request, template, { 'list': user_file_list, 'user': user_name})
