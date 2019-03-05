from .ajaxUtils import ajax, csrfCompat, formSerialize
from JS import alert, document, window, CustomEvent, JSON #__: skip
from org.transcrypt import __pragma__, __new__ #__: skip


__pragma__('js', '{}', """
class AjaxFormEvent extends CustomEvent {
    constructor(event_name, data, xhr) {
        super(event_name);
        this.xhr = xhr;
        this.data = data;
    }
}""")
__pragma__('js', '{}', """/**
*  
*  
*/""")
class AjaxForm(object):
    
    def __init__(self, form):
        self.form = form
        self.form.addEventListener('submit', lambda event: self.form_submit(event))
        self.method = form.method
        self.action = form.action
        self.callbacks = {} #__: jsiter
        self.callbacks['ajaxformsuccess'] = self.ajax_success
        self.form.addEventListener(
                'ajaxformsuccess', 
                lambda event: self.callbacks['ajaxformsuccess'](event)
                )
        self.callbacks['ajaxformjson'] = self.on_json
        self.form.addEventListener(
                'ajaxformjson', 
                lambda event: self.callbacks['ajaxformjson'](event)
                )
        self.callbacks['ajaxformhttp'] = self.on_http
        self.form.addEventListener(
                'ajaxformhttp', 
                lambda event: self.callbacks['ajaxformhttp'](event)
                )
        self.callbacks['ajaxformerror'] = self.ajax_error
        self.form.addEventListener(
            'ajaxformerror',
            lambda event: self.callbacks['ajaxformerror'](event)
        )

    def form_submit(self, event):
        event.preventDefault()
        test = formSerialize(self.form)
        
        def success(data, status, xhr):
            self.data = data
            self.form.dispatchEvent(__new__(AjaxFormEvent)('ajaxformsuccess', data, xhr))

        def error(xhr, status, error):
            self.form.dispatchEvent(__new__(AjaxFormEvent)('ajaxformerror', error, xhr))
        
        # __pragma__('noalias', 'type')
        # __pragma__('jsiter')
        # __pragma__('jskeys')
        # ajax({
        #     type: self.method, 
        #     url: self.action,
        #     data: test,
        #     contentType: 'application/x-www-form-urlencoded',
        #     beforeSend: lambda xhr, settings: csrfCompat(xhr, settings),
        #     success: success,
        #     error: error,
        # })
        # __pragma__('nojskeys')
        # __pragma__('nojsiter')
        # __pragma__('alias', 'type', 'py_type')   

        __pragma__('js', '{}', """
ajax ({
    type: self.method, 
    url: self.action, 
    data: test, 
    contentType: 'application/x-www-form-urlencoded', 
    beforeSend: (function __lambda__ (xhr, settings) {
        return csrfCompat (xhr, settings);
    }), 
    success: success,
    error: error
});""")

    def on(self, event, callback):
        self.callbacks[event] = callback

    def ajax_success(self, event):
        if event.data.status:
            self.form.dispatchEvent(
                __new__(AjaxFormEvent)('ajaxformjson', event.data, event.xhr))
        
        else:
            self.form.dispatchEvent(
                __new__(AjaxFormEvent)('ajaxformhttp', event.data, event.xhr))
        
    def ajax_error(self, event):
            alert("ajax response error: "+event.data)
    
    def on_json(self, event):
        data = event.data

        if data.HttpResponse:
            if data.status >= 300 and data.status < 400:
                window.location.js_replace(data.HttpResponse)
            
            elif data.status < 500:
                document.open('text/html')
                document.write(data.HttpResponse)
                document.close()

            else:
                print(data.HttpResponse)

    def on_http(self, event):
        if event.xhr.status >= 300 and event.xhr.status < 400:
            window.location.js_replace(event.data)

        else:
            document.open('text/html')
            document.write(event.data)
            document.close()
    
            
__pragma__('js', '{}', """/**
*  
*  
*/""")
# class ScanForm(AjaxForm):
    
#     @property
#     def ajax_success(self, data):
#         if data.HttpResponse:
#             if data.status == 302:
#                 window.location.js_replace(data.HttpResponse)
            
#             elif data.status == 200:
#                 document.open('text/html')
#                 document.write(data.HttpResponse)
#                 document.close()
        
#         elif data.html:
#             elem = document.getElementById('scan-rows')
#             elem.innerHTML = data.html + elem.innerHTML

#         handleMessages(data)
