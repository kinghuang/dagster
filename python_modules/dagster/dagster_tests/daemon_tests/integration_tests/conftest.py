import sys

import pytest
from dagster import file_relative_path
from dagster.core.host_representation import (
    ManagedGrpcPythonEnvRepositoryLocationOrigin,
    PipelineHandle,
)
from dagster.core.types.loadable_target_origin import LoadableTargetOrigin


def get_example_repository_location_handle():
    loadable_target_origin = LoadableTargetOrigin(
        executable_path=sys.executable,
        python_file=file_relative_path(__file__, "repo.py"),
    )
    location_name = "example_repo_location"

    origin = ManagedGrpcPythonEnvRepositoryLocationOrigin(loadable_target_origin, location_name)

    return origin.create_handle()


@pytest.fixture
def foo_example_repo():
    with get_example_repository_location_handle() as location_handle:
        yield location_handle.create_location().get_repository("example_repo")


@pytest.fixture
def foo_pipeline_handle(foo_example_repo):  # pylint: disable=redefined-outer-name
    return PipelineHandle("foo_pipeline", foo_example_repo.handle)
