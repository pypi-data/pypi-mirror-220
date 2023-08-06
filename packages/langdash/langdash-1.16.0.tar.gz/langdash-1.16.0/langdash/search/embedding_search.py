from typing import Generator, List, Tuple, Union

import faiss  # type: ignore

from langdash.llm_session import LLMEmbeddingSession
from langdash.search.engine import Engine


class EmbeddingSearch(Engine):
  """ A search engine that uses vector embeddings from a language model. """

  def __init__(
    self,
    embd_session: LLMEmbeddingSession,
    embd_formatter: str = "{text}",
  ):
    """
    Args:
      embd_session (LLMEmbeddingSession):
        An LLMSession object for models that supports embeddings.
      embd_formatter (str):
        Formatting string which will be passed into the model.
        This string must contain the `text` variable as formatting argument.

        Defaults to `"{text}"`.
    """
    super().__init__()
    self._embd_session = embd_session
    self._embd_formatter = embd_formatter
    self._embds = faiss.IndexFlatIP(self._embd_session.embedding_size)

  def add(self, text_raw: Union[str, List[str]]):
    if isinstance(text_raw, str):
      texts = [self._embd_formatter.format(text=text_raw)]
      self._documents.append(text_raw)
    else:
      texts = []
      for text in text_raw:
        if not text:
          raise ValueError("unexpected empty text")
        texts.append(self._embd_formatter.format(text=text))
      self._documents += text_raw

    self._embds.add(self._embd_session.embed(texts))

  def search(
    self,
    text: str,
    max_documents: int = 1
  ) -> Generator[Tuple[int, str, float], None, None]:
    if not text:
      return
    embd = self._embd_session.embed([text])
    if max_documents == -1:
      max_documents = len(self._documents)
    docs, indices = self._embds.search(embd, max_documents)
    for doc, i in zip(docs[0], indices[0]):
      yield i, self._documents[i], doc
