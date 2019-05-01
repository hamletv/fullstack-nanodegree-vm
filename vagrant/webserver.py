from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# CRUD operations imports needed.
from database_setup import Restaurant, Base, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# handler class
class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html></body>"
                output += "<h1><a href = '/restaurants/new'>Add a new restaurant here</a></h1>"
                restaurants = session.query(Restaurant).all()
                for restaurant in restaurants:
                    output += "<li>%s</li>" % restaurant.name
                    output += "<a href = '#'>Edit</a></br>"
                    output += "<a href = '#'>Delete</a></br>"

                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html></body>"
                output += "<a href = '/restaurants'>Return to restaurants listings</a>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Enter new restaurant name below</h2><input name="newRestaurantName" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = ""
            output += "<html><body>"
            output += "<h2>Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += '''<form method = 'POST' enctype = 'multipart/form-data' action = '/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            print output

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')

            output = ""
            output += "<html><body>"
            output += "<h2>Create your new restaurant</h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += '''<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurants/new'><h2>New restaurant name:</h2><input name="newRestaurantName" type="text" ><input type="submit" value="Create"> </form>'''
            newRestaurant = Restaurant(name = 'messagecontent')
            session.add(newRestaurant)
            session.commit()
            output += "</body></html>"
            self.wfile.write(output)
            print output


        except:
            pass

# main method
def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server."
        server.socket.close()


if __name__ == '__main__':
  main()
