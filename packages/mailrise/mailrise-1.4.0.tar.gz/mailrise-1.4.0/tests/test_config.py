"""
Tests for configuration loading.
"""

import logging
from io import StringIO

import pytest
from apprise import Apprise, AppriseConfig, NotifyFormat
from pytest import MonkeyPatch

from mailrise.basic_authenticator import BasicAuthenticator
from mailrise.config import load_config
from mailrise.simple_router import _Key, SimpleRouter


_logger = logging.getLogger(__name__)


def test_errors() -> None:
    """Tests for :fun:`load_config`'s failure conditions."""
    with pytest.raises(SystemExit):
        file = StringIO("""
            24
        """)
        load_config(_logger, file)
    with pytest.raises(SystemExit):
        file = StringIO("""
            configs: 24
        """)
        load_config(_logger, file)
    with pytest.raises(SystemExit):
        file = StringIO("""
            configs:
              test: 24
        """)
        load_config(_logger, file)


def test_load() -> None:
    """Tests a successful load with :fun:`load_config`."""
    file = StringIO("""
        configs:
          test:
            urls:
              - json://localhost
    """)
    mrise = load_config(_logger, file)
    router = mrise.router
    assert isinstance(router, SimpleRouter)
    assert len(router.senders) == 1
    key = _Key(user='test')
    assert mrise.authenticator is None

    sender = router.get_sender(key)
    assert sender is not None
    notifier = _make_notifier(sender.config_yaml)
    assert len(notifier) == 1
    assert notifier[0].url().startswith('json://localhost/')


def test_multi_load() -> None:
    """Tests a sucessful load with :fun:`load_config` with multiple configs."""
    file = StringIO("""
        configs:
          test1:
            urls:
              - json://localhost
          test2:
            urls:
              - json://localhost
    """)
    mrise = load_config(_logger, file)
    router = mrise.router
    assert isinstance(router, SimpleRouter)
    assert len(router.senders) == 2

    for user in ('test1', 'test2'):
        key = _Key(user=user)

        sender = router.get_sender(key)
        assert sender is not None
        notifier = _make_notifier(sender.config_yaml)
        assert len(notifier) == 1
        assert notifier[0].url().startswith('json://localhost/')


def test_mailrise_options() -> None:
    """Tests a successful load with :fun:`load_config` with Mailrise-specific
    options."""
    file = StringIO("""
        configs:
          test:
            urls:
              - json://localhost
            mailrise:
              title_template: ""
              body_format: "text"
    """)
    mrise = load_config(_logger, file)
    router = mrise.router
    assert isinstance(router, SimpleRouter)
    assert len(router.senders) == 1
    key = _Key(user='test')

    sender = router.get_sender(key)
    assert sender is not None
    assert sender.title_template.template == ''
    assert sender.body_format == NotifyFormat.TEXT

    with pytest.raises(SystemExit):
        file = StringIO("""
            configs:
              test:
                urls:
                  - json://localhost
                mailrise:
                  body_format: "BAD"
        """)
        load_config(_logger, file)


def test_config_keys() -> None:
    """Tests the config key parser with both string and full email formats."""
    with pytest.raises(SystemExit):
        file = StringIO("""
            configs:
              has.periods:
                urls:
                  - json://localhost
        """)
        load_config(_logger, file)
    with pytest.raises(SystemExit):
        file = StringIO("""
            configs:
              bademail@:
                urls:
                  - json://localhost
        """)
        load_config(_logger, file)
    file = StringIO("""
        configs:
          user@example.com:
            urls:
              - json://localhost
    """)
    mrise = load_config(_logger, file)
    router = mrise.router
    assert isinstance(router, SimpleRouter)
    assert len(router.senders) == 1
    key = _Key(user='user', domain='example.com')
    assert router.get_sender(key) is not None


def test_fnmatch_config_keys() -> None:
    """Tests the config key parser with fnmatch pattern tokens."""
    # This defaults to "*@mailrise.xyz", which may not be obvious at first
    # glance.
    file = StringIO("""
        configs:
          "*":
            urls:
              - json://localhost
    """)
    mrise = load_config(_logger, file)
    router = mrise.router
    assert isinstance(router, SimpleRouter)
    key = _Key(user='user', domain='example.com')
    assert router.get_sender(key) is None
    key = _Key(user='user', domain='mailrise.xyz')
    assert router.get_sender(key) is not None

    file = StringIO("""
        configs:
          "*@*":
            urls:
              - json://localhost
    """)
    mrise = load_config(_logger, file)
    router = mrise.router
    assert isinstance(router, SimpleRouter)
    key = _Key(user='user', domain='example.com')
    assert router.get_sender(key) is not None

    file = StringIO("""
        configs:
          "the*@*":
            urls:
              - json://localhost
    """)
    mrise = load_config(_logger, file)
    router = mrise.router
    assert isinstance(router, SimpleRouter)
    key = _Key(user='user', domain='example.com')
    assert router.get_sender(key) is None
    key = _Key(user='thequickbrownfox', domain='example.com')
    assert router.get_sender(key) is not None


def test_authenticator() -> None:
    """Tests a successful load with an authenticator."""
    file = StringIO("""
        configs:
          test:
            urls:
              - json://localhost
        smtp:
          auth:
            basic:
              username: password
              AzureDiamond: hunter2
    """)
    mrise = load_config(_logger, file)
    assert isinstance(mrise.authenticator, BasicAuthenticator)
    logins = mrise.authenticator.logins
    assert logins['username'] == 'password'
    assert logins['AzureDiamond'] == 'hunter2'
    assert 'test' not in logins


def test_env_var() -> None:
    """Tests the environment variable loader."""
    with MonkeyPatch.context() as ctx:
        ctx.setenv('mytesturl', 'json://localhost')

        files = [
            StringIO("""
              configs:
                test:
                  urls:
                    - !env_var mytesturl
            """),
            StringIO("""
              configs:
                test:
                  urls:
                    - !env_var fallback json://localhost
            """)
        ]
        for file in files:
            mrise = load_config(_logger, file)
            router = mrise.router
            assert isinstance(router, SimpleRouter)
            assert len(router.senders) == 1
            key = _Key(user='test')
            sender = router.get_sender(key)
            assert sender is not None
            notifier = _make_notifier(sender.config_yaml)
            # Missing type annotation for this property as of Dec 2022.
            ap_servers = notifier.servers  # type: ignore
            assert len(ap_servers) == 1
            config = ap_servers[0]
            servers = config.servers()
            assert len(servers) == 1
            assert servers[0].url().startswith('json://localhost')

    with pytest.raises(SystemExit):
        file = StringIO("""
          configs:
            test:
              urls:
                - !env_var error
        """)
        load_config(_logger, file)


def _make_notifier(config: str):
    ap_config = AppriseConfig()
    ap_config.add_config(config, format='yaml')
    return Apprise(ap_config)
