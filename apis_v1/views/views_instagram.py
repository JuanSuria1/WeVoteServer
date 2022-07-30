# apis_v1/views/views_instagram.py
# Brought to you by We Vote. Be good.
# -*- coding: UTF-8 -*-
from config.base import get_environment_variable
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from import_export_twitter.controllers import twitter_identity_retrieve_for_api, twitter_sign_in_start_for_api, \
    twitter_sign_in_request_access_token_for_api, twitter_sign_in_request_voter_info_for_api, \
    twitter_process_deferred_images_for_api, twitter_sign_in_retrieve_for_api, twitter_retrieve_ids_i_follow_for_api, \
    twitter_native_sign_in_save_for_api
import json
from urllib.parse import quote
from urllib.parse import urlencode
import wevote_functions.admin
from wevote_functions.functions import get_voter_device_id, positive_value_exists
import requests
from instagrapi import Client


logger = wevote_functions.admin.get_logger(__name__)

WE_VOTE_SERVER_ROOT_URL = get_environment_variable("WE_VOTE_SERVER_ROOT_URL")


def twitter_identity_retrieve_view(request):  # twitterIdentityRetrieve
    """
    Find the kind of owner and unique id of this twitter handle. We use this to take an incoming URI like
    https://wevote.guide/RepBarbaraLee and return the owner of 'RepBarbaraLee'. (twitterIdentityRetrieve)
    :param request:
    :return:
    """
    twitter_handle = request.GET.get('twitter_handle', '')

    if not positive_value_exists(twitter_handle):
        status = 'VALID_TWITTER_HANDLE_MISSING'
        json_data = {
            'status':                   status,
            'success':                  False,
            'twitter_handle':           twitter_handle,
            'owner_found':              False,
            'kind_of_owner':            '',
            'owner_we_vote_id':         '',
            'owner_id':                 0,
            'google_civic_election_id': 0,
        }
        return HttpResponse(json.dumps(json_data), content_type='application/json')

    voter_device_id = get_voter_device_id(request)  # We standardize how we take in the voter_device_id
    results = twitter_identity_retrieve_for_api(twitter_handle, voter_device_id)
    json_data = {
        'status':                                   results['status'],
        'success':                                  results['success'],
        'twitter_handle':                           results['twitter_handle'],
        'owner_found':                              results['owner_found'],
        'kind_of_owner':                            results['kind_of_owner'],
        'owner_we_vote_id':                         results['owner_we_vote_id'],
        'owner_id':                                 results['owner_id'],
        'google_civic_election_id':                 results['google_civic_election_id'],
        'twitter_description':                      results['twitter_description'],
        'twitter_followers_count':                  results['twitter_followers_count'],
        'twitter_photo_url':                        results['twitter_photo_url'],
        'we_vote_hosted_profile_image_url_large':   results['we_vote_hosted_profile_image_url_large'],
        'we_vote_hosted_profile_image_url_medium':  results['we_vote_hosted_profile_image_url_medium'],
        'we_vote_hosted_profile_image_url_tiny':    results['we_vote_hosted_profile_image_url_tiny'],
        'twitter_profile_banner_url_https':         results['twitter_profile_banner_url_https'],
        'twitter_user_website':                     results['twitter_user_website'],
        'twitter_id':                               results['twitter_id'],
        'twitter_name':                             results['twitter_name'],
        }
    return HttpResponse(json.dumps(json_data), content_type='application/json')


################################################################
def instagram_sign_in_start_view(request):  # twitterSignInStart (Step 1)


    cl = Client()
    cl.login("juan_suria19", '')

    user_id = cl.user_id_from_username("gamingguy2289")
    print("*************************************")
    print(user_id)
    print(cl.user_followers(cl.user_id).keys())
    print(cl.user_following(cl.user_id))



    #r = requests.get('https://graph.facebook.com/v14.0/me', params={'access_token':'EAAKY4bSSV30BAApt7EZBqz0fjp2ZCjmWYARbzajDWjL3gzZBGR84s4mWZBRJxxP82ug3hDQVRv7VUssPf0ZB1x0TQ4l8S7P65MirH1vOhPmpI1pF0vvieiwV9cujcZAEm1X0KDPFJP6eZCMgvXImhOJc1wMuk7h64OSTf1ReDb1NZAVFwPwXMgOCmkjZB20MWWAPUIeRK8EpZBLdHyipSrDV1vJ0ZCDkZCXVK3R3rABjVBzqgeedwZBlPgJy8'})
    #p = requests.get( "https://platform-lookaside.fbsbx.com/platform/profilepic/?asid=1950389381838858&height=50&width=50&ext=1661147283&hash=AeRTy0_Tv3tmzH8aeg0")
    #c = requests.get('https://graph.instagram.com/v14.0/me', params={'access_token':'IGQVJWT2p3b3V4VTMzOXljYms3QkdJR2J3NWZAhRkdkaTNIeHlROUdUS2ZAxOEg5Ym1qTmVpa3pOcUUxNGdfM1hGQTlPekhIQVBJQk4xZAVRhNjdDaDBrOVRobnV0VUVTUDQtMXFlRmxibUc2R3JlY24xaTUyOW5zazdvYU9R'})
    #print(WE_VOTE_SERVER_ROOT_URL)
   # client_id = '599015611785883'
    #redirect_uri = f'{WE_VOTE_SERVER_ROOT_URL}apis/v1/instagramSignInRequestAccessToken/'
    #scope = 'user_profile,user_media'
    #response_type = 'code'


    #stuff = {
    #    c.text,
        #p.content,  
    #}
    
    json_data = {
        'status':               200,
        'success':              "worked",
        'test':                 "tester",
#        'voter_device_id':      voter_device_id,
#        'twitter_redirect_url': results['twitter_redirect_url'],
#        'voter_info_retrieved': results['voter_info_retrieved'],
#        'switch_accounts':      results['switch_accounts'],  # If true, new voter_device_id returned
#        'cordova':              cordova,
    }

    #return HttpResponse(stuff, content_type='application/json')
    return HttpResponseRedirect(f'https://api.instagram.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&response_type={response_type}')


def instagram_sign_in_request_access_token_view(request):

    code = request.GET.get('code', '')
    client_id = '599015611785883'
    client_secret = '8c04837a59e6d5f218ca2cb3da3ec6a4'
    grant_type = 'authorization_code'
    redirect_uri = f'{WE_VOTE_SERVER_ROOT_URL}apis/v1/instagramSignInRequestAccessToken/'
  
    
    data = {
        'code'                 : code,
        'client_id'            : client_id,
        'client_secret'        : client_secret,
        'grant_type'           : grant_type,
        'redirect_uri'         : redirect_uri,
    }
    r = requests.post('https://api.instagram.com/oauth/access_token', data = data)

    #voter_device_id = get_voter_device_id(request)  # We standardize how we take in the voter_device_id
    #incoming_request_token = request.GET.get('oauth_token', '')
    #incoming_oauth_verifier = request.GET.get('oauth_verifier', '')
    #return_url = request.GET.get('return_url', '')
    #cordova = request.GET.get('cordova', False)

    #results = twitter_sign_in_request_access_token_for_api(voter_device_id,
                                                           #incoming_request_token, incoming_oauth_verifier,
                                                           #return_url, cordova)

    #if positive_value_exists(results['return_url']):
      #  next_step_url = WE_VOTE_SERVER_ROOT_URL + "/apis/v1/twitterSignInRequest/"  # twitterSignInRequestVoterInfo
       # next_step_url += "?voter_info_mode=1"
        #next_step_url += "&voter_device_id=" + voter_device_id
        #next_step_url += "&return_url=" + quote(results['return_url'], safe='')
        #next_step_url += "&cordova=" + str(cordova)
        #return HttpResponseRedirect(next_step_url)

    #json_data = {
     #   'status':                           results['status'],
      #  'success':                          results['success'],
       # 'voter_device_id':                  voter_device_id,
        #'access_token_and_secret_returned': results['access_token_and_secret_returned'],
        #'cordova':                          cordova,
        #'voter_info_mode':                  voter_info_mode,
    #}

    #if cordova:
    #    return twitter_cordova_signin_response(request, json_data)
    #else:
    return HttpResponse(r.text)

#######################################################################################################################################################












def twitter_sign_in_request_view(request):  # twitterSignInRequest (Switch for Step 1 & Step 2)
    voter_info_mode = request.GET.get('voter_info_mode', 0)
    if positive_value_exists(voter_info_mode):
        return twitter_sign_in_request_voter_info_view(request)
    else:
        return twitter_sign_in_request_access_token_view(request)


def twitter_sign_in_request_access_token_view(request):  # twitterSignInRequestAccessToken (Step 2)
    """
    Step 2 of the Twitter Sign In Process (twitterSignInRequestAccessToken) for the WebApp
    :param request:
    :return:
    """

    voter_info_mode = request.GET.get('voter_info_mode', 0)
    voter_device_id = get_voter_device_id(request)  # We standardize how we take in the voter_device_id
    incoming_request_token = request.GET.get('oauth_token', '')
    incoming_oauth_verifier = request.GET.get('oauth_verifier', '')
    return_url = request.GET.get('return_url', '')
    cordova = request.GET.get('cordova', False)

    results = twitter_sign_in_request_access_token_for_api(voter_device_id,
                                                           incoming_request_token, incoming_oauth_verifier,
                                                           return_url, cordova)

    if positive_value_exists(results['return_url']):
        next_step_url = WE_VOTE_SERVER_ROOT_URL + "/apis/v1/twitterSignInRequest/"  # twitterSignInRequestVoterInfo
        next_step_url += "?voter_info_mode=1"
        next_step_url += "&voter_device_id=" + voter_device_id
        next_step_url += "&return_url=" + quote(results['return_url'], safe='')
        next_step_url += "&cordova=" + str(cordova)
        return HttpResponseRedirect(next_step_url)

    json_data = {
        'status':                           results['status'],
        'success':                          results['success'],
        'voter_device_id':                  voter_device_id,
        'access_token_and_secret_returned': results['access_token_and_secret_returned'],
        'cordova':                          cordova,
        'voter_info_mode':                  voter_info_mode,
    }

    if cordova:
        return twitter_cordova_signin_response(request, json_data)
    else:
        return HttpResponse(json.dumps(json_data), content_type='application/json')


def twitter_native_sign_in_save_view(request):  # twitterNativeSignInSave
    """
    For the native "app" react-native-oauth, replaces Steps 1 & 2 of the WebApp Twitter Sign In Process.
    Receives twitter_access_token and twitter_access_token_secret from the native app's authenticate() call
    :param request:
    :return:
    """

    voter_device_id = get_voter_device_id(request)  # We standardize how we take in the voter_device_id
    twitter_access_token = request.GET.get('twitter_access_token', '')
    twitter_access_token_secret = request.GET.get('twitter_access_token_secret', '')
    results_native = twitter_native_sign_in_save_for_api(voter_device_id, twitter_access_token,
                                                         twitter_access_token_secret)

    if not results_native['success'] == True:
        logger.error("Bad save in twitter_native_sign_in_save_view: " + results_native['status'])

    # Call equivalent of oAuth for WebApp Step 3
    results_voter_info = twitter_sign_in_request_voter_info_for_api(voter_device_id, "Native API Call, No Return URL")

    json_data = {
        'status':               results_voter_info['status'] + ' ' + results_native['status'],
        'success':              results_voter_info['success'],
        'twitter_handle':       results_voter_info['twitter_handle'],
        'twitter_handle_found': results_voter_info['twitter_handle_found'],
        'twitter_secret_key':   results_voter_info['twitter_secret_key'],
        'voter_device_id':      results_voter_info['voter_device_id'],
        'voter_info_retrieved': results_voter_info['voter_info_retrieved'],
        'switch_accounts':      results_voter_info['switch_accounts'],
    }
    return HttpResponse(json.dumps(json_data), content_type='application/json')


def twitter_sign_in_request_voter_info_view(request):  # twitterSignInRequestVoterInfo (Step 3)
    """
    Step 3 of the Twitter Sign In Process (twitterSignInRequestVoterInfo)
    :param request:
    :return:
    """

    cordova = request.GET.get('cordova', False)
    return_url = request.GET.get('return_url', '')
    voter_device_id = get_voter_device_id(request)  # We standardize how we take in the voter_device_id
    voter_info_mode = request.GET.get('voter_info_mode', 0)

    results = twitter_sign_in_request_voter_info_for_api(voter_device_id, return_url)

    if positive_value_exists(results['return_url']) and not positive_value_exists(cordova):
        return HttpResponseRedirect(results['return_url'])

    json_data = {
        'status':               results['status'],
        'success':              results['success'],
        'voter_device_id':      results['voter_device_id'],
        'twitter_handle':       results['twitter_handle'],
        'twitter_handle_found': results['twitter_handle_found'],
        'voter_info_mode':      voter_info_mode,
        'voter_info_retrieved': results['voter_info_retrieved'],
        'switch_accounts':      results['switch_accounts'],
    }

    if cordova:
        return twitter_cordova_signin_response(request, json_data)
    else:
        return HttpResponse(json.dumps(json_data), content_type='application/json')


def twitter_cordova_signin_response(request, json_data):
    """
    https://medium.com/@jlchereau/stop-using-inappbrowser-for-your-cordova-phonegap-oauth-flow-a806b61a2dc5
    :param request:
    :return: A webpage that initiates a native scheme for iOS (received in Application.js in the WebApp)
    """
    logger.debug("twitter_cordova_signin_response: " + urlencode(json_data))

    template_values = {
        'query_string': urlencode(json_data),
    }

    # return render(request, 'cordova/cordova_ios_redirect_to_scheme.html', template_values,
    #               content_type='text/html')
    return render(request, 'cordova/cordova_ios_redirect_to_scheme.html', template_values,
                  content_type='text/html')


def twitter_process_deferred_images_view(request):  # twitterProcessDeferredImages
    """
    Deferred processing of the twitter image URLs, to save 5 or 10 seconds on initial sign in
    :param request:
    :return:
    """
    results = twitter_process_deferred_images_for_api(
        organization_we_vote_id=request.GET.get('organization_we_vote_id'),
        status=request.GET.get('status'),
        success=request.GET.get('success'),
        twitter_id=request.GET.get('twitter_id'),
        twitter_name=request.GET.get('twitter_name'),
        twitter_profile_banner_url_https=request.GET.get('twitter_profile_banner_url_https'),
        twitter_profile_image_url_https=request.GET.get('twitter_profile_image_url_https'),
        twitter_secret_key=request.GET.get('twitter_secret_key'),
        twitter_screen_name=request.GET.get('twitter_screen_name'),
        voter_we_vote_id_for_cache=request.GET.get('voter_we_vote_id_for_cache')
    )

    return HttpResponse(json.dumps(results), content_type='application/json')


def twitter_sign_in_retrieve_view(request):  # twitterSignInRetrieve
    """
    :param request:
    :return:
    """
    voter_device_id = get_voter_device_id(request)  # We standardize how we take in the voter_device_id
    image_load_deferred = request.GET.get('image_load_deferred'),
    load_deferred = image_load_deferred and image_load_deferred[0] == 'true'

    results = twitter_sign_in_retrieve_for_api(voter_device_id=voter_device_id, image_load_deferred=load_deferred)

    json_data = {
        'status':                                   results['status'],
        'success':                                  results['success'],
        'existing_twitter_account_found':           results['existing_twitter_account_found'],
        'twitter_image_load_info':                  results['twitter_image_load_info'],
        'twitter_profile_image_url_https':          results['twitter_profile_image_url_https'],
        'twitter_retrieve_attempted':               True,
        'twitter_secret_key':                       results['twitter_secret_key'],
        'twitter_sign_in_failed':                   results['twitter_sign_in_failed'],
        'twitter_sign_in_found':                    results['twitter_sign_in_found'],
        'twitter_sign_in_verified':                 results['twitter_sign_in_verified'],
        'voter_device_id':                          voter_device_id,
        'voter_has_data_to_preserve':               results['voter_has_data_to_preserve'],
        'voter_we_vote_id':                         results['voter_we_vote_id'],
        'voter_we_vote_id_attached_to_twitter':     results['voter_we_vote_id_attached_to_twitter'],
        'we_vote_hosted_profile_image_url_large':   results['we_vote_hosted_profile_image_url_large'],
        'we_vote_hosted_profile_image_url_medium':  results['we_vote_hosted_profile_image_url_medium'],
        'we_vote_hosted_profile_image_url_tiny':    results['we_vote_hosted_profile_image_url_tiny'],
        # 'twitter_who_i_follow':                   results['twitter_who_i_follow'],
        # There are more values we currently aren't returning
    }

    return HttpResponse(json.dumps(json_data), content_type='application/json')


def twitter_retrieve_ids_i_follow_view(request): # twitterRetrieveIdsIFollow
    """
    :param request:
    :return:
    """
    voter_device_id = get_voter_device_id(request)  # We standardize how we take in the voter_device_id

    results = twitter_retrieve_ids_i_follow_for_api(voter_device_id=voter_device_id)

    json_data = {
        'status':                   results['status'],
        'success':                  results['success'],
        'voter_device_id':          voter_device_id,
        'twitter_ids_i_follow':     results['twitter_ids_i_follow'],
    }
    return HttpResponse(json.dumps(json_data), content_type='application/json')
