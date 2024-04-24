import re

from django.test import TestCase


class XSSRegexTest(TestCase):

    def setUp(self):
        self.positive_cases = [
            '<script>alert("XSS")</script>',
            '<img src="x" onerror="alert(document.cookie)" />',
            '<a href="javascript:alert(document.cookie)">click me</a>',
            '<?php echo "Hello world"; ?>',
            '<iframe src="http://malicious.example.com"></iframe>',
            '<frame src="javascript:alert(document.cookie);"></frame>',
            '<body onload=alert(document.cookie)>',
            '<div style="background-image: url(javascript:alert(document.cookie));">Click here</div>',
            '<table background="javascript:alert(document.cookie);">',
            '<form action="javascript:alert(document.cookie);">',
            '<input type="image" src="javascript:alert(document.cookie);">',
            '<svg/onload=alert(document.cookie)>',
            '<input onfocus=alert(document.domain) autofocus>',
            '<meta http-equiv="refresh" content="0;url=javascript:alert(document.cookie);">',
            '<button onclick="alert(document.cookie)">Click me</button>'
        ]

        self.negative_cases = [
            'Writing href=\"javascript:alert(document.cookie)\" in a text should not trigger the regex',
            'What if I just put in <script> without closing it?',
            'This should not work: src=\"javascript:alert(document.cookie)\"',
            'This should not work either: href=\"javascript:alert(document.cookie)\"',
        ]

        self.xss_pattern = re.compile(
            r'''(?:
            <script.*?>.*?</script>|          # Basic script tags
            <.*?javascript:.*?>|              # Elements with JavaScript protocol
            <.*?on\w+.*?=.*?>|                # HTML elements with event handlers
            <\?.*?\?>|                        # PHP tags
            <.*?src=['"].*?javascript:.*?>|   # Using javascript: protocol in src attribute of tags
            <.*?href=['"].*?javascript:.*?>|  # Using javascript: protocol in href attribute of tags
            <.*?style=['"].*?expression\(.*?\).*?>|  # CSS expression
            <.*?style=['"].*?url\(['"]?javascript:.*?\).*?>| # CSS url() with JavaScript
            <.*?(\bon\w+|style|background|src|href|data|action)=['"]?\s*javascript:.*?>| # Common attributes for inline JavaScript
            <.*?(\bon\w+|style|background|src|href|data|action)=['"]?\s*.*?>| # Common attributes for inline JavaScript wider
            <iframe.*?src=['"].*?>|           # Iframe with src
            <frame.*?src=['"].*?>|            # Frame with src
            <.*?data=['"].*?javascript:.*?>|  # Using javascript: protocol in data attribute
            <.*?background=['"].*?javascript:.*?>| # Using javascript: in background
            <.*?formaction=['"].*?javascript:.*?>  # Using javascript: in formaction
            )''',
            re.IGNORECASE | re.VERBOSE)

    def test_positive_xss_regex(self):
        for case in self.positive_cases:
            self.assertTrue(self.xss_pattern.search(case))

    def test_negative_xss_regex(self):
        for case in self.negative_cases:
            self.assertIsNone(self.xss_pattern.search(case))
