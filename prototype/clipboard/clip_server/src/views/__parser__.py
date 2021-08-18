import re
import requests

class RequestParser():
    """
    This class parses incoming requests and builds a clip object from them.
    Metadata will be read from the X-C2-headers sent with the request.
    The headers specified in ACCEPTED_HEADERS can and will be simply read
    and their content put into the clip-object with the key being stripped of
    the leading X-C2-. The database itself will not validate any keys or
    values and just save the clip object as-is, so validation should happen
    here.
    If a header needs special treatment, the appropriate logic has to be added
    in the method get_data_from_request and not into the list below.
    Currently, the only other header is X-C2-download_request. This header
    promts the parser to treat the payload of the request as an URL to a media
    type like an image for example and to download the target of the URL.
    This is used by the Chrome-Extension because it cannot send binary data
    itself.
    """

    ACCEPTED_HEADERS = ['X-C2-src_url', 'X-C2-src_app',
                        'X-C2-sender_id', 'X-C2-from_hook',
                        'X-C2-filename', ]

    def file_too_large(self, url):
        """
        Checks if the requested file is to large for the server to handle.
        """
        r = requests.head(url)
        cl = r.headers.get('content-length')
        if cl and int(cl) <= self.max_content_length:
            return False
        else:
            return True

    def get_filename_from_url(self, url):
        """
        Returns the part of the URL after the last /
        """
        end = url.rsplit('/', 1)[-1]
        if self.filename_pattern.match(end):
            return end
        else:
            return None

    def get_filename_from_cd(self, cd):
        """
        Get filename from content-disposition
        """
        if not cd:
            return None
        fname = re.findall('filename=(.+)', cd)
        if len(fname) == 0:
            return None
        return fname[0]

    def download_file(self, url):
        """
        Proceeds to download the file. Returns None if an error happened
        during the download. Otherwise it returns a tuple consisting of
        the binary content, the name of the file and its mimetype
        https://www.codementor.io/aviaryan/downloading-files-from-urls-in-python-77q3bs0un
        """
        if self.file_too_large(url):
            return None

        try:
            r = requests.get(url, allow_redirects=True)
        except Exception as e:
            print('Error during download')
            return None
        if int(r.headers.get('content-length')) >= self.max_content_length:
            # HEAD to url war not indicating large file
            return None
        # Creates file from response
        file_content = r.content
        filename = self.get_filename_from_url(url)
        if not filename:
            filename = self.get_filename_from_cd(
                    r.headers.get('content-disposition'))
        mimetype = r.headers.get('content-type')

        return (file_content, filename, mimetype)

    def get_data_from_request(self, request):
        """
        This method is responsible for parsing the request. Logic pertaining
        to getting data from the request belongs in here.
        """
        data = {}
        data['mimetype'] = request.headers['Content-Type']
        """
        Server received a file, not that well tested, you should probably
        send the binary data as payload with the filename and mimetype
        in custom headers
        """
        if 'file' in request.files:
            f = request.files['file']
            data['filename'] = f.filename
            data['data'] = f.stream.read()

        # Server received an object (text)
        else:
            data['data'] = request.get_data()
            if 'X-C2-download_request' in request.headers:  # Download file
                _file = self.download_file(data['data'].decode())
                if _file:
                    data['filename'] = _file[1]
                    data['data'] = _file[0]
                    data['mimetype'] = _file[2]
                else:
                    return {'error': 'Error during download. \
                            Check if file is accessible and smaller than 15MB'}

        # Add metadata to the clip
        for h in self.ACCEPTED_HEADERS:
            if h in request.headers:
                data[h[5:]] = request.headers[h]
        return data

    def __init__(self, max_content_length):
        self.filename_pattern = re.compile('^.*\..*$')
        self.max_content_length = max_content_length
