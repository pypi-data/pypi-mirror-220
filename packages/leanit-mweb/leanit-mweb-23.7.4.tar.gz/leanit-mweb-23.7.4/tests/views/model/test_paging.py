import logging
import unittest
from unittest.mock import Mock, patch, MagicMock

from mweb import App
from mweb.orm.fields import IntegerField
from mweb.orm.model import Model
from tests.resources import UNITTEST_APP_ROOT

logger = logging.getLogger(__name__)


class Email(Model):
    _table = "email"
    _pk = ["tenant_id", "id"]

    tenant_id = IntegerField()
    id = IntegerField()


Email._initialize()


class PagingCase(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = App(UNITTEST_APP_ROOT)
        cls.app.setup()

    @patch(f"{__name__}.Email.filter_async")
    @patch("mweb.templates.TemplateResponse")
    async def test_sort_ascending(self, mock_template_response: MagicMock, mock_filter_async: MagicMock):
        from mweb.views.model import ModelView
        class EmailListView(ModelView):
            model = Email
            template_directory = "email"
            list_fields = ["tenant_id", "id"]
            list_order_by = "ASC"
            list_limit = 3

        mock_filter_async.side_effect = [[Email(tenant_id=1, id=1)]]

        request = Mock()
        request.url.path = "/email"
        request.query_params = {}
        request.path_params = {}

        view = EmailListView(request)
        response = await view.render_list()

        render_context = mock_template_response.call_args[0][1]

        self.assertFalse(render_context["pagination"]["has_next"])
        self.assertFalse(render_context["pagination"]["has_previous"])
        self.assertEqual(1, render_context["pagination"]["page"])

        mock_filter_async.side_effect = [
            [Email(tenant_id=1, id=1), Email(tenant_id=1, id=2), Email(tenant_id=1, id=3)],
        ]

        response = await view.render_list()
        render_context = mock_template_response.call_args[0][1]

        self.assertEqual({
            'has_next': True,
            'has_previous': False,
            'next_url': '/email?page=2&page-direction=gt&page-border=tenant_id%2C1%2Cid%2C3',
            'page': 1}, render_context["pagination"])

        # open page 2
        request.query_params = {
            "page": 2,
            "page-direction": "gt",
            "page-border": "tenant_id,1,id,3",
        }
        mock_filter_async.side_effect = [
            [Email(tenant_id=1, id=4), Email(tenant_id=1, id=5), Email(tenant_id=1, id=6)], ]

        response = await view.render_list()
        render_context = mock_template_response.call_args[0][1]

        self.assertEqual({
            'has_next': True,
            'has_previous': True,
            'next_url': '/email?page=3&page-direction=gt&page-border=tenant_id%2C1%2Cid%2C6',
            'page': 2,
            'previous_url': '/email?page=1&page-direction=lt&page-border=tenant_id%2C1%2Cid%2C4'},
            render_context["pagination"])

        # page 3
        request.query_params = {
            "page": 3,
            "page-direction": "gt",
            "page-border": "tenant_id,1,id,6",
        }

        mock_filter_async.side_effect = [
            [Email(tenant_id=1, id=7)]]

        response = await view.render_list()
        render_context = mock_template_response.call_args[0][1]

        self.assertEqual({
            'has_next': False,
            'has_previous': True,
            'page': 3,
            'previous_url': '/email?page=2&page-direction=lt&page-border=tenant_id%2C1%2Cid%2C7'},
            render_context["pagination"])

        self.assertEqual(
            {'_limit': 3, '_only': ['tenant_id', 'id'], '_order_by': 'tenant_id,id', 'tenant_id__gte': '1', 'id__gt': '6'},
            mock_filter_async.call_args.kwargs)

        # go back to page 2
        request.query_params = {
            "page": 2,
            "page-direction": "lt",
            "page-border": "tenant_id,1,id,7",
        }

        mock_filter_async.side_effect = [
            # reverse order because of descending order
            [Email(tenant_id=1, id=6), Email(tenant_id=1, id=5), Email(tenant_id=1, id=4)], ]

        response = await view.render_list()

        # SELECT ... order by ... DESC
        self.assertEqual({
            '_limit': 3,
             '_only': ['tenant_id', 'id'],
             '_order_by': '-tenant_id,-id',
             'id__lt': '7',
             'tenant_id__lte': '1'},
            mock_filter_async.call_args.kwargs)

        render_context = mock_template_response.call_args[0][1]

        # objects are reversed because of descending order -> result should be ascending sort order
        self.assertEqual([4, 5, 6], [obj.id for obj in render_context["object_list"]])



    @patch(f"{__name__}.Email.filter_async")
    @patch("mweb.templates.TemplateResponse")
    async def test_sort_descending(self, mock_template_response: MagicMock, mock_filter_async: MagicMock):
        from mweb.views.model import ModelView
        class EmailListView(ModelView):
            model = Email
            template_directory = "email"
            list_fields = ["tenant_id", "id"]
            list_order_by = "DESC"
            list_limit = 3

        request = Mock()
        request.url.path = "/email"
        request.query_params = {}
        request.path_params = {}

        view = EmailListView(request)

        mock_filter_async.side_effect = [
            # reverse order because of descending order
            [Email(tenant_id=1, id=7), Email(tenant_id=1, id=6), Email(tenant_id=1, id=5)], ]

        response = await view.render_list()

        self.assertEqual({'_limit': 3, '_only': ['tenant_id', 'id'], '_order_by': '-tenant_id,-id'},
            mock_filter_async.call_args.kwargs)

        render_context = mock_template_response.call_args[0][1]

        self.assertEqual([7, 6, 5], [obj.id for obj in render_context["object_list"]])

        self.assertTrue(render_context["pagination"]["has_next"])
        self.assertFalse(render_context["pagination"]["has_previous"])
        self.assertEqual(1, render_context["pagination"]["page"])
        self.assertEqual("/email?page=2&page-direction=lt&page-border=tenant_id%2C1%2Cid%2C5", render_context["pagination"]["next_url"])

        # page 2
        request.query_params = {
            "page": 2,
            "page-direction": "lt",
            "page-border": "tenant_id,1,id,5",
        }

        mock_filter_async.side_effect = [
            # reverse order because of descending order
            [Email(tenant_id=1, id=4), Email(tenant_id=1, id=3), Email(tenant_id=1, id=2)], ]

        response = await view.render_list()
        self.assertEqual({
            '_limit': 3,
             '_only': ['tenant_id', 'id'],
             '_order_by': '-tenant_id,-id',
             'id__lt': '5',
             'tenant_id__lte': '1'},
         mock_filter_async.call_args.kwargs)

        render_context = mock_template_response.call_args[0][1]
        self.assertEqual([4, 3, 2], [obj.id for obj in render_context["object_list"]])

        self.assertEqual({
            'has_next': True,
             'has_previous': True,
             'next_url': '/email?page=3&page-direction=lt&page-border=tenant_id%2C1%2Cid%2C2',
             'page': 2,
             'previous_url': '/email?page=1&page-direction=gt&page-border=tenant_id%2C1%2Cid%2C4'},
            render_context["pagination"])

        # page 3
        request.query_params = {
            "page": 3,
            "page-direction": "lt",
            "page-border": "tenant_id,1,id,2",
        }

        mock_filter_async.side_effect = [
            [Email(tenant_id=1, id=1)], ]

        response = await view.render_list()
        self.assertEqual({
            '_limit': 3,
             '_only': ['tenant_id', 'id'],
             '_order_by': '-tenant_id,-id',
             'id__lt': '2',
             'tenant_id__lte': '1'},
            mock_filter_async.call_args.kwargs)

        render_context = mock_template_response.call_args[0][1]
        self.assertEqual([1], [obj.id for obj in render_context["object_list"]])

        self.assertEqual({
            'has_next': False,
             'has_previous': True,
             'page': 3,
             'previous_url': '/email?page=2&page-direction=gt&page-border=tenant_id%2C1%2Cid%2C1'},
            render_context["pagination"])

        # go back to page 2
        request.query_params = {
            "page": 2,
            "page-direction": "gt",
            "page-border": "tenant_id,1,id,1",
        }

        mock_filter_async.side_effect = [
            [Email(tenant_id=1, id=2), Email(tenant_id=1, id=3), Email(tenant_id=1, id=4)], ]

        response = await view.render_list()

        self.assertEqual({
            '_limit': 3,
             '_only': ['tenant_id', 'id'],
             '_order_by': 'tenant_id,id',
             'id__gt': '1',
             'tenant_id__gte': '1'},
            mock_filter_async.call_args.kwargs)

        render_context = mock_template_response.call_args[0][1]
        self.assertEqual([4, 3, 2], [obj.id for obj in render_context["object_list"]])


if __name__ == '__main__':
    unittest.main()
