from dataclasses import dataclass, field
from typing import Optional, Union, List, Sequence

import pytest

from django_drf_utils.config import (
    BaseConfig,
    Email,
    Logging,
    Oidc,
    Session,
    unwrap_type,
    OidcMapper,
)

data = {
    "name": "no name",
    "description": None,
    "oidc": {
        "client_id": "test",
        "client_secret": "client_secret",
        "config_url": "https://keycloak.example/auth/realms/test/.well-known/openid-configuration",
        "login_redirect_url": "http://localhost",
        "logout_redirect_url": "http://localhost",
        "mapper": {
            "first_name": "given_name",
            "last_name": "family_name",
            "email": "email",
            "affiliation_id": "linkedAffiliationUniqueID",
            "affiliation": "linkedAffiliation",
            "additional_emails": [
                "swissEduIDAssociatedMail",
                "swissEduIDLinkedAffiliationMail",
            ],
        },
    },
    "email": {
        "host": "test.example",
        "port": 25,
        "use_tls": True,
        "user": "chuck",
        "password": "***",
        "from_address": "noreply@example.org",
        "subject_prefix": "Test prefix: ",
    },
    "session": {"expire_at_browser_close": True, "expire_seconds": 3600},
    "logging": {"level": "DEBUG"},
}


@dataclass
class ConfigTest(BaseConfig):
    name: str
    oidc: Oidc
    description: Optional[str] = None
    email: Optional[Email] = None
    logging: Logging = field(default_factory=Logging)
    session: Session = field(default_factory=Session)


def test_from_dict():
    cfg = ConfigTest.from_dict(data)
    assert cfg.name == data["name"]
    assert cfg.oidc == Oidc.from_dict(data["oidc"])
    assert cfg.oidc.mapper == OidcMapper.from_dict(data["oidc"]["mapper"])
    assert len(cfg.oidc.mapper.additional_emails) == 2
    assert cfg.email == Email.from_dict(data["email"])


def test_empty():
    cfg = ConfigTest.empty()
    # pylint: disable=no-member
    assert cfg.name == ""
    assert cfg.description is None
    assert cfg.oidc.client_id == ""
    assert cfg.oidc.mapper.first_name == ""
    assert cfg.oidc.mapper.additional_emails is None
    assert cfg.oidc.login_redirect_url == "/"
    assert cfg.session.expire_at_browser_close is False
    assert cfg.session.expire_seconds == 86400
    # pylint: enable=no-member


@pytest.mark.parametrize(
    "t, expected",
    (
        (None, None),
        (str, str),
        (Optional[str], str),
        (Optional[List[str]], str),
        (Optional[Sequence[str]], str),
        (Union[str, None], str),
        (Union[None, str], str),
        (ConfigTest, ConfigTest),
        (Optional[ConfigTest], ConfigTest),
        (int | None, int),
        (None | int, int),  # type: ignore
        (str | None, str),
        (list[str] | None, str),
        (None | list[str], str),  # type: ignore
        (str | list[str], str),
    ),
)
def test_unwrap_type_for_all(t, expected):
    assert unwrap_type(t) == expected
