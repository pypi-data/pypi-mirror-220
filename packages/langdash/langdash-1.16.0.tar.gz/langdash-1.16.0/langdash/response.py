from dataclasses import dataclass


class Response:
  """ Base class for responses from language model. """
  pass


@dataclass
class RespReturns(Response):
  """
  Returns response. Acts as a header for return values.
  
  Attributes:
    key: Return key
  """
  key: str


@dataclass
class RespInfer(Response):
  """
  Inference response. Will be emitted on every token generated.
  
  Attributes:
    tokid: Token ID
    tokstr: Token string representation
    running_infer: Current generated string
  """
  tokid: int
  tokstr: str
  running_infer: str


@dataclass
class RespInferEnd(Response):
  running_infer: str
  tokens_counter: int


@dataclass
class RespInject(Response):
  """
  Injected response. Will be emitted every time new context is injected.
  
  Attributes:
    tokens_counter: Number of tokens injected to model
  """
  tokens_counter: int


@dataclass
class RespSubchain(Response):
  """
  Subchain response.
  
  Attributes:
    key: Return key
    resp_subchain: Response generated in subchain
  """
  key: str
  resp_subchain: Response


@dataclass
class RespChoice(Response):
  """
  Choice response.
  """
  choice: int
  tokens_counter: int
