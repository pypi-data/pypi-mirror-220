import pytest
from bufap.parser import radius


@pytest.mark.parametrize(
    ("conf", "expected"),
    [
        (
            "radius primary enable server 192.168.11.10 secret buffalo",
            {
                "radius": {
                    "primary": {
                        "enable": "enable",
                        "host": "192.168.11.10",
                        "secret": "buffalo",
                        "type": "server",
                    }
                }
            },
        ),
        (
            "radius secondary enable internal_server",
            {
                "radius": {
                    "secondary": {
                        "enable": "enable",
                        "host": None,
                        "secret": None,
                        "type": "internal_server",
                    }
                }
            },
        ),
        ("radius primary disable", {"radius": {"primary": {"enable": "disable"}}}),
        (
            "radius primary session-timeout 60",
            {"radius": {"primary": {"session-timeout": "60"}}},
        ),
        (
            "radius secondary session-timeout 0",
            {"radius": {"secondary": {"session-timeout": "0"}}},
        ),
        (
            "radius primary authport 12293",
            {"radius": {"primary": {"authport": "12293"}}},
        ),
        (
            "radius secondary authport 19224",
            {"radius": {"secondary": {"authport": "19224"}}},
        ),
        (
            "radius primary acctport 12294",
            {"radius": {"primary": {"acctport": "12294"}}},
        ),
        (
            "radius secondary acctport 19225",
            {"radius": {"secondary": {"acctport": "19225"}}},
        ),
        (
            "radius primary accounting enable",
            {"radius": {"primary": {"accounting": {"enable": "enable"}}}},
        ),
        (
            "radius secondary accounting disable",
            {"radius": {"secondary": {"accounting": {"enable": "disable"}}}},
        ),
        (
            "radius asam enable auth secret key buffalo12345678",
            {"radius": {"asam": {"enable": "enable", "key": "buffalo12345678"}}},
        ),
        (
            "radius calling-station-id-separator none",
            {"radius": {"calling-station-id-separator": "none"}},
        ),
        (
            "radius calling-station-id-separator hyphen",
            {"radius": {"calling-station-id-separator": "hyphen"}},
        ),
        (
            "radius called-station-id-separator mac",
            {"radius": {"called-station-id-separator": "mac"}},
        ),
        (
            "radius called-station-id-separator mac-ssid",
            {"radius": {"called-station-id-separator": "mac-ssid"}},
        ),
        (
            "radius internal_server session-timeout 3600",
            {"radius": {"internal_server": {"session-timeout": "3600"}}},
        ),
        (
            "radius internal_server termination-action request",
            {"radius": {"internal_server": {"termination-action": "request"}}},
        ),
    ],
)
def test_parse(conf: str, expected: dict):
    assert radius.parse(conf) == expected
