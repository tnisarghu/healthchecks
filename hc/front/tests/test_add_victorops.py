from hc.api.models import Channel
from hc.test import BaseTestCase


class AddVictorOpsTestCase(BaseTestCase):
    url = "/integrations/add_victorops/"

    def test_instructions_work(self):
        self.client.login(username="alice@example.org", password="password")
        r = self.client.get(self.url)
        self.assertContains(r, "incident management system")

    def test_it_works(self):
        form = {"value": "http://example.org"}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(self.url, form)
        self.assertRedirects(r, "/integrations/")

        c = Channel.objects.get()
        self.assertEqual(c.kind, "victorops")
        self.assertEqual(c.value, "http://example.org")
        self.assertEqual(c.project, self.project)

    def test_it_rejects_bad_url(self):
        form = {"value": "not an URL"}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(self.url, form)
        self.assertContains(r, "Enter a valid URL")
