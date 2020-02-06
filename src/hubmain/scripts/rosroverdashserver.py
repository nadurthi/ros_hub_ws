#! /usr/bin/env python
import rospy
import tornado.ioloop
import tornado.web
import os

wrkdir = os.path.dirname(os.path.abspath(__file__))

with open('/etc/hosts', 'r') as F:
    hosts = F.read()

roshubmainip = filter(lambda x: 'roshubmain' in x, hosts.split('\n'))[0].split(' ')[0]


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        urllinks = [{'ref': self.reverse_url("home"), 'name': 'Main'},
                    {'ref': self.reverse_url("videosrcred"), 'name': 'Video Sources'},
                    {'ref': self.reverse_url("rosparams"), 'name': 'Ros Parameters'},
                    {'ref': self.reverse_url("rostopics"), 'name': 'Ros Topics'},
                    {'ref': self.reverse_url("rovercontrol"), 'name': 'Ros Controller'},
                    {'ref': self.reverse_url("backyardpantiltcontrol"),
                     'name': 'Backyard pantilt Controller'}
                    ]
        self.render("roverctrl/templates/mainpage.html",
                    title="Ros Dash", items={'urllinks': urllinks, 'roshubmainip': roshubmainip})


class RosParams(tornado.web.RequestHandler):

    def get(self):
        items = {}
        items['rosparams'] = rospy.get_param_names()
        L = []
        for p in items['rosparams']:
            par = str(rospy.get_param(p))
            tp = "String"
            try:
                float(par)
                tp = "Number"
            except:
                tp = "String"
            L.append([p, str(par), tp])

        items['rosparams'] = L

        # items['rosparams'] = [for p in items['rosparams']]
        # for i in range(len(items['rosparams'])):
        #     paramname = items['rosparams'][i][0]
        #     pp = rospy.get_param(paramname)
        #     items['rosparams'][i][2] = str(pp)

        items['roshubmainip'] = roshubmainip
        self.render("roverctrl/templates/rosparams.html", title="Ros Parameters", items=items)


class RosTopics(tornado.web.RequestHandler):

    def get(self):
        items = {}
        items['rostopics'] = rospy.get_published_topics()
        # for i in range(len(items['rosparams'])):
        #     paramname = items['rosparams'][i][0]
        #     pp = rospy.get_param(paramname)
        #     items['rosparams'][i][2] = str(pp)

        # items = list(map(lambda x: x[0], rospy.get_published_topics()))
        items['roshubmainip'] = roshubmainip
        self.render("roverctrl/templates/rostopics.html", title="Ros Topics", items=items)


class RoverCtrl(tornado.web.RequestHandler):

    def get(self):
        urllinks = [{'ref': self.reverse_url("home"), 'name': 'Main'},
                    {'ref': self.reverse_url("rosparams"), 'name': 'Ros Parameters'}
                    ]
        self.render("roverctrl/templates/roverctrl.html",
                    title="Ros Dash", items={'urllinks': urllinks, 'roshubmainip': roshubmainip})


class backyarkPanTiltCtrl(tornado.web.RequestHandler):

    def get(self):
        urllinks = [{'ref': self.reverse_url("home"), 'name': 'Main'},
                    {'ref': self.reverse_url("rosparams"), 'name': 'Ros Parameters'}
                    ]
        self.render("roverctrl/templates/backyardpantiltctrl.html",
                    title="Ros Dash", items={'urllinks': urllinks, 'roshubmainip': roshubmainip})


class VideoSrcRedirect(tornado.web.RequestHandler):

    def get(self):
        self.render("roverctrl/templates/videosources.html",
                    title="Video src", items={'roshubmainip': roshubmainip})


app = tornado.web.Application([
    tornado.web.url(r"/", MainHandler, name="home"),
    tornado.web.url(r"/home", MainHandler),
    tornado.web.url(r"/rosparams", RosParams, name="rosparams"),
    tornado.web.url(r"/rostopics", RosTopics, name="rostopics"),
    tornado.web.url(r"/roverctrl", RoverCtrl, name="rovercontrol"),
    tornado.web.url(r"/backyardptctrl", backyarkPanTiltCtrl, name="backyardpantiltcontrol"),
    tornado.web.url(r"/videosources", VideoSrcRedirect, name="videosrcred"),


    (r'/static/(.*)', tornado.web.StaticFileHandler,
     {'path': os.path.join(wrkdir, 'roverctrl/static/')}),
    #tornado.web.url(r"/story/([0-9]+)", RosParams, dict(db='ok'), name="story")
])

if __name__ == "__main__":
    # app = make_app()
    app.listen(8118)
    tornado.ioloop.IOLoop.current().start()
