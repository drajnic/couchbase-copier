from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.exceptions import CouchbaseException
from dotenv import load_dotenv
import os

load_dotenv()
source_host = os.environ.get('SOURCE_HOST')
source_bucketname = os.environ.get('SOURCE_BUCKET')
source_username = os.environ.get('SOURCE_USER')
source_password = os.environ.get('SOURCE_PASS')
document_ids_query = os.environ.get('ID_QUERY')

target_host = os.environ.get('TARGET_HOST')
target_bucketname = os.environ.get('TARGET_BUCKET')
target_username = os.environ.get('TARGET_USER')
target_password = os.environ.get('TARGET_PASS')
target_overwrite = 'true' == os.environ.get('TARGET_OVERWRITE', 'false')

batch_size = int(os.environ.get('BATCH_SIZE', '10'))

source_cluster = Cluster.connect(
    f'couchbase://{source_host}',
    ClusterOptions(PasswordAuthenticator(source_username, source_password))
)
source_bucket = source_cluster.bucket(source_bucketname)
source_collection = source_bucket.default_collection()

target_cluster = Cluster.connect(
    f'couchbase://{target_host}',
    ClusterOptions(PasswordAuthenticator(target_username, target_password))
)
target_bucket = target_cluster.bucket(target_bucketname)
target_collection = target_bucket.default_collection()

def copy_documents(document_ids):
    source_documents = source_collection.get_multi(document_ids)
    target_collection.upsert_multi(dict((source_documents.results[key].key, source_documents.results[key].value) for key in source_documents.results))

def split(list_a, chunk_size):
  for i in range(0, len(list_a), chunk_size):
    yield list_a[i:i + chunk_size]

try:
    document_ids_query_result = source_cluster.query(document_ids_query)

    ids = []
    for row in document_ids_query_result.rows():
        ids.append(row['id'])

    print(f'Found {len(ids)} document id(s).')

    if target_overwrite == False:
        print('Reducing ids - skipping existing ones')
        exists_chunks = list(split(ids, 1000))
        for chunk in exists_chunks:
            target_exists = target_collection.exists_multi(chunk)
            for key in target_exists.results:
                if target_exists.results[key].exists:
                    ids.remove(target_exists.results[key].key)
        print(f'Reducing ids - Reduced to {len(ids)} document id(s).')

    final_chunks = list(split(ids, batch_size))

    for index, chunk in enumerate(final_chunks):
        print(f'Transfering chunk {index + 1}/{len(final_chunks)}')
        copy_documents(chunk)

except CouchbaseException as ex:
    import traceback
    traceback.print_exc()