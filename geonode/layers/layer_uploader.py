__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '14/06/17'

import json
import os
from django.conf import settings
from django.http import HttpResponse


def upload_chunk(request, uuid):
    """Upload chunk handle.
    """
    try:
        if request.method == 'POST':
            _file = request.FILES['file']
            filename = _file.name
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
            return _upload_chunk(request, _file, filename)
        else:
            print 'why get'
    except Exception as e:
        print e


def _upload_chunk(request, _file, filename):
    """Upload chunk file for specific folder.
    :param _file: file to be saved

    :param filename:filename path to be saved
    :type filename: src
    """

    # save uploaded file
    if 'HTTP_CONTENT_RANGE' in request.META:
        range_str = request.META.get('HTTP_CONTENT_RANGE')
        start_bytes = int(range_str.split(' ')[1].split('-')[0])
        # remove old file if upload new file
        if start_bytes == 0:
            if os.path.exists(filename):
                os.remove(filename)

        # append chunk to the file on disk, or create new
        with open(filename, 'ab') as f:
            f.seek(start_bytes)
            f.write(_file.read())

    else:
        # this is not a chunked request, so just save the whole file
        # append chunk to the file on disk, or create new
        with open(filename, 'wb+') as destination:
            for chunk in _file.chunks():
                destination.write(chunk)

    # send response with appropriate mime type header
    return HttpResponse(json.dumps({
        "name": _file.name,
        "size": os.path.getsize(filename),
        "thumbnail_url": None,
        "delete_url": None,
        "delete_type": None
    }))
