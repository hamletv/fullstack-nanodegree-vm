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

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]  # split url by / grab id number
                restaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()  # get resto name from db query of id = restaurantIDPath
                if restaurantQuery:     # restaurant found
                    self.send_response(200)     # ok headers started
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = "<html><body>"     # start rendering page
                    output += "<h1>%s</h1>" % restaurantQuery.name
                    output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurants/%s/edit'>" % restaurantIDPath
                    output += "<input name = 'newRestaurantName' type = 'text' placeholder = '%s'>" % restaurantQuery.name
                    output += "<input type = 'submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)

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
                    output += "<a href = '/restaurants/%s/edit'>Edit</a></br>" % restaurant.id
                    output += "<a href = '#'>Delete</a></br>"

                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<a href = '/restaurants'>Return to restaurants listings</a>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Enter new restaurant name below</h2>"
                output += "<input name='newRestaurantName' type='text' placeholder = 'New Restaurant'>"
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
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
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':      # grab input from the form
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    restaurantQuery = session.query(Restaurant).filter_by(
                        id =  restaurantIDPath).one()
                    if restaurantQuery != []:
                        restaurantQuery.name = messagecontent[0]
                        session.add(restaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')    # redirect to send to restaurant listings page
                        self.end_headers()

            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                newRestaurant = Restaurant(name = messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')    # redirect to send to restaurant listings page
                self.end_headers()

            '''ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = ""
            output += "<html><body>"
            output += "<h2>Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>"
            output += "</body></html>"
            self.wfile.write(output)
            print output'''

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
