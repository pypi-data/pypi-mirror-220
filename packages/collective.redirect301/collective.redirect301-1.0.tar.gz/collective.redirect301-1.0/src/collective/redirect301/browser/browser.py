from plone.app.redirector.browser import FourOhFourView as OriginalFourOhFourView
from zope.component import queryUtility
from plone.app.redirector.interfaces import IRedirectionStorage
from six.moves import urllib
from six.moves.urllib.parse import unquote
from six.moves.urllib.parse import quote


class FourOhFourView(OriginalFourOhFourView):
    def attempt_redirect(self):

        url = self._url()
        if not url:
            return False

        try:
            old_path_elements = self.request.physicalPathFromURL(url)
        except ValueError:
            return False

        storage = queryUtility(IRedirectionStorage)
        if storage is None:
            return False

        old_path = "/".join(old_path_elements)

        # First lets try with query string in cases or content migration

        new_path = None

        query_string = self.request.QUERY_STRING
        if query_string:
            new_path = storage.get("%s?%s" % (old_path, query_string))
            # if we matched on the query_string we don't want to include it
            # in redirect
            if new_path:
                query_string = ""

        if not new_path:
            new_path = storage.get(old_path)

        if not new_path:
            new_path = self.find_redirect_if_view(old_path_elements, storage)

        if not new_path:
            new_path = self.find_redirect_if_template(url, old_path_elements, storage)

        if not new_path:
            return False

        url = urllib.parse.urlsplit(new_path)
        if url.netloc:
            # External URL
            # avoid double quoting
            url_path = unquote(url.path)
            url_path = quote(url_path)
            url = urllib.parse.SplitResult(*(url[:2] + (url_path,) + url[3:])).geturl()
        else:
            url = self.request.physicalPathToURL(new_path)

        # some analytics programs might use this info to track
        if query_string:
            url += "?" + query_string

        # Answer GET requests with 302 (Found). Every other method will be answered
        # with 307 (Temporary Redirect), which instructs the client to NOT
        # switch the method (if the original request was a POST, it should
        # re-POST to the new URL from the Location header).
        if self.request.method.upper() == "GET":
            status = 301
        else:
            status = 308

        self.request.response.redirect(url, status=status, lock=1)
        return True
