from abc import ABC, abstractmethod
from typing import Dict, Generator, List, Optional, Union


class BufferedToken(ABC):

  @abstractmethod
  def __len__(self) -> int:
    pass

  @abstractmethod
  def add_token_id(self, token_id: int) -> Optional[str]:
    pass

  @abstractmethod
  def flush(self) -> str:
    pass


class Tokenizer(ABC):

  @abstractmethod
  def encode(self, text: str, add_special_tokens: bool = False) -> List[int]:
    pass

  @abstractmethod
  def decode(self, tokens: List[int]) -> str:
    pass

  @abstractmethod
  def decode_once(self, token_id: int) -> Union[str, BufferedToken]:
    pass

  @abstractmethod
  def tokens_starting_with(self, token_id: int) -> Generator[int, None, None]:
    pass

  @abstractmethod
  def get_vocab(self) -> Dict[Union[str, bytes], int]:
    pass
