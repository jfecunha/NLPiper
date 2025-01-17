"""Cleaner Module."""

import re
from string import punctuation
from typing import Optional
from unicodedata import normalize, combining

from nlpiper.core import Document
from nlpiper.transformers.base import (
    BaseTransformer,
    TransformersType,
    add_step,
    validate
)
from nlpiper.logger import log


__all__ = [
    "CleanAccents",
    "CleanEmail",
    "CleanEOF",
    "CleanMarkup",
    "CleanNumber",
    "CleanPunctuation",
    "CleanURL",
]


class CleanURL(BaseTransformer):
    """Remove URLs from a document.

    Callable arguments:

    Args:
        doc (Document): document to be cleaned.
        inplace (bool, default False): if False will return a new document object,
                        otherwise will change the object passed as parameter and return None.

    Returns:
        Document without URLs or None if `inplace=True`.

    Example:
        >>> doc = Document("URL: www.web.com")
        >>> cleaner = CleanURL()
        >>> out = cleaner(doc)
        >>> out.cleaned
        "URL: "
    """

    @validate(TransformersType.CLEANERS)
    @add_step
    def __call__(self, doc: Document, inplace: bool = False) -> Optional[Document]:
        """Remove URLs from a document.

        Args:
            doc (Document): document to be cleaned.
            inplace (bool): if False will return a new doc object,
                            otherwise will change the object passed as parameter.

        Returns: Document
        """
        d = doc if inplace else doc._deepcopy()

        d.cleaned = re.sub(r"http\S+", "", d.cleaned)
        d.cleaned = re.sub(r"www\S+", "", d.cleaned)

        return None if inplace else d


class CleanEmail(BaseTransformer):
    """Remove emails from a document.

    Callable arguments:

    Args:
        doc (Document): document to be cleaned.
        inplace (bool, default False): if False will return a new document object,
                        otherwise will change the object passed as parameter and return None.

    Returns:
        Document without emails or None if `inplace=True`.

    Example:
        >>> doc = Document("Email: test@test.com")
        >>> cleaner = CleanEmail()
        >>> out = cleaner(doc)
        >>> out.cleaned
        "Email: "
    """

    @validate(TransformersType.CLEANERS)
    @add_step
    def __call__(self, doc: Document, inplace: bool = False) -> Optional[Document]:
        """Remove emails from a document.

        Args:
            doc (Document): document to be cleaned.
            inplace (bool): if False will return a new doc object,
                            otherwise will change the object passed as parameter.

        Returns: Document
        d = doc if inplace else doc._deepcopy()
        """
        d = doc if inplace else doc._deepcopy()

        d.cleaned = re.sub(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", "", d.cleaned)

        return None if inplace else d


class CleanNumber(BaseTransformer):
    """Remove numbers from a document.

    Callable arguments:

    Args:
        doc (Document): document to be cleaned.
        inplace (bool, default False): if False will return a new document object,
                        otherwise will change the object passed as parameter and return None.

    Returns:
        Document without numbers or None if `inplace=True`.

    Example:
        >>> doc = Document("Number 12")
        >>> cleaner = CleanNumber()
        >>> out = cleaner(doc)
        >>> out.cleaned
        "Number "
    """

    @validate(TransformersType.CLEANERS)
    @add_step
    def __call__(self, doc: Document, inplace: bool = False) -> Optional[Document]:
        """Remove numbers from a document.

        Args:
            doc (Document): document to be cleaned.
            inplace (bool): if False will return a new doc object,
                            otherwise will change the object passed as parameter.

        Returns: Document
        """
        d = doc if inplace else doc._deepcopy()

        d.cleaned = re.sub(r'[0-9]+', '', d.cleaned)

        return None if inplace else d


class CleanPunctuation(BaseTransformer):
    """Remove punctuation from a document.

    Callable arguments:

    Args:
        doc (Document): document to be cleaned.
        inplace (bool, default False): if False will return a new document object,
                        otherwise will change the object passed as parameter and return None.

    Returns:
        Document without punctuation or None if `inplace=True`.

    Example:
        >>> doc = Document("Document without punctuation!")
        >>> cleaner = CleanPunctuation()
        >>> out = cleaner(doc)
        >>> out.cleaned
        "Document without punctuation"
    """

    @validate(TransformersType.CLEANERS)
    @add_step
    def __call__(self, doc: Document, inplace: bool = False) -> Optional[Document]:
        """Remove punctuation from a document.

        Args:
            doc (Document): document to be cleaned.
            inplace (bool): if False will return a new doc object,
                            otherwise will change the object passed as parameter.

        Returns: Document
        """
        d = doc if inplace else doc._deepcopy()

        d.cleaned = d.cleaned.translate(str.maketrans('', '', punctuation))

        return None if inplace else d


class CleanEOF(BaseTransformer):
    """Remove end of line from a document.

    Callable arguments:

    Args:
        doc (Document): document to be cleaned.
        inplace (bool, default False): if False will return a new document object,
                        otherwise will change the object passed as parameter and return None.

    Returns:
        Document without end of line or None if `inplace=True`.

    Example:
        >>> doc = Document("Line 1\\nLine 2")
        >>> cleaner = CleanEOF()
        >>> out = cleaner(doc)
        >>> out.cleaned
        "Line 1 Line 2"
    """

    @validate(TransformersType.CLEANERS)
    @add_step
    def __call__(self, doc: Document, inplace: bool = False) -> Optional[Document]:
        """Remove end of line from a document.

        Args:
            doc (Document): document to be cleaned.
            inplace (bool): if False will return a new doc object,
                            otherwise will change the object passed as parameter.

        Returns: Document
        """
        d = doc if inplace else doc._deepcopy()

        d.cleaned = d.cleaned.translate(str.maketrans('\n', ' '))

        return None if inplace else d


class CleanMarkup(BaseTransformer):
    """Remove HTML and XML from a document using BeautifulSoup4 package.

    Callable arguments:

    Args:
        doc (Document): document to be cleaned.
        inplace (bool, default False): if False will return a new document object,
                        otherwise will change the object passed as parameter and return None.

    Returns:
        Document without HTML and XML or None if `inplace=True`.

    Example:
        >>> doc = Document("<html><title>Title 1</title>")
        >>> cleaner = CleanMarkup()
        >>> out = cleaner(doc)
        >>> out.cleaned
        "Title 1"
    """

    def __init__(self, features: str = "html.parser", *args, **kwargs):
        """Remove HTML and XML.

        Args:
            features (str, default `html.parser`): Parser used to remove HTML and XML, which could be used
                the following parsers: ``"html.parser"``, ``"lxml"``, ``"lxml-xml"``, ``"xml"``,  ``"html5lib"``.
                For more information about the parser
                go to
                `BeautifulSoup4 parsers documentation
                <https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser>`_.
            *args: See the docs at https://www.crummy.com/software/BeautifulSoup/bs4/doc/ for more information.
            **kwargs: See the docs at https://www.crummy.com/software/BeautifulSoup/bs4/doc/ for more information.
        """
        super().__init__(features=features, *args, **kwargs)
        try:
            from bs4 import BeautifulSoup
            self.c = BeautifulSoup
            self.args = args
            self.kwargs = kwargs
            self.features = features

        except ImportError:
            log.error("Please install BeautifulSoup4. "
                      "See the docs at https://www.crummy.com/software/BeautifulSoup/ for more information.")
            raise

    @validate(TransformersType.CLEANERS)
    @add_step
    def __call__(self, doc: Document, inplace: bool = False) -> Optional[Document]:
        """Remove HTML and XML from the document.

        Args:
            doc (Document): document to be cleaned.
            inplace (bool): if False will return a new doc object,
                            otherwise will change the object passed as parameter.

        Returns: Document
        """
        d = doc if inplace else doc._deepcopy()

        d.cleaned = self.c(d.cleaned, features=self.features, *self.args, **self.kwargs).get_text(" ")

        return None if inplace else d


class CleanAccents(BaseTransformer):
    """Strip accents and perform character normalization from a document.

    Callable arguments:

    Args:
        doc (Document): document to be cleaned.
        inplace (bool, default False): if False will return a new document object,
                        otherwise will change the object passed as parameter and return None.

    Returns:
        Document without accents or None if `inplace=True`.

    Example:
        >>> doc = Document("This is à test")
        >>> cleaner = CleanAccents()
        >>> out = cleaner(doc)
        >>> out.cleaned
        "This is a test"
    """

    def __init__(self, mode: str = "unicode"):
        """Strip accents and perform character normalization from a document.

        Args:
            mode (str, default `unicode`): Available methods: `ascii` and `unicode`. The first method is faster
                                           and only works for characters that have an direct ASCII mapping.
                                           The second is sightly slower but works in any characters.

        Warning: mode `ascii` is only suited for languages that have a direct transliteration to ASCII symbols.
        """
        if mode not in ('unicode', 'ascii'):
            raise ValueError(f"{mode} is not implemented. The only available modes are: 'unicode' and 'ascii'.")

        super().__init__(mode=mode)
        self.mode = mode

    @validate(TransformersType.CLEANERS)
    @add_step
    def __call__(self, doc: Document, inplace: bool = False) -> Optional[Document]:
        """Strip accents and perform character normalization from the document.

        Args:
            doc (Document): document to be cleaned.
            inplace (bool): if False will return a new doc object,
                            otherwise will change the object passed as parameter.

        Returns: Document
        """
        d = doc if inplace else doc._deepcopy()

        d.cleaned = (self._strip_accents_unicode(d.cleaned) if self.mode == 'unicode'
                     else self._strip_accents_ascii(d.cleaned))

        return None if inplace else d

    @staticmethod
    def _strip_accents_unicode(text):
        """Strip accents using unicode method.

        Args:
            text (str): Text to be stripped.

        Returns: str
        """
        try:
            # If `text` is ASCII-compatible, then it does not contain any accented
            # characters and we can avoid an expensive list comprehension
            text.encode("ASCII", errors="strict")
            return text
        except UnicodeEncodeError:
            normalized = normalize('NFKD', text)
            return ''.join([c for c in normalized if not combining(c)])

    @staticmethod
    def _strip_accents_ascii(text):
        """Strip accents using ASCII method.

        This will transform accentuated unicode symbols into ASCII or nothing.

        Warning: this is only suited for languages that have a direct
        transliteration to ASCII symbols.

        Args:
            text (str): Text to be stripped.

        Returns: str
        """
        nkfd_form = normalize('NFKD', text)
        return nkfd_form.encode('ASCII', 'ignore').decode('ASCII')
