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
            _file = unicode(body["file"])
            filename = body["filename"]
            filenames = os.path.splitext(filename)
            # folder for this campaign
            filename = os.path.join(
                settings.TEMP_FOLDER,
                'chunk',
                uuid
            )
            if not os.path.exists(filename):
                os.makedirs(filename)

            # filename
            filename = os.path.join(
                filename,
                '%s%s' % (
                    uuid,
                    filenames[1] if len(filenames) > 1 else ''
                )
            )
            with open(filename, 'wb+') as destination:
                destination.write(_file.encode("utf-8"))
            # send response with appropriate mime type header
            return HttpResponse(json.dumps({
                "name": _file.name,
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
