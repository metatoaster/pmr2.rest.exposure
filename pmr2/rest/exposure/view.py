import json
import zope.component
from zope.publisher.browser import BrowserView

from Products.CMFCore.utils import getToolByName
from pmr2.rest.workspace.base import BaseJsonView
from pmr2.app.exposure.interfaces import IExposureSourceAdapter


class ExposureJsonView(BaseJsonView):
    """\
    Exposure views.
    """

    def contents(self):
        # XXX figure out how to simplify this
        catalog = getToolByName(self.context, 'portal_catalog')

        query = {
            'portal_type': 'ExposureFile',
            'path': [
                u'/'.join(self.context.getPhysicalPath()),
            ],
            'sort_on': 'sortable_title',
        }
        results = catalog(**query)

        keys = ['Title', 'URI']
        values = ([(i.Title, i.getURL(),) for i in results])
        result = {
            'keys': keys,
            'values': values,
        }
        return self.dumps(result)

    def info(self):
        helper = zope.component.queryAdapter(self.context,
            IExposureSourceAdapter)
        if not helper:
            # XXX exception of some sort
            return False
        exposure, workspace, path = helper.source()
        keys = ('title', 'workspace', 'commit_id',)
        title = self.context.title
        workspace = workspace.absolute_url()
        node = self.context.commit_id

        values = (title, workspace, node,)
        result = dict(zip(keys, values))
        return self.dumps(result)