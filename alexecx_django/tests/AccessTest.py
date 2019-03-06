from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import (Client,  # Permet d'initialiser la base de donnée 1 fois; et rollback après chaque tests.; Rollback seulement à la fin de la série de tests; Pour des tests n'utilisant pas la bd
                         SimpleTestCase, TestCase, TransactionTestCase)
from django.test.utils import override_settings
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

User = get_user_model()

def add_session(request, session=None):
    # adding session
    if session:
        request.session = session
    else:
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
    
def add_messages(request, messages=None):
    # adding messages
    if messages:
        setattr(request, '_messages', messages)
    else:
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
    
# Create your tests here.
class AccessHelper:

    class AccessHelperException(Exception):
        pass

    def __init__(self, tester=None, *args, **kwargs):
        self.tester = tester if tester else SimpleTestCase()

    def assert_login_redirect(self, client:Client, url:str, **kwargs):
        # follow=True pour qu'il garde une liste de tuple contenant les
        # redirection. 
        # ex. response.redirect_chain == [ ("http://url.com/this", 302) ]
        url = self._reverse(url, **kwargs)
        response = self._url_call(client, url, **kwargs)

        self.tester.assertRedirects(
                        response, 
                        expected_url="/signin/?next={}".format(url), 
                        status_code=302, target_status_code=200, 
                        fetch_redirect_response=True,
                        msg_prefix="{} client".format(auth.get_user(client))
                        )

        # self.tester.assertGreater(len(response.redirect_chain), 0,
        #                 msg="There should be a redirection")

        # self.tester.assertEqual(len(response.redirect_chain), 1,
        #                 msg="There should be only 1 redirection")

        # self.tester.assertEqual(response.status_code, 200,
        #                 msg="Problem accessing login page")

        # self.tester.assertEqual("/signin/" in response.request['PATH_INFO'], True,
        #                 msg="Problem accessing login page")

    def assert_has_access(self, client:Client, url:str, **kwargs): 
        """Vérifie qu'un client à un accès, sans redirection, à un url
        
        Args:
            client (Client): Un objet django.test.Client
            url (str): string au format "mon/url/" ou "app:view_name"
        
        Kwargs:
            method (str): La méthode de request à employer (GET default)
            url_args (list): Liste d'args pour reverse(url)
            url_kwargs (dict): Kwargs pour reverse(url)
            data (dict): Arguments pour la request http
            follow (bool): Si True, suivra les redirections
        """
        url = self._reverse(url, **kwargs)
        response = self._url_call(client, url, **kwargs)

        self.tester.assertEqual(response.status_code, 200,
                            msg="Problem accessing page")

        self.tester.assertEqual(response.request["PATH_INFO"], url,
                            msg="Problem accessing page")

    def assert_redirect(self, client:Client, url:str, **kwargs):
        url = self._reverse(url, **kwargs)
        response = self._url_call(client, url, **kwargs)

        if kwargs.get("expected_url"):
            self.tester.assertRedirects(response, 
                                    expected_url=kwargs.get("expected_url"), 
                                    status_code=302,
                                    fetch_redirect_response=False,
                                    )
        else:
            self.tester.assertEqual(response.status_code, 302,
                             msg="Problem redirecting")
            self.tester.assertEqual(response.request["PATH_INFO"], url,
                                msg="Wrong redirect")

    def assert_logged_in(self, client:Client):
        user = auth.get_user(client)
        self.tester.assertEqual(user.is_authenticated, True, 
                            msg="user={}".format(user))

    # def assert_member_only(self, client:Client, url:str):
    #     with self.tester.subTest("anonymous access to {}".format(url)):
    #         client = test_obj.anon_client
    #         self.assert_login_redirect(client, url)

    #     with self.tester.subTest("member access to {}".format(url)):
    #         client = test_obj.user_client
    #         self.assert_has_access(test_obj.client, url)

    # def assert_restricted_page(self, client:Client, url:str, denied=True):
    #     user = auth.get_user(client)
    #     with self.tester.subTest("{} access to {}".format(user,url)):
    #         if denied:
    #             self.assert_login_redirect(client, url)
    #         else:
    #             self.assert_has_access(client, url)

    # def assert_scanneur_only(self, client:Client, url:str):
    #     with self.tester.subTest("anonymous access to {}".format(url)):
    #         client = test_obj.anon_client
    #         self.assert_login_redirect(client, url)

    #     with self.tester.subTest("member access to {}".format(url)):
    #         client = test_obj.user_client
    #         self.assert_login_redirect(client, url)

    #     with self.tester.subTest("scanneur access to {}".format(url)):
    #         client = test_obj.scanneur_client
    #         self.assert_has_access(client, url)

    def _reverse(self, url, **kwargs):
        try:
            url = reverse(url, args=kwargs.get("url_args", []), 
                          kwargs=kwargs.get("url_kwargs", None))
        except NoReverseMatch:
            pass
        
        return url

    def _url_call(self, client, url, **kwargs):
        method = kwargs.get("method", "get")
        data = kwargs.get("data")
        follow = kwargs.get("follow", False)
        
        if method == "get" or method == "GET":
            response = client.get(url, data, follow=follow)
        elif method == "post" or method == "POST":
            response = client.post(url, data, follow=follow)
        else:
            raise self.AccessHelperException(
                             "{} request method not supported".format(method)
                            )
        return response

#@override_settings(DEBUG=True)

