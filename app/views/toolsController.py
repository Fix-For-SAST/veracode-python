# toolsController.py deals with the 'Tools' page and calls the tool functions used in the page
import logging
import subprocess
import os
import shlex
from html import escape

from django.shortcuts import render
from app.fortune.fortuneData import FortuneData, RiddleData



logger = logging.getLogger("VeraDemo:toolsController")

# Redirects request based on type
def tools(request):
    if(request.method == "GET"):
        return showTools(request)
    elif(request.method == "POST"):
        return processTools(request)

# Loads the tool webpage    
def showTools(request):
    request.host = ""
    return render(request, 'app/tools.html', {})

# Performs the actions on the tool page, updating output accordingly
def processTools(request):
    host = request.POST.get('host')
    fortunefile = request.POST.get('fortunefile')
    request.file = fortune(fortunefile) if fortunefile else ""
    safe_host = escape(host) if host else ""
    request.host = safe_host
    request.ping = ping(host) if host else ""
    
    

    return render(request, 'app/tools.html', {"host" : safe_host})

# pings selected host and outputs the result
def ping(host):
    output = ""
    # Validate host input - only allow alphanumeric, dots, and hyphens
    import re
    if not re.match(r'^[a-zA-Z0-9.-]+$', host):
        logger.error(f"Invalid host format: {host}")
        return "ping: invalid host format"

    logger.info("Pinging " + host)
    try:
        result = subprocess.run(['ping', '-c', '1', host],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               timeout=5,
                               check=False,
                               shell=False)
        
        output = result.stdout.decode() if result.stdout else ""
        logger.info(output)
        logger.info("Exit Code:", result.returncode)
    except subprocess.TimeoutExpired:
        logger.error("Ping timed out")
        output = "ping: unknown host " + host
    except Exception as e:  
        logger.error("Error", e)
        output = "ping: unknown host " + host

    return output


# Produces a fortune based on the submitted selection
def fortune(file):
    # Allow-list validation for safe file access
    SAFE_FILES = {'fortunes', 'riddles'}
    if file not in SAFE_FILES:
        logger.error(f"File not allowed: {file}")
        return "Error: File not allowed"

    if file=='fortunes':
        return FortuneData()
    elif file == 'riddles':
        return RiddleData()
    else:
        # This should never be reached due to allow-list above
        logger.error(f"Unexpected file: {file}")
        return "Error: File not allowed"
   
        




   