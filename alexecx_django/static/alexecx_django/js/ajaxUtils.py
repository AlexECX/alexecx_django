
from JS import JSON, XMLHttpRequest, decodeURIComponent, document, encodeURIComponent, typeof, Object, ActiveXObject #__: skip
from transcrypt import __new__, __pragma__ #__: skip


DEFAULT_MESSAGES_ID = 'django_messages'

def handleMessages(data, messages_id=DEFAULT_MESSAGES_ID):
    msg = getattr(data, messages_id, None)
    if msg:
        document.getElementById(messages_id).innerHTML = msg

__pragma__('noalias', 'type')
__pragma__('noalias', 'name')


def ajax(param):
    if window.XMLHttpRequest:
        xhr = __new__(XMLHttpRequest)()
    else:
        xhr = __new__(ActiveXObject("Microsoft.XMLHTTP"))()
    
    xhr.open(param.type, param.url)
    if param.contentType:
       content_type = param.contentType
    else:
        content_type = "application/x-www-form-urlencoded; charset=UTF-8"
    
    xhr.setRequestHeader('Content-Type', content_type)

    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
    if param.headers:
        for header,value in Object.entries(param.headers):
            xhr.setRequestHeader(header, value)

    def xhr_onload():
        if xhr.status is 200:
            try:
                param.success(JSON.parse(xhr.responseText), xhr.statusText, xhr)
            except:
                param.success(xhr.responseText, xhr.statusText, xhr)
        else:
            if param.error:
                param.error(xhr, xhr.statusText, xhr.responseText)
            else:
                alert("ajax response error: "+xhr.responseText)

    xhr.onload = xhr_onload
    xhr.onerror = lambda x, y, z: param.error(xhr, xhr.statusText, "Unknown Error Occured. Server response not received.")
    if param.beforeSend:
        param.beforeSend(xhr, param)

    if param.data:
        xhr.send(param.data)
    else:
        xhr.send()
    

def formSerialize(form):
    field = []
    s = []
    if typeof(form) == 'object' and form.nodeName.toLowerCase() == 'form':
        for field in form.elements:
            if field.name and not field.disabled and field.type not in ['file', 'reset', 'submit', 'button']:
                if field.type == 'select-multiple':
                    for option in reversed(field.options):
                        if option.selected:
                            s[s.length] = encodeURIComponent(field.name) + "=" + encodeURIComponent(option.value)
                elif field.type not in ['checkbox', 'radio'] or field.checked:
                    s[s.length] = encodeURIComponent(field.name) + "=" + encodeURIComponent(field.value)
    return ("&".join(s)).replace('/%20/', '+')

__pragma__('alias', 'name', 'py_name')
__pragma__('alias', 'type', 'py_type')


from pragmajs import csrfSafeMethod, sameOrigin #__: skip

def csrfCompat(xhr, settings):
    if not csrfSafeMethod(settings.type) and sameOrigin(settings.url):
        # Send the token to same-origin, relative URLs only.
        # Send the token only if the method warrants CSRF protection
        # Using the CSRFToken value acquired earlier
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'))


def getCookie(cookie_name):
    cookie_value = None
    if document.cookie and document.cookie is not '':
        cookies = document.cookie.js_split(';')
        for cookie in cookies:
            cookie = cookie.strip()
            if cookie[:len(cookie_name)+1] == cookie_name+'=':
                cookie_value = decodeURIComponent(cookie[len(cookie_name)+1:])
                break
    return cookie_value

__pragma__('js', '{}', """
// This function gets cookie with a given name


/*
The functions below will create a header with csrftoken
*/

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
""")
        