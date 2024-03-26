from django.test import TestCase

# Create your tests here.
examples = [
    '<script>alert("XSS")</script>',
    '<img src="x" onerror="alert(\'XSS\')" />',
    '<a href="javascript:alert(\'XSS\')">click me</a>',
    '<?php echo "Hello world"; ?>',
]