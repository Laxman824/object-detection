# import os

# from counter.adapters.count_repo import CountMongoDBRepo, CountInMemoryRepo
# from counter.adapters.object_detector import TFSObjectDetector, FakeObjectDetector
# from counter.domain.actions import CountDetectedObjects


# def dev_count_action() -> CountDetectedObjects:
#     return CountDetectedObjects(FakeObjectDetector(), CountInMemoryRepo())


# def prod_count_action() -> CountDetectedObjects:
#     tfs_host = os.environ.get('TFS_HOST', 'localhost')
#     tfs_port = os.environ.get('TFS_PORT', 8501)
#     mongo_host = os.environ.get('MONGO_HOST', 'localhost')
#     mongo_port = os.environ.get('MONGO_PORT', 27017)
#     mongo_db = os.environ.get('MONGO_DB', 'prod_counter')
#     return CountDetectedObjects(TFSObjectDetector(tfs_host, tfs_port, 'rfcn'),
#                                 CountMongoDBRepo(host=mongo_host, port=mongo_port, database=mongo_db))


# def get_count_action() -> CountDetectedObjects:
#     env = os.environ.get('ENV', 'dev')
#     count_action_fn = f"{env}_count_action"
#     return globals()[count_action_fn]()
import os

from counter.adapters.count_repo import CountMongoDBRepo, CountInMemoryRepo
from counter.adapters.object_detector import TFSObjectDetector, FakeObjectDetector
from counter.domain.actions import CountDetectedObjects
from counter.domain.ports import ObjectDetector


def dev_count_action() -> CountDetectedObjects:
    return CountDetectedObjects(FakeObjectDetector(), CountInMemoryRepo())


def prod_count_action() -> CountDetectedObjects:
    tfs_host = os.environ.get('TFS_HOST', 'localhost')
    tfs_port = os.environ.get('TFS_PORT', 8501)
    
    # Use get_count_repo() instead of directly creating MongoDB repo
    return CountDetectedObjects(
        TFSObjectDetector(tfs_host, tfs_port, 'rfcn'),
        get_count_repo()  # This will select PostgreSQL or MongoDB based on DB_TYPE
    )


def get_count_action() -> CountDetectedObjects:
    env = os.environ.get('ENV', 'dev')
    count_action_fn = f"{env}_count_action"
    return globals()[count_action_fn]()


def dev_object_detector() -> ObjectDetector:
    return FakeObjectDetector()


def prod_object_detector() -> ObjectDetector:
    tfs_host = os.environ.get('TFS_HOST', 'localhost')
    tfs_port = os.environ.get('TFS_PORT', 8501)
    return TFSObjectDetector(tfs_host, tfs_port, 'rfcn')


def get_object_detector() -> ObjectDetector:
    env = os.environ.get('ENV', 'dev')
    detector_fn = f"{env}_object_detector"
    return globals()[detector_fn]()

def get_count_repo():
    """Get the appropriate repository based on configuration"""
    db_type = os.environ.get('DB_TYPE', 'mongo')
    if db_type == 'postgres':
        from counter.adapters.count_repo_postgres import CountPostgresRepo
        return CountPostgresRepo(
            host=os.environ.get('DB_HOST', 'localhost'),
            port=int(os.environ.get('DB_PORT', 5432)),
            database=os.environ.get('DB_NAME', 'object_counter'),
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD', 'postgres')
        )
    else:
        # Return MongoDB repo as default
        return CountMongoDBRepo(
            host=os.environ.get('DB_HOST', 'localhost'),
            port=int(os.environ.get('DB_PORT', 27017)),
            database=os.environ.get('DB_NAME', 'prod_counter')
        )