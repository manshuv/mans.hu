#!/usr/bin/env python3
"""Generate a deterministic summary RSS feed from dated posts (standard library only)."""
from datetime import datetime, timezone
from email.utils import format_datetime
from html.parser import HTMLParser
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
BASE = 'https://manshuverma.com'

class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ''
        self.description = ''
        self.in_title = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'title': self.in_title = True
        if tag == 'meta' and attrs.get('name') == 'description':
            self.description = attrs.get('content', '')
    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
    def handle_data(self, data):
        if self.in_title: self.title += data

rss = ET.Element('rss', version='2.0')
channel = ET.SubElement(rss, 'channel')
for key, value in [('title', 'Manshu Verma'), ('link', BASE + '/'),
                   ('description', 'New writing and interactive essays by Manshu Verma.'),
                   ('language', 'en')]:
    ET.SubElement(channel, key).text = value
for path in sorted((ROOT / 'posts').glob('*.html'), reverse=True):
    match = re.match(r'^(\d{4}-\d{2}-\d{2})-', path.name)
    if not match: continue
    meta = Metadata()
    meta.feed(path.read_text())
    if not meta.title or not meta.description:
        raise ValueError(f'Missing title or description: {path.name}')
    item = ET.SubElement(channel, 'item')
    title = re.sub(r'\s*[-—]\s*manshuverma\.com$', '', meta.title).strip()
    url = BASE + '/posts/' + path.stem
    ET.SubElement(item, 'title').text = title
    ET.SubElement(item, 'link').text = url
    # Keep this GUID unchanged after publication, even if URLs change.
    ET.SubElement(item, 'guid', isPermaLink='false').text = 'manshuverma:' + path.stem
    ET.SubElement(item, 'pubDate').text = format_datetime(
        datetime.strptime(match[1], '%Y-%m-%d').replace(tzinfo=timezone.utc), usegmt=True)
    ET.SubElement(item, 'description').text = meta.description + ' Read the full article on manshuverma.com.'
ET.indent(rss)
ET.ElementTree(rss).write(ROOT / 'feed.xml', encoding='utf-8', xml_declaration=True)
