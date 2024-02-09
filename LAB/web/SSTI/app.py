import tornado.template
import tornado.ioloop
import tornado.web
TEMPLATE = '''
<html>
 <head><title> Hello {{ name }} </title></head>
 <body> Hello FOO </body>
</html>
'''
class MainHandler(tornado.web.RequestHandler):

    def get(self):
        name = self.get_argument('name', '')
        template_data = TEMPLATE.replace("FOO",name)
        t = tornado.template.Template(template_data)
        self.write(t.generate(name=name))

application = tornado.web.Application([
    (r"/", MainHandler),
], debug=True, static_path=None, template_path=None)

if __name__ == '__main__':
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
