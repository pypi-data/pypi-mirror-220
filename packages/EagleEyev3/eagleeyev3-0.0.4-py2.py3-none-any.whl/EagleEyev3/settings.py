
# Set up your application and get client id/secrete first
# https://developerv3.eagleeyenetworks.com/page/my-application
client_id = ""
client_secret = ""

# you will need to add approved redirect_uris in your application
# this examples assumes you've added http://127.0.0.1:3333/login_callback
# change the following variables if you did something different
# Note: do not use localhost for server_host, use 127.0.0.1 instead
server_protocol = "http"
server_host = "127.0.0.1" 
server_port = "3333"
server_path = "login_callback"
