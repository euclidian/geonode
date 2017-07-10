from django.contrib.auth.decorators import login_required

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '14/06/17'

import json
import os
from django.conf import settings
from django.http import HttpResponse


@login_required
def upload_chunk(request, uuid):
    """Upload chunk handle.
    """
    try:
        if request.method == 'POST':
            body = json.loads(request.body)
            _file = body["file"]
            filename = body["filename"]
            # folder for this campaign
            foldername = os.path.join(
                settings.TEMP_FOLDER,
                'chunk',
                uuid
            )
            if not os.path.exists(foldername):
                os.makedirs(foldername)

            # filename
            filename = os.path.join(
                foldername,
                filename
            )
            with open(filename, 'wb+') as destination:
                destination.write(_file.encode("utf-8"))
            # send response with appropriate mime type header
            return HttpResponse(status=200, content=json.dumps({
                "name": filename,
                "size": os.path.getsize(filename),
                "thumbnail_url": None,
                "delete_url": None,
                "delete_type": None
            }))
        else:
            return HttpResponse(content=json.dumps({
                "message": "Get Not Accepted"
            }), status=402)
    except Exception as e:
        return HttpResponse(content=json.dumps({
            "message": "%s" % e
        }), status=500)
