# Scribe
Automatically create pages and upload images to a conflunce page.

## Setup
1. Copy `settings.py-dist` to `settings.py` and fill out the settings.
2. Run `./scribe.py` to start the server.

## How it works
* Watch a directory for new image files
* Find the Confluence page for the current Sprint based on date
* Find the page for the current day in the sprint(Design Day ?), or create it if it doesn't exist
* Attach the image to the page
* Edit the page to embed the attachment with a thumbnail

### Assumptions
In confluence, it is assumed that you have a master page that holds all of your sprints.  Each sprint is assumed to be 2 weeks long, and starts on a configurable date.

Each sprint will have its own page, named "Sprint #".  Somewhere on this page should be a link to all subpages.

Each day in a sprint will have its own page that contains uploaded images, for example of a design drawn on a whiteboard.  This program than takes those images, and creates the correct pages in Confluence and uploads them.

The hierarchy ends up looking something like this:

    Sprints
    |________Sprint 1
    |        |--------Design Day 1(Monday 1/1/2013)    - Contains uploaded pictures
    |        |--------Design Day 2(Tuesday 1/2/2013)   - Contains uploaded pictures
    |        |--------Design Day 3(Wednesday 1/3/2013) - Contains uploaded pictures
    |________Sprint 2
             |--------Design Day 1(Monday 2/1/2013)
             |--------Design Day 2(Tuesday 2/2/2013)
             |--------Design Day 3(Wednesday 2/3/2013)

## License
License under the MIT License. See `LICENSE` for details.
