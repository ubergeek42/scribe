#!/usr/bin/env python
import datetime
import os
import shutil
import sys
import xmlrpclib
import time

import argh
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Add current directory to path so we can import settings.
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import settings


__version__ = '0.1'


def upload(parent_name, page_name, image_path):
    """
    Uploads an image to the confluence wiki page 'page_name' as an attachment,
    and inserts a link + a thumbnail at the end of the wiki page content. It
    also sets the parent page to parent_name.
    """
    filename = os.path.basename(image_path)

    # Login to the server
    server = xmlrpclib.ServerProxy(settings.SERVER)
    token = server.confluence2.login(settings.USERNAME, settings.PASSWORD)

    # Get the parent page(we need the numeric ID from it)
    try:
        sprint_page = server.confluence2.getPage(token, settings.SPACE,
                                                 parent_name)
    except:
        # create the page if it didn't exist
        sprint_parent = server.confluence2.getPage(token, settings.SPACE,
                                                   settings.PARENT_PAGE)
        sprint_page = {}
        sprint_page['parentId'] = sprint_parent['id']
        sprint_page['title'] = parent_name
        sprint_page['space'] = settings.SPACE
        sprint_page['content'] = """
        <h3>Design :</h3>
        <p>
          <ac:macro ac:name="children">
            <ac:parameter ac:name="depth">1</ac:parameter>
          </ac:macro>
        </p>
        """
        sprint_page = server.confluence2.storePage(token, sprint_page)

    # Try to get the page, but if it fails, that's ok, we'll create a new one
    try:
        image_page = server.confluence2.getPage(token, settings.SPACE,
                                                page_name)
    except:
        image_page = {}

    # Set all the page attributes
    image_page['space'] = settings.SPACE
    image_page['title'] = page_name
    image_page['parentId'] = sprint_page['id']
    if 'content' not in image_page:
        image_page['content'] = ''

    # Append the proper formatted text to the wiki page to add the file we are
    # about to upload.
    image_page['content'] += """
      <p>
        <ac:link><ri:attachment ri:filename="{filename}" /></ac:link>
      </p>
      <p>
        <ac:image ac:thumbnail="true" ac:width="300">
          <ri:attachment ri:filename="{filename}" />
        </ac:image>
      </p>
    """.format(filename=filename)

    # Create or update the page that holds the images
    image_page = server.confluence2.storePage(token, image_page)

    # Upload the image as an attachment to the page
    attachment = {}
    with open(image_path, 'rb') as handle:
        image_data = xmlrpclib.Binary(handle.read())

    attachment['comment'] = filename
    attachment['fileName'] = filename
    attachment['contentType'] = 'image/jpeg'
    attachment['pageId'] = image_page['id']

    # actually make the call to upload the iamge
    server.confluence2.addAttachment(token, image_page['id'], attachment,
                                     image_data)


class PhotoEventHandler(FileSystemEventHandler):
    """
    Searches for photos in a certain folder structure and triggers processing
    on them.
    """
    def dispatch(self, event):
        # Only handle file creation events.
        if event.event_type != 'created':
            return

        filename = os.path.basename(event.src_path)
        directory_name = os.path.basename(os.path.dirname(event.src_path))
        date = datetime.datetime.strptime(directory_name, '%Y-%m-%d').date()

        # Determine the sprint and page names based on the date.
        difference = date - settings.FIRST_SPRINT_DATE
        sprint_name = 'Sprint {0}'.format(abs(difference.days / 14) + 1)
        page_name = 'Design Day {0} ({1})'.format(
            (difference.days % 14) + 1,
            date.strftime('%A %Y-%m-%d')
        )

        msg = 'Uploading photo {filename} for {page_name} in {sprint_name}...'
        print msg.format(filename=event.src_path, page_name=page_name,
                         sprint_name=sprint_name)
        upload(sprint_name, page_name, event.src_path)
        print 'Done'

        # Copy file to archive and delete the existing file.
        dest_dir = os.path.join(settings.ARCHIVE_DIRECTORY, directory_name)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        shutil.move(event.src_path, os.path.join(dest_dir, filename))


def main():
    """Start monitoring a directory for incoming photos."""
    handler = PhotoEventHandler()
    observer = Observer()
    observer.schedule(handler, path=settings.PHOTO_DIRECTORY, recursive=True)

    print 'Monitoring `{0}`...'.format(settings.PHOTO_DIRECTORY)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


argh.dispatch_command(main)
