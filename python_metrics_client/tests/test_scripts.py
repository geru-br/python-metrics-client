# -*- coding: utf-8 -*-
import mock
from click.testing import CliRunner
from python_metrics_client.tests.base import TestCase
from python_metrics_client.scripts.grafana import influx_send_data, tasks_send_data


class ScriptsTest(TestCase):

    @mock.patch('python_metrics_client.influx.requests')
    def test_influx_send_data(self, requests_mock):

        mocked_response = mock.Mock()
        requests_mock.post.return_value = mocked_response
        mocked_response.status_code = 204

        runner = CliRunner()

        response = runner.invoke(influx_send_data, ['url', 'measurement', '{"tag":"value"}', '2', '-t 1490223248024070912'])

        self.assertEquals(response.exit_code, 0)
        self.assertEquals(1, requests_mock.post.call_count)
        requests_mock.post.assert_called_with('url', data='measurement,tag=value value=2 1490223248024070912', timeout=30)

    @mock.patch('python_metrics_client.tasks.send_data')
    def test_tasks_send_data(self, send_data_mock):

        runner = CliRunner()
        response = runner.invoke(tasks_send_data, ['measurement', '{"tag":"value"}', '2', '-t 1490223248024070912'])

        self.assertEquals(response.exit_code, 0)
        self.assertEquals(1, send_data_mock.delay.call_count)
        send_data_mock.delay.assert_called_with(u'measurement', {u'tag': u'value'}, u'2')
