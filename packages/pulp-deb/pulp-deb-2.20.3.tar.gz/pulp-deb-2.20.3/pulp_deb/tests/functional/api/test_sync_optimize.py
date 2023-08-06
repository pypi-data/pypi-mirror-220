"""Tests that sync deb repositories in optimized mode."""
import pytest

from pulp_smash.pulp3.bindings import monitor_task

from pulp_deb.tests.functional.constants import (
    DEB_FIXTURE_ARCH,
    DEB_FIXTURE_ARCH_UPDATE,
    DEB_FIXTURE_COMPONENT,
    DEB_FIXTURE_COMPONENT_UPDATE,
    DEB_FIXTURE_SINGLE_DIST,
    DEB_FIXTURE_DISTRIBUTIONS,
    DEB_FIXTURE_STANDARD_REPOSITORY_NAME,
    DEB_FIXTURE_UPDATE_REPOSITORY_NAME,
    DEB_REPORT_CODE_SKIP_PACKAGE,
    DEB_REPORT_CODE_SKIP_RELEASE,
)


@pytest.mark.parallel
def test_sync_optimize_skip_unchanged_release_file(
    deb_remote_factory,
    deb_repository_factory,
    deb_get_repository_by_href,
    deb_sync_repository,
):
    """Test whether synchronization is skipped when a Release file remains unchanged."""
    # Create a repository and a remote and verify latest `repository_version` is 0
    repo = deb_repository_factory()
    remote = deb_remote_factory(distributions=DEB_FIXTURE_DISTRIBUTIONS)
    assert repo.latest_version_href.endswith("/0/")

    # Sync the repository
    task = deb_sync_repository(remote, repo)
    repo = deb_get_repository_by_href(repo.pulp_href)

    # Verify latest `repository_version` is 1 and sync was not skipped
    assert repo.latest_version_href.endswith("/1/")
    assert not is_sync_skipped(task, DEB_REPORT_CODE_SKIP_RELEASE)

    # Sync the repository again
    task_skip = deb_sync_repository(remote, repo)
    repo = deb_get_repository_by_href(repo.pulp_href)

    # Verify that the latest `repository_version` is still1 and sync was skipped
    assert repo.latest_version_href.endswith("/1/")
    assert is_sync_skipped(task_skip, DEB_REPORT_CODE_SKIP_RELEASE)


@pytest.mark.parallel
@pytest.mark.parametrize(
    "remote_params, remote_diff_params",
    [
        (
            [
                DEB_FIXTURE_STANDARD_REPOSITORY_NAME,
                DEB_FIXTURE_SINGLE_DIST,
                DEB_FIXTURE_COMPONENT,
                None,
            ],
            [
                DEB_FIXTURE_STANDARD_REPOSITORY_NAME,
                DEB_FIXTURE_SINGLE_DIST,
                DEB_FIXTURE_COMPONENT_UPDATE,
                None,
            ],
        ),
        (
            [DEB_FIXTURE_STANDARD_REPOSITORY_NAME, DEB_FIXTURE_SINGLE_DIST, None, DEB_FIXTURE_ARCH],
            [
                DEB_FIXTURE_STANDARD_REPOSITORY_NAME,
                DEB_FIXTURE_SINGLE_DIST,
                None,
                DEB_FIXTURE_ARCH_UPDATE,
            ],
        ),
        (
            [
                DEB_FIXTURE_STANDARD_REPOSITORY_NAME,
                DEB_FIXTURE_SINGLE_DIST,
                DEB_FIXTURE_COMPONENT,
                None,
            ],
            [
                DEB_FIXTURE_UPDATE_REPOSITORY_NAME,
                DEB_FIXTURE_SINGLE_DIST,
                DEB_FIXTURE_COMPONENT_UPDATE,
                None,
            ],
        ),
    ],
)
def test_sync_optimize_no_skip_release_file(
    deb_remote_factory,
    deb_repository_factory,
    deb_get_repository_by_href,
    remote_params,
    remote_diff_params,
    deb_sync_repository,
):
    """Test whether synchronizations have not been skipped for certain conditions.

    The following cases are tested:

    * `Sync a repository with same Release file but updated Components.`_
    * `Sync a repository with same Release file but updated Architectures.`_
    * `Sync a repository with updated Release file and updated Components.`_
    """
    # Create a repository and a remote and verify latest `repository_version` is 0
    repo = deb_repository_factory()
    remote = deb_remote_factory(
        remote_params[0],
        distributions=remote_params[1],
        components=remote_params[2],
        architectures=remote_params[3],
    )
    assert repo.latest_version_href.endswith("/0/")

    # Sync the repository
    task = deb_sync_repository(remote, repo)
    repo = deb_get_repository_by_href(repo.pulp_href)

    # Verify latest `repository_version` is 1 and sync was not skipped
    assert repo.latest_version_href.endswith("/1/")
    assert not is_sync_skipped(task, DEB_REPORT_CODE_SKIP_RELEASE)
    assert not is_sync_skipped(task, DEB_REPORT_CODE_SKIP_PACKAGE)

    # Create a new remote with different parameters and sync with repository
    remote_diff = deb_remote_factory(
        remote_diff_params[0],
        distributions=remote_diff_params[1],
        components=remote_diff_params[2],
        architectures=remote_diff_params[3],
    )
    task_diff = deb_sync_repository(remote_diff, repo)
    repo = deb_get_repository_by_href(repo.pulp_href)

    # Verify that latest `repository_version` is 2 and sync was not skipped
    assert repo.latest_version_href.endswith("/2/")
    assert not is_sync_skipped(task_diff, DEB_REPORT_CODE_SKIP_RELEASE)
    assert not is_sync_skipped(task_diff, DEB_REPORT_CODE_SKIP_PACKAGE)


@pytest.mark.parallel
def test_sync_optimize_skip_unchanged_package_index(
    deb_remote_factory,
    deb_repository_factory,
    deb_get_repository_by_href,
    deb_sync_repository,
):
    """Test whether package synchronization is skipped when a package has not been changed."""
    # Create a repository and a remote and verify latest `repository_version` is 0
    repo = deb_repository_factory()
    remote = deb_remote_factory(distributions=DEB_FIXTURE_SINGLE_DIST)
    assert repo.latest_version_href.endswith("/0/")

    # Sync the repository
    task = deb_sync_repository(remote, repo)
    repo = deb_get_repository_by_href(repo.pulp_href)

    # Verify latest `repository_version` is 1 and sync was not skipped
    assert repo.latest_version_href.endswith("/1/")
    assert not is_sync_skipped(task, DEB_REPORT_CODE_SKIP_RELEASE)
    assert not is_sync_skipped(task, DEB_REPORT_CODE_SKIP_PACKAGE)

    # Create new remote with both updated and unchanged packages and sync with repository
    remote_diff = deb_remote_factory(
        DEB_FIXTURE_UPDATE_REPOSITORY_NAME, distributions=DEB_FIXTURE_SINGLE_DIST
    )
    task_diff = deb_sync_repository(remote_diff, repo)
    repo = deb_get_repository_by_href(repo.pulp_href)

    # Verify latest `repository_version` is 2, release was not skipped and package was skipped
    assert repo.latest_version_href.endswith("/2/")
    assert not is_sync_skipped(task_diff, DEB_REPORT_CODE_SKIP_RELEASE)
    assert is_sync_skipped(task_diff, DEB_REPORT_CODE_SKIP_PACKAGE)


def test_sync_orphan_cleanup_fail(
    deb_remote_factory,
    deb_repository_factory,
    deb_get_repository_by_href,
    deb_sync_repository,
    orphans_cleanup_api_client,
    delete_orphans_pre,
):
    """Test whether an orphan cleanup is possible after syncing where only some PackageIndices got
    changed and older repository versions are not kept.

    See: https://github.com/pulp/pulp_deb/issues/690
    """
    # Create a repository and only retain the latest repository version.
    repo = deb_repository_factory(retain_repo_versions=1)

    # Create a remote and sync with repo. Verify the latest `repository_version` is 1.
    remote = deb_remote_factory(distributions=DEB_FIXTURE_SINGLE_DIST)
    deb_sync_repository(remote, repo)
    repo = deb_get_repository_by_href(repo.pulp_href)
    assert repo.latest_version_href.endswith("/1/")

    # Create a new remote with updated packages and sync again. Verify `repository_version` is 2.
    remote_diff = deb_remote_factory(
        DEB_FIXTURE_UPDATE_REPOSITORY_NAME, distributions=DEB_FIXTURE_SINGLE_DIST
    )
    deb_sync_repository(remote_diff, repo)
    repo = deb_get_repository_by_href(repo.pulp_href)
    assert repo.latest_version_href.endswith("/2/")

    # Trigger orphan cleanup without protection time and verify the task completed
    # and Content and Artifacts have been removed.
    task = monitor_task(orphans_cleanup_api_client.cleanup({"orphan_protection_time": 0}).task)
    assert task.state == "completed"
    for report in task.progress_reports:
        if "Content" in report.message:
            assert report.done == 2


def is_sync_skipped(task, code):
    """Checks if a given task has skipped the sync based of a given code."""
    for report in task.progress_reports:
        if report.code == code:
            return True
    return False
