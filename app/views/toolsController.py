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
    
    # Get raw outputs
    file_output = fortune(fortunefile) if fortunefile else ""
    ping_output = ping(host) if host else ""
    
    # Escape all user-controlled data before setting on request object
    request.file = escape(file_output)
    request.host = escape(host) if host else ""
    request.ping = escape(ping_output)

    return render(request, 'app/tools.html', {})

# pings selected host and outputs the result
def ping(host):
    import re
    output = ""

    # Validate host format: allow only valid IP addresses and hostnames
    # IP address pattern: digits and dots
    # Hostname pattern: alphanumeric, dots, hyphens
    if not re.match(r'^[a-zA-Z0-9.-]+$', host):
        logger.warning(f"Invalid host format: {host}")
        return "Error: Invalid host format"

    # Additional validation: prevent command injection attempts
    if len(host) > 253:  # Max hostname length
        logger.warning(f"Host name too long: {host}")
        return "Error: Host name too long"

    # Use shlex.quote() to safely escape the host parameter
    safe_host = shlex.quote(host)

    logger.info("Pinging " + safe_host)
    try:
        # Use list format with shell=False to prevent command injection
        result = subprocess.run(['ping', '-c', '1', safe_host],
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
    # Allow-list validation: only allow specific safe files
    SAFE_FILES = {'fortunes', 'riddles'}

    if file == 'fortunes':
        return FortuneData()
    elif file == 'riddles':
        return RiddleData()
    elif file in SAFE_FILES:
        # This branch handles any additional safe files in the allow-list
        # Use shlex.quote() to safely escape the file parameter
        safe_file = shlex.quote(file)
        try:
            # Use list format with shell=False to prevent command injection
            result = subprocess.run(['cat', safe_file],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   check=False,
                                   shell=False,
                                   timeout=5)
            return result.stdout.decode() if result.stdout else ""
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return "Error reading file"
    else:
        # File not in allow-list
        logger.warning(f"Attempted to access unauthorized file: {file}")
        return "Error: File not allowed"
   
        




   