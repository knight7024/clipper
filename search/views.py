# IMPORT PACKAGE
import requests
import json
from urllib import parse
import dateutil.parser
import pytz

from django.conf import settings

from django.shortcuts import render

# Create your views here.

def search(request):
    if request.method == 'GET':
        # Get Client ID
        config_secret_common = json.loads(open(settings.CONFIG_SECRET_COMMON_FILE).read())
        client_id = config_secret_common['TWITCH']['CLIENT_ID']

        # First Set Information
        search_type = request.GET.get('type')
        search_limit = 30
        keyword = request.GET.get('keyword')
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}

        # Search by Channel
        if search_type == '0':
            url = 'https://api.twitch.tv/kraken/search/channels?limit=1&query=' + parse.quote(keyword)
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_body = response.json()
            keyword = response_body['channels'][0]['name']

            # Request
            url = "https://api.twitch.tv/kraken/clips/top"
            params = {'channel': keyword, 'limit': search_limit}
            response = requests.get(url, headers=headers, params=params)

        # Search by Game Name
        else:
            # Request
            url = "https://api.twitch.tv/kraken/clips/top"
            params = {'game': keyword, 'limit': search_limit}
            response = requests.get(url, headers=headers, params=params)

        # Make Error if not 200
        response.raise_for_status()

        response_body = response.json()['clips']

        for i in response_body:
            # DateTime Format Parsing
            date_time = dateutil.parser.parse(i['created_at'])

            #Change TimeZone
            local_timezone = pytz.timezone('Asia/Seoul')
            local_date = date_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)

            #Print Local Time
            i['created_at'] = local_date.date()

        return render(request, 'search/result.html', {'result': response_body})