# modified to handle <pre> and <code>
# original code from https://github.com/matthewwithanm/python-markdownify
from bs4 import BeautifulSoup, NavigableString
import re
import six


convert_heading_re = re.compile(r'convert_h(\d+)')
line_beginning_re = re.compile(r'^', re.MULTILINE)
# whitespace_re = re.compile(r'[\r\n\s\t ]+')
whitespace_re = re.compile(r'[\s\t ]+')


# Heading styles
ATX = 'atx'
ATX_CLOSED = 'atx_closed'
UNDERLINED = 'underlined'
SETEXT = UNDERLINED


def escape(text):
    if not text:
        return ''
    return text.replace('_', r'\_')


def chomp(text):
    """
    If the text in an inline tag like b, a, or em contains a leading or trailing
    space, strip the string and return a space as suffix of prefix, if needed.
    This function is used to prevent conversions like
        <b> foo</b> => ** foo**
    """
    prefix = ' ' if text and text[0] == ' ' else ''
    suffix = ' ' if text and text[-1] == ' ' else ''
    text = text.strip()
    return (prefix, suffix, text)


def _todict(obj):
    return dict((k, getattr(obj, k)) for k in dir(obj) if not k.startswith('_'))


class MarkdownConverter(object):
    class DefaultOptions:
        strip = None
        convert = None
        autolinks = True
        heading_style = UNDERLINED
        bullets = '*+-'  # An iterable of bullet types.

    class Options(DefaultOptions):
        pass

    def __init__(self, **options):
        # Create an options dictionary. Use DefaultOptions as a base so that
        # it doesn't have to be extended.
        self.options = _todict(self.DefaultOptions)
        self.options.update(_todict(self.Options))
        self.options.update(options)
        if self.options['strip'] is not None and self.options['convert'] is not None:
            raise ValueError('You may specify either tags to strip or tags to'
                             ' convert, but not both.')

    def convert(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return self.process_tag(soup, children_only=True)

    def process_tag(self, node, children_only=False):
        text = ''
        # Convert the children first
        for el in node.children:
            if isinstance(el, NavigableString):
                text += self.process_text(el, six.text_type(el))
            else:
                text += self.process_tag(el)

        if not children_only:
            convert_fn = getattr(self, 'convert_%s' % node.name, None)
            if convert_fn and self.should_convert_tag(node.name):
                text = convert_fn(node, text)

        return text

    def process_text(self, el, text):
        if text == '\n':
            return ''
        if el.parent.name == "code":
            return text
        text = escape(whitespace_re.sub(' ', text or ''))
        return text

    def __getattr__(self, attr):
        # Handle headings
        m = convert_heading_re.match(attr)
        if m:
            n = int(m.group(1))

            def convert_tag(el, text):
                return self.convert_hn(n, el, text)

            convert_tag.__name__ = 'convert_h%s' % n
            setattr(self, convert_tag.__name__, convert_tag)
            return convert_tag

        raise AttributeError(attr)

    def should_convert_tag(self, tag):
        tag = tag.lower()
        strip = self.options['strip']
        convert = self.options['convert']
        if strip is not None:
            return tag not in strip
        elif convert is not None:
            return tag in convert
        else:
            return True

    def indent(self, text, level):
        return line_beginning_re.sub('\t' * level, text) if text else ''

    def underline(self, text, pad_char):
        text = (text or '').rstrip()
        return '%s\n%s\n\n' % (text, pad_char * len(text)) if text else ''

    def convert_a(self, el, text):
        prefix, suffix, text = chomp(text)
        if not text:
            return ''
        href = el.get('href')
        title = el.get('title')
        if self.options['autolinks'] and text == href and not title:
            # Shortcut syntax
            return '<%s>' % href
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ''
        return '%s[%s](%s%s)%s' % (prefix, text, href, title_part, suffix) if href else text

    def convert_b(self, el, text):
        return self.convert_strong(el, text)

    def convert_blockquote(self, el, text):
        return '\n' + line_beginning_re.sub('> ', text) if text else ''

    def convert_br(self, el, text):
        return '\n'

    def convert_em(self, el, text):
        if el.parent.name == "code":
            return text
        return self.convert_strong(el, text)

    def convert_code(self, el, text):
        if el.parent.name == "pre":
            return text
        prefix, suffix, atext = chomp(text)
        if not atext:
            return ''
        return '%s`%s`%s' % (prefix, atext, suffix)

    def convert_pre(self, el, text):
        if not text:
            return ''
        return '```\n%s\n```\n' % text.rstrip()

    def convert_samp(self, el, text):
        return self.convert_code(el, text)

    def convert_kbd(self, el, text):
        return self.convert_code(el, text)

    def convert_hn(self, n, el, text):
        style = self.options['heading_style']
        text = text.rstrip()
        if style == UNDERLINED and n <= 2:
            line = '=' if n == 1 else '-'
            return self.underline(text, line)
        hashes = '#' * n
        if style == ATX_CLOSED:
            return '%s %s %s\n\n' % (hashes, text, hashes)
        text = text.strip(' -')
        return '%s %s\n\n' % (hashes, text)

    def convert_i(self, el, text):
        prefix, suffix, text = chomp(text)
        if not text:
            return ''
        return '%s*%s*%s' % (prefix, text, suffix)

    def convert_list(self, el, text):
        nested = False
        while el:
            if el.name == 'li':
                nested = True
                break
            el = el.parent
        if nested:
            # remove trailing newline if nested
            return '\n' + self.indent(text, 1).rstrip()
        return text + '\n'

    convert_ul = convert_list
    convert_ol = convert_list

    def convert_li(self, el, text):
        parent = el.parent
        if parent is not None and parent.name == 'ol':
            if parent.get("start"):
                start = int(parent.get("start"))
            else:
                start = 1
            bullet = '%s.' % (start + parent.index(el))
        else:
            depth = -1
            while el:
                if el.name == 'ul':
                    depth += 1
                el = el.parent
            bullets = self.options['bullets']
            bullet = bullets[depth % len(bullets)]
        return '%s %s\n' % (bullet, text or '')

    def convert_p(self, el, text):
        return '%s\n\n' % text if text else ''

    def convert_strong(self, el, text):
        prefix, suffix, text = chomp(text)
        if not text:
            return ''
        return '%s**%s**%s' % (prefix, text, suffix)

    def convert_img(self, el, text):
        alt = el.attrs.get('alt', None) or ''
        src = el.attrs.get('src', None) or ''
        title = el.attrs.get('title', None) or ''
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ''
        return '![%s](%s%s)' % (alt, src, title_part)


def markdownify(html, **options):
    return MarkdownConverter(**options).convert(html)


def md_header(y, d):
    return f"""# Day {d}
Copyright (c) Eric Wastl
#### [Source](https://adventofcode.com/{y}/day/{d})

## Part 1
"""


def make_md(text):
    text = re.sub(r"(<code>)(<em>)", r"\2\1", text)
    text = re.sub(r"(</em>)(</code>)", r"\2\1", text)
    return markdownify(text, heading_style=ATX)

if __name__ == "__main__":
    with open("day21.html") as f:
        y, d = 2020, 21
        html = f.read()
        start = html.find("<article")
        end = html.rfind("</article>")+len("</article>")
        end_success = html.rfind("<p class=\"day-success\">")
        text = html[start:max(end, end_success)]
        text = make_md(text)
        with open("README.md", "w+") as statement:
            statement.write(md_header(y, d))
            statement.write(text)