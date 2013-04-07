from flask import render_template


class BaseLevel(object):
    
    name = ''
    
    template = ''
    
    def process(self, request):
        return {}
    
    def render(self, request):
        context = self.process(request)
        response_body = render_template(self.template, **context)
        return response_body, 200, {'X-XSS-Protection': '0'}


class ReflectedXSSForm(BaseLevel):
    
    name = 'Reflected XSS in an HTML Form'
    
    template = 'xss.html'


class ReflectedXSSAttr(BaseLevel):
    
    name = 'Reflected XSS on an HTML Attribute'
    
    template = 'xss-attr.html'


class ReflectedXSSQueryParam(BaseLevel):
    
    name = 'Reflected XSS in a Query Parameter'
    
    template = 'xss-query.html'
    
    def process(self, request):
        return {'name': request.args.get('name', '')}
    

# An index of available levels.
LEVELS = [
    ReflectedXSSForm(),
    ReflectedXSSAttr(),
    ReflectedXSSQueryParam(),
]
