"""Tests utils of for dataset_test."""
import os
import pathlib
from datetime import datetime
from typing import Optional, Type, cast

from typing_extensions import Protocol

from ..schema import (
  MANIFEST_FILENAME,
  PARQUET_FILENAME_PREFIX,
  VALUE_KEY,
  DataType,
  Field,
  Item,
  Schema,
  SourceManifest,
  field,
)
from ..signals.signal import EMBEDDING_KEY
from ..utils import get_dataset_output_dir, open_file
from .dataset import Dataset
from .dataset_utils import is_primitive, lilac_span, write_items_to_parquet

TEST_NAMESPACE = 'test_namespace'
TEST_DATASET_NAME = 'test_dataset'


def _infer_dtype(value: Item) -> DataType:
  if isinstance(value, str):
    return DataType.STRING
  elif isinstance(value, bool):
    return DataType.BOOLEAN
  elif isinstance(value, bytes):
    return DataType.BINARY
  elif isinstance(value, float):
    return DataType.FLOAT32
  elif isinstance(value, int):
    return DataType.INT32
  elif isinstance(value, datetime):
    return DataType.TIMESTAMP
  else:
    raise ValueError(f'Cannot infer dtype of primitive value: {value}')


def _infer_field(item: Item) -> Field:
  """Infer the schema from the items."""
  if isinstance(item, dict):
    fields: dict[str, Field] = {}
    for k, v in item.items():
      fields[k] = _infer_field(cast(Item, v))
    dtype = None
    if VALUE_KEY in fields:
      dtype = fields[VALUE_KEY].dtype
      del fields[VALUE_KEY]
    return Field(fields=fields, dtype=dtype)
  elif is_primitive(item):
    return Field(dtype=_infer_dtype(item))
  elif isinstance(item, list):
    return Field(repeated_field=_infer_field(item[0]))
  else:
    raise ValueError(f'Cannot infer schema of item: {item}')


def _infer_schema(items: list[Item]) -> Schema:
  """Infer the schema from the items."""
  schema = Schema(fields={})
  for item in items:
    field = _infer_field(item)
    if not field.fields:
      raise ValueError(f'Invalid schema of item. Expected an object, but got: {item}')
    schema.fields = {**schema.fields, **field.fields}
  return schema


class TestDataMaker(Protocol):
  """A function that creates a test dataset."""

  def __call__(self, items: list[Item], schema: Optional[Schema] = None) -> Dataset:
    """Create a test dataset."""
    ...


def make_dataset(dataset_cls: Type[Dataset],
                 tmp_path: pathlib.Path,
                 items: list[Item],
                 schema: Optional[Schema] = None) -> Dataset:
  """Create a test dataset."""
  schema = schema or _infer_schema(items)
  _write_items(tmp_path, TEST_DATASET_NAME, items, schema)
  return dataset_cls(TEST_NAMESPACE, TEST_DATASET_NAME)


def _write_items(tmpdir: pathlib.Path, dataset_name: str, items: list[Item],
                 schema: Schema) -> None:
  """Write the items JSON to the dataset format: manifest.json and parquet files."""
  source_dir = get_dataset_output_dir(str(tmpdir), TEST_NAMESPACE, dataset_name)
  os.makedirs(source_dir)

  simple_parquet_files, _ = write_items_to_parquet(
    items, source_dir, schema, filename_prefix=PARQUET_FILENAME_PREFIX, shard_index=0, num_shards=1)
  manifest = SourceManifest(files=[simple_parquet_files], data_schema=schema)
  with open_file(os.path.join(source_dir, MANIFEST_FILENAME), 'w') as f:
    f.write(manifest.json(indent=2, exclude_none=True))


def enriched_item(value: Optional[Item] = None, metadata: dict[str, Item] = {}) -> Item:
  """Wrap a value in a dict with the value key."""
  return {VALUE_KEY: value, **metadata}


def enriched_embedding_span(start: int, end: int, metadata: dict[str, Item] = {}) -> Item:
  """Makes an item that represents an embedding span that was enriched with metadata."""
  return lilac_span(start, end, {EMBEDDING_KEY: {VALUE_KEY: None, **metadata}})


def enriched_embedding_span_field(metadata: Optional[object] = {}) -> Field:
  """Makes a field that represents an embedding span that was enriched with metadata."""
  return field('string_span', fields={EMBEDDING_KEY: field('embedding', fields=metadata)})
