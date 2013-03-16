import os
import sys
import xmlrpclib

# Add current directory to path so we can import settings.
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import settings

__version__ = '0.1'


# Uploads an image to a given pageName
def upload(parentPageName, pageName, imagepath):
    """
    Uploads an image to the confluence wiki page 'pageName' as an attachment, and inserts
    a link + a thumbnail at the end of the wiki page content.  It also sets the parent page
    to parentPageName.
    """

    filename = os.path.basename(imagepath)

    # Login to the server
    server = xmlrpclib.ServerProxy(settings.SERVER)
    token = server.confluence2.login(settings.USERNAME, settings.PASSWORD)

    # Get the parent page(we need the numeric ID from it)
    sprintPage = server.confluence2.getPage(token, settings.SPACE, parentPageName)

    # Try to get the page, but if it fails, that's ok, we'll create a new one
    try:
        imagePage = server.confluence2.getPage(token,settings.SPACE, pageName)
    except:
        imagePage = {}

    # Set all the page attributes
    imagePage['space'] = settings.SPACE
    imagePage['title'] = pageName
    imagePage['parentId'] = sprintPage['id']
    if 'content' not in imagePage:
        imagePage['content'] = ""

    # Append the proper formatted text to the wiki page to add the file we are about to upload
    imageContent = "<p><ac:link><ri:attachment ri:filename=\"%s\" /></ac:link></p>" % filename
    imageContent += "<p><ac:image ac:thumbnail=\"true\" ac:width=\"300\"><ri:attachment ri:filename=\"%s\" /></ac:image></p>" % filename
    imagePage['content'] += imageContent

    # Create or update the page that holds the images
    imagePage = server.confluence2.storePage(token, imagePage)

    # Upload the image as an attachment to the page
    attachment = {}
    with open(imagepath, "rb") as handle:
        ba = xmlrpclib.Binary(handle.read())

    attachment['comment'] = filename
    attachment['fileName'] = filename
    attachment['contentType'] = "image/jpeg"
    attachment['pageId'] = imagePage['id']

    # actually make the call to upload the iamge
    server.confluence2.addAttachment(token, imagePage['id'], attachment, ba)

# Sample call:
# upload("Sprint 1", "Design Day 1", "/path/to/some/jpeg/2013-02-05_09-59-54_241.jpg")