# Copyright (c) 2023 Zeeland
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright Owner: Zeeland
# GitHub Link: https://github.com/Undertone0809/
# Project Link: https://github.com/Undertone0809/cushy-socket
# Contact Email: zeeland@foxmail.com

import unittest
from unittest.mock import patch, MagicMock
from cushy_socket.tcp import CushyTCPClient

class TestCSTCPClient(unittest.TestCase):
    @patch('cushy_socket.tcp.socket.socket')
    def test_run(self, mock_socket):
        # Test CushyTCPClient run method
        mock_socket.return_value.recv.return_value = b"Hello from server"
        cushy_tcp_client = CushyTCPClient(host='localhost', port=7777)

        with patch('cushy_socket.tcp.ThreadPoolExecutor'):
            cushy_tcp_client.run()
            mock_socket.return_value.connect.assert_called_with(('localhost', 7777))

    @patch('cushy_socket.tcp.socket.socket')
    def test_send(self, mock_socket):
        # Test CushyTCPClient send method
        mock_socket.return_value.recv.return_value = b"Hello from server"
        cushy_tcp_client = CushyTCPClient(host='localhost', port=7777)

        with patch('cushy_socket.tcp.ThreadPoolExecutor'):
            cushy_tcp_client.run()
            cushy_tcp_client.socket.sendall.assert_called_with(b"Hello, World")

    def test_listen_decorator(self):
        # Test CushyTCPClient listen decorator
        cushy_tcp_client = CushyTCPClient(host='localhost', port=7777)
        cushy_tcp_client.run()

        @cushy_tcp_client.on_listen()
        def callback(msg):
            self.assertEqual(msg, "Hello from server")

        cushy_tcp_client.socket.recv.return_value = b"Hello from server"
        callback.assert_called_once()

    def test_listen_function(self):
        # Test CushyTCPClient listen function
        cushy_tcp_client = CushyTCPClient(host='localhost', port=7777)
        cushy_tcp_client.run()

        def callback(msg):
            self.assertEqual(msg, "Hello from server")

        cushy_tcp_client.listen(callback)
        cushy_tcp_client.socket.recv.return_value = b"Hello from server"
        callback.assert_called_once()

if __name__ == '__main__':
    unittest.main()
