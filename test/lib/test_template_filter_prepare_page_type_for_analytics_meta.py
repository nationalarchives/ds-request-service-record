import pytest

from app.lib.template_filters import prepare_page_type_for_analytics_meta_tag


@pytest.mark.parametrize(
    "request_path,expected",
    [
        (None, ""),
        ("", ""),
        ("   ", ""),
    ],
)
def test_returns_empty_string_for_empty_like_inputs(request_path, expected):
    assert prepare_page_type_for_analytics_meta_tag(request_path) == expected


@pytest.mark.parametrize(
    "request_path,expected",
    [
        (
            "request-a-military-service-record",
            "request-a-military-service-record_ramsr",
        ),
        (
            "/request-a-military-service-record",
            "request-a-military-service-record_ramsr",
        ),
        (
            "request-a-military-service-record/",
            "request-a-military-service-record_ramsr",
        ),
        (
            "/request-a-military-service-record/",
            "request-a-military-service-record_ramsr",
        ),
        (
            "  /request-a-military-service-record/  ",
            "request-a-military-service-record_ramsr",
        ),
    ],
)
def test_base_path_variants_map_to_base_suffix(request_path, expected):
    assert prepare_page_type_for_analytics_meta_tag(request_path) == expected


@pytest.mark.parametrize(
    "request_path,expected",
    [
        (
            "request-a-military-service-record/before-you-start",
            "before-you-start_ramsr",
        ),
        (
            "/request-a-military-service-record/before-you-start/",
            "before-you-start_ramsr",
        ),
        (
            "request-a-military-service-record/before-you-start/12345",
            "before-you-start_ramsr",
        ),
        (
            "request-a-military-service-record/before-you-start/12345/67890",
            "before-you-start_ramsr",
        ),
    ],
)
def test_base_child_paths_use_first_segment_only_plus_suffix(request_path, expected):
    assert prepare_page_type_for_analytics_meta_tag(request_path) == expected
