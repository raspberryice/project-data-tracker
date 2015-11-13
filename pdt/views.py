from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(req):
	return HttpResponse("""
<html>
<head>
<title>Project Data Tracker</title>
</head>
<body>
<div><h1>Hello World</h1></div><div><h2>This is the Project Data Tracker.</h2></div>
</body>
</html>
""")
