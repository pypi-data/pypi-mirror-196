import logging
import pickle
from os import remove, rmdir, walk
from os.path import exists, join
from typing import Iterable, Dict, Union, Set, Sequence, Tuple, List, Any

import lmdb
from cachetools import LFUCache, cached
from lmdb import Environment

from pysqlitekg2vec.graphs import Vertex
from pysqlitekg2vec.graphs.io import Triple
from pysqlitekg2vec.graphs.sqlite.sqlitekg import EntityName
from pysqlitekg2vec.graphs.types import EntityID, EntityIDs, EntityNames
from pysqlitekg2vec.typings import Literals, Embeddings


class LMDBKG:
    """KG using LMDB key-value store."""

    _is_remote = False

    def __init__(self, db_file_path: str,
                 index_manager: 'IndexManager',
                 *,
                 skip_verify: bool = False):
        self.skip_verify = skip_verify
        self._index_manager = index_manager
        self._db_file_path = db_file_path
        self._lmdb = None
        self._dbs = None

    def __getstate__(self):
        return {
            'skip_verify': self.skip_verify,
            'db_file_path': self._db_file_path,
            'index_manager': self._index_manager,
        }

    def __setstate__(self, state):
        self.skip_verify = state['skip_verify']
        self._db_file_path = state['db_file_path']
        self._index_manager = state['index_manager']
        self._lmdb = None
        self._dbs = None

    def _open(self) -> Tuple[Environment, Any]:
        if self._lmdb is None:
            self._lmdb = lmdb.open(self._db_file_path, max_dbs=3)
            self._dbs = {
                'forward': self._lmdb.open_db(b'forward'),
                'backward': self._lmdb.open_db(b'backward')
            }
        return self._lmdb, self._dbs

    @property
    def entity_count(self) -> int:
        """ count of entities (occur as subject or object) in this KG. """
        return self._index_manager.object_count()

    @property
    def predicate_count(self) -> int:
        """ count of distinct predicates in the KG. """
        return self._index_manager.predicate_count()

    @property
    def statement_count(self) -> int:
        """ count of statements in the KG. """
        return 0

    def id(self, entity_name: EntityName) -> Union[EntityID, None]:
        """ returns the integer ID of the entity in form of a string.

        :param entity_name: name of the entity for which to get the ID.
        :return: the integer ID of the entity in form of a string, or `None`,
        if no entity with such a name could be found.
        """
        return self._index_manager.get_index_no(entity_name)

    def from_id(self, entity_id: EntityID) -> Union[EntityName, None]:
        """ returns the name of the entity in form of a string.

        :param entity_id: ID of the entity for which to get the name.
        :return: the integer ID of the entity in form of a string, or `None`, if
        no entity with such a ID could be found.
        """
        return self._index_manager.get_label(entity_id)

    def entities(self, restricted_to: EntityNames = None) -> EntityIDs:
        """returns all the entities, which occur as either a subject or object
        in a statement of the KG. No entity will be returned twice.

        :param restricted_to: the names (e.g. IRI) of the resources that shall
        be exclusively considered. If `None`, then all entities will be
        returned. It is `None` by default.
        :return: a list with all entity IDs.
        """
        if restricted_to is None:
            return [str(e) for e in self._index_manager.entities()]
        else:
            restriction = set(restricted_to)
            return [str(e) for e in self._index_manager.entities() if
                    self._index_manager.get_label(e) in restriction]

    def pack(self, entities: EntityIDs,
             embeddings: Embeddings) -> Sequence[Tuple[EntityName, str]]:
        """packs the entities with their embeddings.

        :param entities: IDs of the entities with which the embeddings shall be
        packed.
        :param embeddings: which shall be packed with the name of the entity.
        :return: a list of the embeddings with the corresponding name of the
        entity.
        """
        if len(entities) != len(embeddings):
            raise ValueError('list of entities must be the same size as list '
                             'of embeddings')
        return [(self._index_manager.get_label(entityID), embedding) for
                entityID, embedding in zip(entities, embeddings)]

    @cached(cache=LFUCache(maxsize=131072))
    def get_hops(self, vertex: 'Vertex',
                 is_reverse: bool = False) -> List['Hop']:
        """gets the direct hops of specified vertex as a list.

        :param vertex: name of the vertex for which to get the hops.
        :param is_reverse: If `True`, this function gets the parent nodes of a
        vertex (backward links). Otherwise, get the child nodes for this
        vertex (forward links). It is `False` by default.
        :return: the hops of a vertex in (predicate, object) form.
        """
        link_type = 'backward' if is_reverse else 'forward'
        lmdb, dbs = self._open()
        with lmdb.begin(write=False, buffers=True) as txn:
            with txn.cursor(dbs[link_type]) as cursor:
                subj_key = int(vertex.name).to_bytes(8, 'big')
                neighbours = pickle.dumps(cursor.get(subj_key))
                hops = []
                for pred, obj in neighbours:
                    other_vertex = Vertex(name=str(obj))
                    pred = Vertex(name=str(pred),
                                  vprev=other_vertex if is_reverse else vertex,
                                  vnext=vertex if is_reverse else other_vertex,
                                  predicate=True)
                    hops.append((pred, obj))
                    logging.debug('Detected %d (%s) hops for vertex "%s"',
                                  len(hops), link_type, vertex.name)
                    print(hops)
                return hops

    def get_literals(self, entities: EntityIDs, verbose: int = 0) -> Literals:
        """ gets the literals for one or more entities for all the predicates
        chain.

        :param entities: entity or entities for which to get the literals.
        :param verbose: specifies the verbosity level. `0` does not display
        anything; `1` display of the progress of extraction and training of
        walks; `2` debugging. It is `0` by default.
        :return: list that contains literals for each entity.
        """
        logging.warning('LMDBKG doesn\'t support literals')
        return []

    def is_exist(self, entities: EntityIDs) -> bool:
        """ checks whether all provided entities exist in the KG.

        :param entities: IDs of the entities for which to check the existence.
        :return: `True`, if all the entities exists, `False` otherwise.
        """
        ent_in_kg = set([int(x) for x in self.entities()])
        for entity in entities:
            if int(entity) not in ent_in_kg:
                return False
        return True


class IndexManager:
    """manages a forward and backward index for a KG."""

    def __init__(self):
        """creates a new index manager for a KG."""
        self._forward: Dict[str, int] = {}
        self._backward: Dict[int, str] = {}
        self._objects: Set[int] = set()
        self._predicates: Set[int] = set()
        self._n = 0

    def entities(self) -> Iterable[EntityID]:
        """gets an iterable over entity IDs in the index.

        :return: iterable over entity IDs in the index.
        """
        for e in self._backward.keys():
            yield e

    def store_and_get(self, entity: EntityName,
                      is_predicate: bool = False) -> int:
        """inserts given entity into the index, if a mapping doesn't already
        exist. This method returns the ID of this entity regardless of whether
        the entity was newly inserted or it already existed.

        :param entity: label of the entity that shall be inserted.
        :param is_predicate: `True`, if entity is a predicate, otherwise
        `False`.
        :return: the unique integer ID of the given entity.
        """
        # find out key
        if entity in self._forward:
            key = self._forward[entity]
        else:
            key = self._n
            self._forward[entity] = key
            self._backward[key] = entity
            self._n += 1
        # store entity in corresponding set
        if is_predicate:
            self._predicates.add(key)
        else:
            self._objects.add(key)

        return key

    def get_index_no(self, label: EntityName) -> Union[None, EntityID]:
        """gets the index number of entity with the given label.

        :param label: label of the entity for which the index shall be
        returned.
        :returns: the index number of the entity with given label will be
        returned, or `None`, if this entity doesn't exist in the index.
        """
        return self._forward.get(label, None)

    def get_label(self, index_no: EntityID) -> Union[None, EntityName]:
        """gets the label for the entity with the given index number.

        :param index_no: index number of the entity for which the label shall
        be returned.
        :return: the label of the entity with given index number will be
        returned, or `None`, if this entity doesn't exist in the index.
        """
        return self._backward.get(index_no, None)

    def predicate_count(self) -> int:
        """gets the number of predicates in the index.

        :return: the number of predicates in the index.
        """
        return len(self._predicates)

    def object_count(self) -> int:
        """gets the number of objects in the index.

        :return: the number of objects in the index.
        """
        return len(self._objects)

    def count(self) -> int:
        """gets the number of entities in the index.

        :return: the number of entities in the index.
        """
        return len(self._forward)

    def __len__(self):
        return self.count()


_ELD = pickle.dumps([])


class AutoLoadableLMDBKG(LMDBKG):
    """KG that initially loads specified data into a LMDB key-value store."""

    def __init__(self, data: Iterable[Triple],
                 db_file_path: str = 'tmp.db',
                 *,
                 skip_predicates: Iterable[str] = None,
                 **kwargs
                 ):
        """ creates a new auto loadable SQLite KG that persists the database in
        the specified file on disk.

        :param data: an iterable stream of triples.
        :param db_file_path: file path to the database.
        :param skip_predicates: a list of predicates, which makes all the
        statements with one of these predicates to be ignored.
        """
        super(AutoLoadableLMDBKG, self).__init__(db_file_path, IndexManager())
        self._db_file_path = db_file_path
        self._kwargs = kwargs
        self._import_kg(data, skip_predicates)

    def _import_kg(self, data: Iterable[Triple],
                   skip_predicates: Iterable[str]) -> None:
        skip_predicates = set(skip_predicates) \
            if skip_predicates is not None else set([])

        db_env = lmdb.Environment(self._db_file_path, max_dbs=3)
        forward_db = db_env.open_db(b'forward')
        try:
            with db_env.begin(write=True, buffers=True) as txn:
                stmt_count = 0
                with txn.cursor(db=forward_db) as forward_cursor:
                    for subj, pred, obj in data:
                        if pred in skip_predicates:
                            continue
                        subj_key = self._index_manager.store_and_get(subj)
                        pred_key = self._index_manager \
                            .store_and_get(pred, is_predicate=True)
                        obj_key = self._index_manager.store_and_get(obj)
                        # store statement
                        subj_b_key = subj_key.to_bytes(8, 'big')
                        neighbours_dump = forward_cursor \
                            .get(subj_b_key, default=_ELD)
                        neighbours = pickle.loads(neighbours_dump)
                        neighbours.append((pred_key, obj_key))
                        forward_cursor.put(subj_b_key,
                                           pickle.dumps(neighbours))
                        # count statement
                        stmt_count += 1
        finally:
            db_env.close()

    def __enter__(self):
        return LMDBKG(self._db_file_path, self._index_manager)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exists(self._db_file_path):
            for root, dirs, files in walk(self._db_file_path, topdown=False):
                for name in files:
                    remove(join(root, name))
                for name in dirs:
                    rmdir(join(root, name))
