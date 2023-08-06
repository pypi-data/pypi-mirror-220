"""Tests for dataset.select_rows(sort_by=...)."""

from typing import Iterable, Optional, Sequence, cast

import numpy as np
import pytest
from typing_extensions import override

from ..embeddings.vector_store import VectorStore
from ..schema import UUID_COLUMN, Field, Item, RichData, VectorKey, field
from ..signals.signal import (
  EMBEDDING_KEY,
  TextEmbeddingModelSignal,
  TextEmbeddingSignal,
  TextSignal,
  clear_signal_registry,
  register_signal,
)
from .dataset import BinaryOp, Column, SortOrder
from .dataset_test_utils import TestDataMaker, enriched_item
from .dataset_utils import lilac_embedding, lilac_span


class TestSignal(TextSignal):
  name = 'test_signal'

  def fields(self) -> Field:
    return field(fields={'len': 'int32', 'is_all_cap': 'boolean'})

  def compute(self, data: Iterable[RichData]) -> Iterable[Optional[Item]]:
    for text_content in data:
      yield {'len': len(text_content), 'is_all_cap': text_content.isupper()}


class TestPrimitiveSignal(TextSignal):
  name = 'primitive_signal'

  def fields(self) -> Field:
    return field('int32')

  def compute(self, data: Iterable[RichData]) -> Iterable[Optional[Item]]:
    for text_content in data:
      yield len(text_content) + 1


class NestedArraySignal(TextSignal):
  name = 'nested_array'

  def fields(self) -> Field:
    return field(fields=[['int32']])

  def compute(self, data: Iterable[RichData]) -> Iterable[Optional[Item]]:
    for text_content in data:
      yield [[len(text_content) + 1], [len(text_content)]]


@pytest.fixture(scope='module', autouse=True)
def setup_teardown() -> Iterable[None]:
  # Setup.
  register_signal(TestSignal)
  register_signal(TestPrimitiveSignal)
  register_signal(NestedArraySignal)
  register_signal(TopKEmbedding)
  # Unit test runs.
  yield
  # Teardown.
  clear_signal_registry()


def test_sort_by_source_no_alias_no_repeated(make_test_data: TestDataMaker) -> None:
  dataset = make_test_data([{
    UUID_COLUMN: '1',
    'erased': True,
    'score': 4.1,
    'document': {
      'num_pages': 4,
      'header': {
        'title': 'c'
      }
    }
  }, {
    UUID_COLUMN: '2',
    'erased': False,
    'score': 3.5,
    'document': {
      'num_pages': 5,
      'header': {
        'title': 'b'
      }
    },
  }, {
    UUID_COLUMN: '3',
    'erased': True,
    'score': 3.7,
    'document': {
      'num_pages': 3,
      'header': {
        'title': 'a'
      }
    },
  }])

  # Sort by bool.
  result = dataset.select_rows(columns=[UUID_COLUMN], sort_by=['erased'], sort_order=SortOrder.ASC)
  assert list(result) == [{UUID_COLUMN: '2'}, {UUID_COLUMN: '1'}, {UUID_COLUMN: '3'}]
  result = dataset.select_rows(columns=[UUID_COLUMN], sort_by=['erased'], sort_order=SortOrder.DESC)
  assert list(result) == [{UUID_COLUMN: '1'}, {UUID_COLUMN: '3'}, {UUID_COLUMN: '2'}]

  # Sort by float.
  result = dataset.select_rows(columns=[UUID_COLUMN], sort_by=['score'], sort_order=SortOrder.ASC)
  assert list(result) == [{UUID_COLUMN: '2'}, {UUID_COLUMN: '3'}, {UUID_COLUMN: '1'}]
  result = dataset.select_rows(columns=[UUID_COLUMN], sort_by=['score'], sort_order=SortOrder.DESC)
  assert list(result) == [{UUID_COLUMN: '1'}, {UUID_COLUMN: '3'}, {UUID_COLUMN: '2'}]

  # Sort by nested int.
  result = dataset.select_rows(
    columns=[UUID_COLUMN], sort_by=['document.num_pages'], sort_order=SortOrder.ASC)
  assert list(result) == [{UUID_COLUMN: '3'}, {UUID_COLUMN: '1'}, {UUID_COLUMN: '2'}]
  result = dataset.select_rows(
    columns=[UUID_COLUMN], sort_by=['document.num_pages'], sort_order=SortOrder.DESC)
  assert list(result) == [{UUID_COLUMN: '2'}, {UUID_COLUMN: '1'}, {UUID_COLUMN: '3'}]

  # Sort by double nested string.
  result = dataset.select_rows(
    columns=[UUID_COLUMN], sort_by=['document.header.title'], sort_order=SortOrder.ASC)
  assert list(result) == [{UUID_COLUMN: '3'}, {UUID_COLUMN: '2'}, {UUID_COLUMN: '1'}]
  result = dataset.select_rows(
    columns=[UUID_COLUMN], sort_by=['document.header.title'], sort_order=SortOrder.DESC)
  assert list(result) == [{UUID_COLUMN: '1'}, {UUID_COLUMN: '2'}, {UUID_COLUMN: '3'}]


def test_sort_by_signal_no_alias_no_repeated(make_test_data: TestDataMaker) -> None:
  dataset = make_test_data([{
    UUID_COLUMN: '1',
    'text': 'HEY'
  }, {
    UUID_COLUMN: '2',
    'text': 'everyone'
  }, {
    UUID_COLUMN: '3',
    'text': 'HI'
  }])

  dataset.compute_signal(TestSignal(), 'text')

  # Sort by `signal.len`.
  result = dataset.select_rows(
    columns=[UUID_COLUMN], sort_by=['text.test_signal.len'], sort_order=SortOrder.ASC)
  assert list(result) == [{UUID_COLUMN: '3'}, {UUID_COLUMN: '1'}, {UUID_COLUMN: '2'}]
  result = dataset.select_rows(
    columns=[UUID_COLUMN], sort_by=['text.test_signal.len'], sort_order=SortOrder.DESC)
  assert list(result) == [{UUID_COLUMN: '2'}, {UUID_COLUMN: '1'}, {UUID_COLUMN: '3'}]

  # Sort by `signal.is_all_cap`.
  result = dataset.select_rows(
    columns=[UUID_COLUMN], sort_by=['text.test_signal.is_all_cap'], sort_order=SortOrder.ASC)
  assert list(result) == [{UUID_COLUMN: '2'}, {UUID_COLUMN: '1'}, {UUID_COLUMN: '3'}]
  result = dataset.select_rows(
    columns=[UUID_COLUMN], sort_by=['text.test_signal.is_all_cap'], sort_order=SortOrder.DESC)
  assert list(result) == [{UUID_COLUMN: '1'}, {UUID_COLUMN: '3'}, {UUID_COLUMN: '2'}]


def test_sort_by_signal_alias_no_repeated(make_test_data: TestDataMaker) -> None:
  dataset = make_test_data([{
    UUID_COLUMN: '1',
    'text': 'HEY'
  }, {
    UUID_COLUMN: '2',
    'text': 'everyone'
  }, {
    UUID_COLUMN: '3',
    'text': 'HI'
  }])

  dataset.compute_signal(TestSignal(), 'text')

  # Sort by `signal.len`.
  signal_alias = Column('text.test_signal', alias='signal')
  result = dataset.select_rows(
    columns=[signal_alias], sort_by=['signal.len'], sort_order=SortOrder.ASC)
  assert list(result) == [{
    UUID_COLUMN: '3',
    'signal': {
      'len': 2,
      'is_all_cap': True
    }
  }, {
    UUID_COLUMN: '1',
    'signal': {
      'len': 3,
      'is_all_cap': True
    }
  }, {
    UUID_COLUMN: '2',
    'signal': {
      'len': 8,
      'is_all_cap': False
    }
  }]
  result = dataset.select_rows(
    columns=[signal_alias], sort_by=['signal.len'], sort_order=SortOrder.DESC)
  assert list(result) == [{
    UUID_COLUMN: '2',
    'signal': {
      'len': 8,
      'is_all_cap': False
    }
  }, {
    UUID_COLUMN: '1',
    'signal': {
      'len': 3,
      'is_all_cap': True
    }
  }, {
    UUID_COLUMN: '3',
    'signal': {
      'len': 2,
      'is_all_cap': True
    }
  }]


def test_sort_by_enriched_alias_no_repeated(make_test_data: TestDataMaker) -> None:
  dataset = make_test_data([{
    UUID_COLUMN: '1',
    'text': 'HEY'
  }, {
    UUID_COLUMN: '2',
    'text': 'everyone'
  }, {
    UUID_COLUMN: '3',
    'text': 'HI'
  }])

  dataset.compute_signal(TestSignal(), 'text')

  # Sort by `document.test_signal.is_all_cap` where 'document' is an alias to 'text'.
  text_alias = Column('text', alias='document')
  result = dataset.select_rows(
    columns=[text_alias],
    sort_by=['document.test_signal.is_all_cap'],
    sort_order=SortOrder.ASC,
    combine_columns=True)
  assert list(result) == [{
    UUID_COLUMN: '2',
    'text': enriched_item('everyone', {'test_signal': {
      'len': 8,
      'is_all_cap': False
    }})
  }, {
    UUID_COLUMN: '1',
    'text': enriched_item('HEY', {'test_signal': {
      'len': 3,
      'is_all_cap': True
    }})
  }, {
    UUID_COLUMN: '3',
    'text': enriched_item('HI', {'test_signal': {
      'len': 2,
      'is_all_cap': True
    }})
  }]

  result = dataset.select_rows(
    columns=[text_alias],
    sort_by=['document.test_signal.is_all_cap'],
    sort_order=SortOrder.DESC,
    combine_columns=True)
  # Aliases are ignored when combining columns.
  assert list(result) == [{
    UUID_COLUMN: '1',
    'text': enriched_item('HEY', {'test_signal': {
      'len': 3,
      'is_all_cap': True
    }})
  }, {
    UUID_COLUMN: '3',
    'text': enriched_item('HI', {'test_signal': {
      'len': 2,
      'is_all_cap': True
    }})
  }, {
    UUID_COLUMN: '2',
    'text': enriched_item('everyone', {'test_signal': {
      'len': 8,
      'is_all_cap': False
    }})
  }]


def test_sort_by_udf_alias_no_repeated(make_test_data: TestDataMaker) -> None:
  dataset = make_test_data([{
    UUID_COLUMN: '1',
    'text': 'HEY'
  }, {
    UUID_COLUMN: '2',
    'text': 'everyone'
  }, {
    UUID_COLUMN: '3',
    'text': 'HI'
  }])

  # Equivalent to: SELECT `TestSignal(text) AS udf`.
  text_udf = Column('text', signal_udf=TestSignal(), alias='udf')
  # Sort by `udf.len`, where `udf` is an alias to `TestSignal(text)`.
  result = dataset.select_rows(['*', text_udf], sort_by=['udf.len'], sort_order=SortOrder.ASC)
  assert list(result) == [{
    UUID_COLUMN: '3',
    'text': 'HI',
    'udf': {
      'len': 2,
      'is_all_cap': True
    }
  }, {
    UUID_COLUMN: '1',
    'text': 'HEY',
    'udf': {
      'len': 3,
      'is_all_cap': True
    }
  }, {
    UUID_COLUMN: '2',
    'text': 'everyone',
    'udf': {
      'len': 8,
      'is_all_cap': False
    }
  }]


def test_sort_by_udf_no_alias_no_repeated(make_test_data: TestDataMaker) -> None:
  dataset = make_test_data([{
    UUID_COLUMN: '1',
    'text': 'HEY'
  }, {
    UUID_COLUMN: '2',
    'text': 'everyone'
  }, {
    UUID_COLUMN: '3',
    'text': 'HI'
  }])

  text_udf = Column('text', signal_udf=TestSignal())
  # Sort by `text.test_signal.len`, produced by executing the udf `TestSignal(text)`.
  result = dataset.select_rows(['*', text_udf],
                               sort_by=[('text', 'test_signal', 'len')],
                               sort_order=SortOrder.ASC,
                               combine_columns=True)
  assert list(result) == [{
    UUID_COLUMN: '3',
    'text': enriched_item('HI', {'test_signal': {
      'len': 2,
      'is_all_cap': True
    }}),
  }, {
    UUID_COLUMN: '1',
    'text': enriched_item('HEY', {'test_signal': {
      'len': 3,
      'is_all_cap': True
    }}),
  }, {
    UUID_COLUMN: '2',
    'text': enriched_item('everyone', {'test_signal': {
      'len': 8,
      'is_all_cap': False
    }}),
  }]

  # Sort descending.
  result = dataset.select_rows(['*', text_udf],
                               sort_by=[('text', 'test_signal', 'len')],
                               sort_order=SortOrder.DESC,
                               combine_columns=True)
  assert list(result) == [{
    UUID_COLUMN: '2',
    'text': enriched_item('everyone', {'test_signal': {
      'len': 8,
      'is_all_cap': False
    }}),
  }, {
    UUID_COLUMN: '1',
    'text': enriched_item('HEY', {'test_signal': {
      'len': 3,
      'is_all_cap': True
    }}),
  }, {
    UUID_COLUMN: '3',
    'text': enriched_item('HI', {'test_signal': {
      'len': 2,
      'is_all_cap': True
    }}),
  }]


def test_sort_by_primitive_udf_alias_no_repeated(make_test_data: TestDataMaker) -> None:
  dataset = make_test_data([{
    UUID_COLUMN: '1',
    'text': 'HEY'
  }, {
    UUID_COLUMN: '2',
    'text': 'everyone'
  }, {
    UUID_COLUMN: '3',
    'text': 'HI'
  }])

  # Equivalent to: SELECT `TestPrimitiveSignal(text) AS udf`.
  text_udf = Column('text', signal_udf=TestPrimitiveSignal(), alias='udf')
  # Sort by the primitive value returned by the udf.
  result = dataset.select_rows(['*', text_udf], sort_by=['udf'], sort_order=SortOrder.ASC)
  assert list(result) == [{
    UUID_COLUMN: '3',
    'text': 'HI',
    'udf': 3
  }, {
    UUID_COLUMN: '1',
    'text': 'HEY',
    'udf': 4
  }, {
    UUID_COLUMN: '2',
    'text': 'everyone',
    'udf': 9
  }]


def test_sort_by_source_non_leaf_errors(make_test_data: TestDataMaker) -> None:
  dataset = make_test_data([{
    UUID_COLUMN: '1',
    'vals': [7, 1]
  }, {
    UUID_COLUMN: '2',
    'vals': [3, 4]
  }, {
    UUID_COLUMN: '3',
    'vals': [9, 0]
  }])

  # Sort by repeated.
  with pytest.raises(ValueError, match='Unable to sort by path'):
    dataset.select_rows(columns=[UUID_COLUMN], sort_by=['vals'], sort_order=SortOrder.ASC)


def test_sort_by_source_no_alias_repeated(make_test_data: TestDataMaker) -> None:
  dataset = make_test_data([{
    UUID_COLUMN: '1',
    'vals': [[{
      'score': 7
    }, {
      'score': 1
    }], [{
      'score': 1
    }, {
      'score': 7
    }]]
  }, {
    UUID_COLUMN: '2',
    'vals': [[{
      'score': 3
    }, {
      'score': 4
    }]]
  }, {
    UUID_COLUMN: '3',
    'vals': [[{
      'score': 9
    }, {
      'score': 0
    }]]
  }])

  # Sort by repeated 'vals'.
  result = dataset.select_rows(
    columns=[UUID_COLUMN, 'vals'], sort_by=['vals.*.*.score'], sort_order=SortOrder.ASC)
  assert list(result) == [{
    UUID_COLUMN: '3',
    'vals': [[{
      'score': 9
    }, {
      'score': 0
    }]]
  }, {
    UUID_COLUMN: '1',
    'vals': [[{
      'score': 7
    }, {
      'score': 1
    }], [{
      'score': 1
    }, {
      'score': 7
    }]]
  }, {
    UUID_COLUMN: '2',
    'vals': [[{
      'score': 3
    }, {
      'score': 4
    }]]
  }]

  result = dataset.select_rows(
    columns=[UUID_COLUMN, 'vals'], sort_by=['vals.*.*.score'], sort_order=SortOrder.DESC)
  assert list(result) == [{
    UUID_COLUMN: '3',
    'vals': [[{
      'score': 9
    }, {
      'score': 0
    }]]
  }, {
    UUID_COLUMN: '1',
    'vals': [[{
      'score': 7
    }, {
      'score': 1
    }], [{
      'score': 1
    }, {
      'score': 7
    }]]
  }, {
    UUID_COLUMN: '2',
    'vals': [[{
      'score': 3
    }, {
      'score': 4
    }]]
  }]


def test_sort_by_source_alias_repeated(make_test_data: TestDataMaker) -> None:
  dataset = make_test_data([{
    UUID_COLUMN: '1',
    'vals': [[7, 1], [1, 7]]
  }, {
    UUID_COLUMN: '2',
    'vals': [[3], [11]]
  }, {
    UUID_COLUMN: '3',
    'vals': [[9, 0]]
  }])

  # Sort by repeated 'vals'.
  result = dataset.select_rows(
    columns=[UUID_COLUMN, Column('vals', alias='scores')],
    sort_by=['scores.*.*'],
    sort_order=SortOrder.ASC)
  assert list(result) == [{
    UUID_COLUMN: '3',
    'scores': [[9, 0]]
  }, {
    UUID_COLUMN: '1',
    'scores': [[7, 1], [1, 7]]
  }, {
    UUID_COLUMN: '2',
    'scores': [[3], [11]]
  }]

  result = dataset.select_rows(
    columns=[UUID_COLUMN, Column('vals', alias='scores')],
    sort_by=['scores.*.*'],
    sort_order=SortOrder.DESC)
  assert list(result) == [{
    UUID_COLUMN: '2',
    'scores': [[3], [11]]
  }, {
    UUID_COLUMN: '3',
    'scores': [[9, 0]]
  }, {
    UUID_COLUMN: '1',
    'scores': [[7, 1], [1, 7]]
  }]


def test_sort_by_udf_alias_repeated(make_test_data: TestDataMaker) -> None:
  dataset = make_test_data([{
    UUID_COLUMN: '1',
    'text': 'HEY'
  }, {
    UUID_COLUMN: '2',
    'text': 'everyone'
  }, {
    UUID_COLUMN: '3',
    'text': 'HI'
  }])

  # Equivalent to: SELECT `NestedArraySignal(text) AS udf`.
  text_udf = Column('text', signal_udf=NestedArraySignal(), alias='udf')
  # Sort by `udf.*.*`, where `udf` is an alias to `NestedArraySignal(text)`.
  result = dataset.select_rows(['*', text_udf], sort_by=['udf.*.*'], sort_order=SortOrder.ASC)
  assert list(result) == [{
    UUID_COLUMN: '3',
    'text': 'HI',
    'udf': [[3], [2]]
  }, {
    UUID_COLUMN: '1',
    'text': 'HEY',
    'udf': [[4], [3]]
  }, {
    UUID_COLUMN: '2',
    'text': 'everyone',
    'udf': [[9], [8]]
  }]
  result = dataset.select_rows(['*', text_udf], sort_by=['udf.*.*'], sort_order=SortOrder.DESC)
  assert list(result) == [{
    UUID_COLUMN: '2',
    'text': 'everyone',
    'udf': [[9], [8]]
  }, {
    UUID_COLUMN: '1',
    'text': 'HEY',
    'udf': [[4], [3]]
  }, {
    UUID_COLUMN: '3',
    'text': 'HI',
    'udf': [[3], [2]]
  }]


def test_sort_by_complex_signal_udf_alias_called_on_repeated(make_test_data: TestDataMaker) -> None:
  dataset = make_test_data([{
    UUID_COLUMN: '1',
    'texts': [{
      'text': 'eardrop'
    }, {
      'text': 'I'
    }]
  }, {
    UUID_COLUMN: '2',
    'texts': [{
      'text': 'hey'
    }, {
      'text': 'CARS'
    }]
  }, {
    UUID_COLUMN: '3',
    'texts': [{
      'text': 'everyone'
    }, {
      'text': ''
    }]
  }])

  # Equivalent to: SELECT `TestSignal(texts.*.text) AS udf`.
  texts_udf = Column('texts.*.text', signal_udf=TestSignal(), alias='udf')
  # Sort by `udf.len`, where `udf` is an alias to `TestSignal(texts.*.text)`.
  result = dataset.select_rows(['*', texts_udf],
                               sort_by=['udf.len'],
                               sort_order=SortOrder.ASC,
                               combine_columns=True)
  assert list(result) == [{
    UUID_COLUMN: '3',
    'texts': [{
      'text': enriched_item('everyone', {'test_signal': {
        'len': 8,
        'is_all_cap': False
      }})
    }, {
      'text': enriched_item('', {'test_signal': {
        'len': 0,
        'is_all_cap': False
      }})
    }]
  }, {
    UUID_COLUMN: '1',
    'texts': [{
      'text': enriched_item('eardrop', {'test_signal': {
        'len': 7,
        'is_all_cap': False
      }})
    }, {
      'text': enriched_item('I', {'test_signal': {
        'len': 1,
        'is_all_cap': True
      }})
    }]
  }, {
    UUID_COLUMN: '2',
    'texts': [{
      'text': enriched_item('hey', {'test_signal': {
        'len': 3,
        'is_all_cap': False
      }})
    }, {
      'text': enriched_item('CARS', {'test_signal': {
        'len': 4,
        'is_all_cap': True
      }})
    }]
  }]


def test_sort_by_primitive_signal_udf_alias_called_on_repeated(
    make_test_data: TestDataMaker) -> None:
  dataset = make_test_data([{
    UUID_COLUMN: '1',
    'texts': [{
      'text': 'eardrop'
    }, {
      'text': 'I'
    }]
  }, {
    UUID_COLUMN: '2',
    'texts': [{
      'text': 'hey'
    }, {
      'text': 'CARS'
    }]
  }, {
    UUID_COLUMN: '3',
    'texts': [{
      'text': 'everyone'
    }, {
      'text': ''
    }]
  }])

  # Equivalent to: SELECT `TestPrimitiveSignal(texts.*.text) AS udf`.
  texts_udf = Column('texts.*.text', signal_udf=TestPrimitiveSignal(), alias='udf')
  # Sort by `udf`, where `udf` is an alias to `TestPrimitiveSignal(texts.*.text)`.
  result = dataset.select_rows(['*', texts_udf],
                               sort_by=['udf'],
                               sort_order=SortOrder.ASC,
                               combine_columns=True)
  assert list(result) == [{
    UUID_COLUMN: '3',
    'texts': [{
      'text': enriched_item('everyone', {'primitive_signal': 9})
    }, {
      'text': enriched_item('', {'primitive_signal': 1})
    }]
  }, {
    UUID_COLUMN: '1',
    'texts': [{
      'text': enriched_item('eardrop', {'primitive_signal': 8})
    }, {
      'text': enriched_item('I', {'primitive_signal': 2})
    }]
  }, {
    UUID_COLUMN: '2',
    'texts': [{
      'text': enriched_item('hey', {'primitive_signal': 4})
    }, {
      'text': enriched_item('CARS', {'primitive_signal': 5})
    }]
  }]
  result = dataset.select_rows(['*', texts_udf],
                               sort_by=['udf'],
                               sort_order=SortOrder.DESC,
                               combine_columns=True)
  assert list(result) == [{
    UUID_COLUMN: '3',
    'texts': [{
      'text': enriched_item('everyone', {'primitive_signal': 9})
    }, {
      'text': enriched_item('', {'primitive_signal': 1})
    }]
  }, {
    UUID_COLUMN: '1',
    'texts': [{
      'text': enriched_item('eardrop', {'primitive_signal': 8})
    }, {
      'text': enriched_item('I', {'primitive_signal': 2})
    }]
  }, {
    UUID_COLUMN: '2',
    'texts': [{
      'text': enriched_item('hey', {'primitive_signal': 4})
    }, {
      'text': enriched_item('CARS', {'primitive_signal': 5})
    }]
  }]


class TopKEmbedding(TextEmbeddingSignal):
  """A test embed function."""
  name = 'topk_embedding'

  def compute(self, data: Iterable[RichData]) -> Iterable[Item]:
    """Call the embedding function."""
    for example in data:
      example = cast(str, example)
      emb_spans: list[Item] = []
      for i, score in enumerate(example.split('_')):
        start, end = i * 2, i * 2 + 1
        vector = np.array([int(score)])
        emb_spans.append(lilac_embedding(start, end, vector))
      yield emb_spans


class TopKSignal(TextEmbeddingModelSignal):
  """Compute scores along a given concept for documents."""
  name = 'topk_signal'

  _query = np.array([1])

  def fields(self) -> Field:
    return field('float32')

  @override
  def vector_compute(self, keys: Iterable[VectorKey],
                     vector_store: VectorStore) -> Iterable[Optional[Item]]:
    text_embeddings = vector_store.get(keys)
    dot_products = text_embeddings.dot(self._query).reshape(-1)
    return dot_products.tolist()

  @override
  def vector_compute_topk(
      self,
      topk: int,
      vector_store: VectorStore,
      keys: Optional[Iterable[VectorKey]] = None) -> Sequence[tuple[VectorKey, Optional[Item]]]:
    return vector_store.topk(self._query, topk, keys)


def test_sort_by_topk_embedding_udf(make_test_data: TestDataMaker) -> None:
  dataset = make_test_data([{
    UUID_COLUMN: '1',
    'scores': '8_1',
  }, {
    UUID_COLUMN: '2',
    'scores': '3_5'
  }, {
    UUID_COLUMN: '3',
    'scores': '9_7'
  }])

  dataset.compute_signal(TopKEmbedding(), 'scores')

  # Equivalent to: SELECT `TopKSignal(scores, embedding='...') AS udf`.
  text_udf = Column('scores', signal_udf=TopKSignal(embedding='topk_embedding'), alias='udf')
  # Sort by `udf`, where `udf` is an alias to `TopKSignal(scores, embedding='...')`.
  result = dataset.select_rows(['*', text_udf],
                               sort_by=['udf'],
                               sort_order=SortOrder.DESC,
                               limit=3,
                               combine_columns=True)
  assert list(result) == [{
    UUID_COLUMN: '3',
    'scores': enriched_item(
      '9_7', {
        'topk_embedding': [
          lilac_span(0, 1, {EMBEDDING_KEY: {
            'topk_signal': 9.0
          }}),
          lilac_span(2, 3, {EMBEDDING_KEY: {
            'topk_signal': 7.0
          }})
        ]
      }),
  }, {
    UUID_COLUMN: '1',
    'scores': enriched_item(
      '8_1', {
        'topk_embedding': [
          lilac_span(0, 1, {EMBEDDING_KEY: {
            'topk_signal': 8.0
          }}),
          lilac_span(2, 3, {EMBEDDING_KEY: {
            'topk_signal': 1.0
          }})
        ]
      }),
  }]

  # Same but set limit to 4.
  result = dataset.select_rows(['*', text_udf],
                               sort_by=['udf'],
                               sort_order=SortOrder.DESC,
                               limit=4,
                               combine_columns=True)
  assert list(result) == [{
    UUID_COLUMN: '3',
    'scores': enriched_item(
      '9_7', {
        'topk_embedding': [
          lilac_span(0, 1, {EMBEDDING_KEY: {
            'topk_signal': 9.0
          }}),
          lilac_span(2, 3, {EMBEDDING_KEY: {
            'topk_signal': 7.0
          }})
        ]
      }),
  }, {
    UUID_COLUMN: '1',
    'scores': enriched_item(
      '8_1', {
        'topk_embedding': [
          lilac_span(0, 1, {EMBEDDING_KEY: {
            'topk_signal': 8.0
          }}),
          lilac_span(2, 3, {EMBEDDING_KEY: {
            'topk_signal': 1.0
          }})
        ]
      }),
  }, {
    UUID_COLUMN: '2',
    'scores': enriched_item(
      '3_5', {
        'topk_embedding': [
          lilac_span(0, 1, {EMBEDDING_KEY: {
            'topk_signal': 3.0
          }}),
          lilac_span(2, 3, {EMBEDDING_KEY: {
            'topk_signal': 5.0
          }})
        ]
      }),
  }]


def test_sort_by_topk_udf_with_filter(make_test_data: TestDataMaker) -> None:
  dataset = make_test_data([{
    UUID_COLUMN: '1',
    'scores': '8_1',
    'active': True
  }, {
    UUID_COLUMN: '2',
    'scores': '3_5',
    'active': True
  }, {
    UUID_COLUMN: '3',
    'scores': '9_7',
    'active': False
  }])

  dataset.compute_signal(TopKEmbedding(), 'scores')

  # Equivalent to: SELECT `TopKSignal(scores, embedding='...') AS udf`.
  text_udf = Column('scores', signal_udf=TopKSignal(embedding='topk_embedding'), alias='udf')
  # Sort by `udf`, where `udf` is an alias to `TopKSignal(scores, embedding='...')`.
  result = dataset.select_rows(['*', text_udf],
                               sort_by=['udf'],
                               filters=[('active', BinaryOp.EQUALS, True)],
                               sort_order=SortOrder.DESC,
                               limit=2,
                               combine_columns=True)
  # We make sure that '3' is not in the result, because it is not active, even though it has the
  # highest topk score.
  assert list(result) == [{
    UUID_COLUMN: '1',
    'active': True,
    'scores': enriched_item(
      '8_1', {
        'topk_embedding': [
          lilac_span(0, 1, {EMBEDDING_KEY: {
            'topk_signal': 8.0
          }}),
          lilac_span(2, 3, {EMBEDDING_KEY: {
            'topk_signal': 1.0
          }})
        ]
      })
  }, {
    UUID_COLUMN: '2',
    'active': True,
    'scores': enriched_item(
      '3_5', {
        'topk_embedding': [
          lilac_span(0, 1, {EMBEDDING_KEY: {
            'topk_signal': 3.0
          }}),
          lilac_span(2, 3, {EMBEDDING_KEY: {
            'topk_signal': 5.0
          }})
        ]
      })
  }]
