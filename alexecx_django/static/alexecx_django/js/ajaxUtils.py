
from JS import JSON, XMLHttpRequest, decodeURIComponent, document, encodeURIComponent, typeof, Object, ActiveXObject #__: skip
from transcrypt import __new__, __pragma__ #__: skip

__pragma__('js', '{}', """
if (!Object.entries) {
    Object.entries = function( obj ){
        var ownProps = Object.keys( obj ),
            i = ownProps.length,
            resArray = new Array(i);
        while (i--)
        resArray[i] = [ownProps[i], obj[ownProps[i]]];
        
        return resArray;
    };
}""")

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
    
    if param.contentType:
       content_type = param.contentType
    else:
        content_type = "application/x-www-form-urlencoded; charset=UTF-8"

    if param.dataType:
        xhr.responseType = param.dataType
    
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

    xhr.open(param.type, param.url)
    if param.data:
        xhr.send(param.data)
    else:
        xhr.send()

def serialize(obj):
    s = []
    for key in obj:
        s.append(encodeURIComponent(key) + "=" + encodeURIComponent(obj[key]))
    return ("&".join(s)).replace('/%20/', '+')

def formJS():
    form_data = {} #__: jsiter
    if typeof(form) == 'object' and form.nodeName.toLowerCase() == 'form':
        for field in form.elements:
            if field.name and not field.disabled and field.type not in ['file', 'reset', 'submit', 'button']:
                if field.type == 'select-multiple':
                    for option in reversed(field.options):
                        if option.selected:
                            form_data[field.name] = option.value
                elif field.type not in ['checkbox', 'radio'] or field.checked:
                    form_data[field.name] = field.value
    return form_data

def formSerialize(form):
    return serialize(formJS(form))

def formJSON(form):
    return JSON.stringify(formJS(form))

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
        