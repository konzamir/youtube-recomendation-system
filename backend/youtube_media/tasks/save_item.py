from main.celery import app
from ..models import (
    Links, RequestData, RequestLinkConn
)


@app.task
def save_items(d):
    data = d
    for x in data['links']:
        x['title'] = x['title'].encode('utf-8').decode('iso-8859-1')
        x['description'] = x['description'].encode('utf-8').decode('iso-8859-1')
        x['channel_title'] = x['channel_title'].encode('utf-8').decode('iso-8859-1')

    # links = [Links.objects.get_or_create(**x)[0] for x in data['links']]
    # links = [Links(**x) for x in data['links']]
    # Links.objects.bulk_create(links, ignore_conflicts=True)

    links = []
    for x in data['links']:
        try:
            l = Links.objects.get(video_id=x['video_id'])
        except Links.DoesNotExist:
            l = Links.objects.create(**x)

        links.append(l)

    try:
        page_token = data['request_data']['curr_page']
        if page_token:
            r = RequestData.objects.get(hash_data=data['request_data']['hash_data'],
                curr_page=page_token)
        else:
            r = RequestData.objects.get(hash_data=data['request_data']['hash_data'],
                curr_page__isnull=True)
    except RequestData.DoesNotExist:
        r = RequestData.objects.create(**data['request_data'])
    # r = RequestData(**data['request_data'])
    # RequestData.objects.bulk_create([r], ignore_conflicts=True)

    RequestLinkConn.objects.bulk_create(
        [RequestLinkConn(request_data=r, link=l) for l in links],
        ignore_conflicts=True
    )

    r.click_count = 1
    r.save()
    return "Saved"
