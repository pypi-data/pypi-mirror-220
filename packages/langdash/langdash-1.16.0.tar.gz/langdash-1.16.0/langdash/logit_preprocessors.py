import abc
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
  import torch

  from langdash.llm_session import LLMGenerationSession


class LogitPreprocessor(abc.ABC):
  """
  Base class for a logit preprocessor.
  """

  @abc.abstractmethod
  def __init__(self, session: "LLMGenerationSession"):
    pass

  @abc.abstractmethod
  def __call__(self, input_ids: List[int], logits: "torch.Tensor"):
    """
    Preprocesor callback at each generation step.

    Args:
      input_ids (List[int]):
        The list of token ids generated so far.
      logits (torch.Tensor):
        The logit vector for the next generation step. This vector may be modified
        within the function.

    Returns:
      None
    """
    pass
