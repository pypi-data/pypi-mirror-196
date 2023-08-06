"""
Basic http access functions
    
### Available Methods:
- get() > Call a URL and return a class method
- post() > POST JSON data to a URL and return a class method
    
### HTTP Methods return a response class:
- url > Requested URL
- code > Status code
- raw > Original text in bytes
- text > Original text as a str
- html > HTML of URL (If applicable)
- json > Converted JSON data
- pretty > Pretty JSON data

Status codes available at:
  https://en.wikipedia.org/wiki/List_of_HTTP_status_codes/
"""


class _bm:
    from ssl import create_default_context, CERT_NONE
    from urllib.error import URLError, HTTPError
    from urllib.request import urlopen, Request
    from json.decoder import JSONDecodeError
    from tooltils.info import __version__
    from json import dumps, loads


class response:
    pass

def _ctx(verify: bool, capath: str=None, cafile: str=None):
    """Setup context for urlopen"""
    
    ctx = _bm.create_default_context(capath=capath, cafile=cafile)
    
    if not verify:
        ctx.check_hostname = False
        ctx.verify_mode    = _bm.CERT_NONE
        ctx.                 set_ciphers('RSA')
    
    return ctx

def _req(req):
    """Configure request headers for payload"""
    
    req.add_header('User-Agent', 
                   f'Python-tooltils/{_bm.__version__}')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/json')
        
    return req

def _response(_url: str, data):
    """Return a classmethod containing response data"""
        
    ntext: str = data.read().decode()

    class response:
        """Response structure"""

        url:    str = _url
        code:   int = data.getcode()
        raw:  bytes = ntext.encode()
        text:   str = ntext
        html        = None

        try:
            json:  dict = _bm.loads(ntext)
            pretty: str = _bm.dumps(json, indent=2)
        except _bm.JSONDecodeError:
            json   = None
            pretty = None
            if ntext[0] == '<' or ntext[-1] == '>':
                html: str = ntext
        
    return response

def _error(err, ctx) -> None:
    if type(err) is _bm.HTTPError:
        if '403' in str(err):
            raise ConnectionError('403 Forbidden')
        elif '503' in str(err):
            raise ConnectionError('503 Unavailable')
        else:
            raise ConnectionError('Unspecified error:\n' + str(err))
    else:
        if '[Errno 8]' in str(err):
            try:
                _bm.urlopen('https://google.com', context=ctx)
                raise ConnectionError('404 Not found')
            except _bm.URLError:
                raise ConnectionError('Internet connection not found')
        elif 'ssl' in str(err):
            raise ConnectionError('Certificate not verified correctly.')

def get(url: str, params: dict={}, verify: bool=True, 
        capath: str=None, cafile: str=None, timeout: int=5) -> response:
    """Call a URL with payload included"""
    
    try:
        if not url.startswith('https://') and not url.startswith('http://'):
            url = 'https://' + url
        elif url[-1] != '?':
            url += '?'

        if params != {}:
            for i in params.keys():
                if i + '=' not in url:
                    url += i + '=' + params[i] + '&'
            url = url[:-1]

        ctx = _ctx(verify, capath, cafile)
        req = _req(_bm.Request(url, method='GET'))
        data = _bm.urlopen(req, context=ctx, timeout=timeout)
        
        return _response(url, data)
    except (_bm.URLError, _bm.HTTPError) as err:
        _error(err, ctx)
    
def post(url: str, params: dict={}, verify: bool=True, 
         capath: str=None,  cafile: str=None, timeout: int=5) -> response:
    """Post a payload to a URL"""

    if not _url.startswith('https://') and not _url.startswith('http://'):
        _url = 'https://' + _url
        
    try:
        ctx = _ctx(verify, capath, cafile)
        req = _req(_bm.Request(_url, method='POST'))
        if params != {}:
            jdata: bytes = _bm.dumps(params).encode()
            req.add_header('User-Agent', f'Python-tooltils/{_bm.__version__}')
            req.add_header('Content-Type', 'application/json')
            req.add_header('Accept', 'application/json')
        
        data = _bm.urlopen(url, data=jdata, context=ctx, timeout=timeout)
        
        return _response(url, data)
    except (_bm.URLError, _bm.HTTPError) as err:
        _error(err, ctx)
