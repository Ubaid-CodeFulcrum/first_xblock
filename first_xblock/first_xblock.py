"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Integer, Scope, Boolean
import logging

from xblock.fields import Boolean, Integer, Scope

log = logging.getLogger(__name__)

class FirstXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    # count = Integer(
    #     default=0, scope=Scope.user_state,
    #     help="A simple counter, to show something happening",
    # )
    
    upvotes = Integer(help="Number of up votes", default=0,
        scope=Scope.user_state_summary)
    downvotes = Integer(help="Number of down votes", default=0,
        scope=Scope.user_state_summary)
    voted = Boolean(help="Has this student voted?", default=False,
        scope=Scope.user_state)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        # """
        # The primary view of the FirstXBlock, shown to students
        # when viewing courses.
        # """
        # html = self.resource_string("static/html/first_xblock.html")
        # frag = Fragment(html.format(self=self))
        # frag.add_css(self.resource_string("static/css/first_xblock.css"))
        # frag.add_javascript(self.resource_string("static/js/src/first_xblock.js"))
        # frag.initialize_js('FirstXBlock')
        # return frag
        
        """
        Create a fragment used to display the XBlock to a student.
        `context` is a dictionary used to configure the display (unused)

        Returns a `Fragment` object specifying the HTML, CSS, and JavaScript
        to display.
        """

        # Load the HTML fragment from within the package and fill in the template
        html_str = pkg_resources.resource_string(__name__,
                                                 "static/html/first_xblock.html").decode('utf-8')
        frag = Fragment(str(html_str).format(self=self))

        # Load the CSS and JavaScript fragments from within the package
        css_str = pkg_resources.resource_string(__name__,
                                                "static/css/first_xblock.css").decode('utf-8')
        frag.add_css(str(css_str))

        js_str = pkg_resources.resource_string(__name__,
                                               "static/js/src/first_xblock.js").decode('utf-8')
        frag.add_javascript(str(js_str))

        frag.initialize_js('FirstXBlock')
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    # @XBlock.json_handler
    # def increment_count(self, data, suffix=''):
    #     """
    #     An example handler, which increments the data.
    #     """
    #     # Just to show data coming in...
    #     assert data['hello'] == 'world'

    #     self.count += 1
    #     return {"count": self.count}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("FirstXBlock",
             """<first_xblock/>
             """),
            ("Multiple FirstXBlock",
             """<vertical_demo>
                <first_xblock/>
                <first_xblock/>
                <first_xblock/>
                </vertical_demo>
             """),
        ]

    @XBlock.json_handler
    def vote(self, data, suffix=''):  # pylint: disable=unused-argument
        """
        Update the vote count in response to a user action.
        """
        # Here is where we would prevent a student from voting twice, but then
        # we couldn't click more than once in the demo!
        #
        #     if self.voted:
        #         log.error("cheater!")
        #         return

        if data['voteType'] not in ('up', 'down'):
            log.error('error!')
            return

        if data['voteType'] == 'up':
            self.upvotes += 1
        else:
            self.downvotes += 1

        self.voted = True

        return {'up': self.upvotes, 'down': self.downvotes}