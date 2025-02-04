from pathlib import Path
from shutil import copyfile
from typing import TYPE_CHECKING, Callable, List, Optional, Union
from unittest.mock import patch

import pytest

from rotkehlchen.assets.asset import EvmToken
from rotkehlchen.assets.resolver import AssetResolver
from rotkehlchen.constants.assets import A_BTC, A_ETH, A_EUR
from rotkehlchen.fval import FVal
from rotkehlchen.globaldb import GlobalDBHandler
from rotkehlchen.globaldb.upgrades.manager import UPGRADES_LIST
from rotkehlchen.globaldb.utils import GLOBAL_DB_VERSION
from rotkehlchen.history.types import HistoricalPrice, HistoricalPriceOracle
from rotkehlchen.types import Price, Timestamp

if TYPE_CHECKING:
    from rotkehlchen.utils.upgrades import UpgradeRecord


@pytest.fixture(name='generatable_user_ethereum_tokens')
def fixture_generatable_user_ethereum_tokens() -> bool:
    return False


@pytest.fixture(name='user_ethereum_tokens')
def fixture_user_ethereum_tokens() -> Optional[Union[List[EvmToken], Callable]]:
    return None


@pytest.fixture(name='reload_user_assets')
def fixture_reload_user_assets() -> bool:
    return True


@pytest.fixture(name='target_globaldb_version')
def fixture_target_globaldb_version() -> int:
    return GLOBAL_DB_VERSION


@pytest.fixture(name='globaldb_upgrades')
def fixture_globaldb_upgrades() -> List['UpgradeRecord']:
    return UPGRADES_LIST


def create_globaldb(
        data_directory,
        sql_vm_instructions_cb,
) -> GlobalDBHandler:
    # Since this is a singleton and we want it initialized everytime the fixture
    # is called make sure its instance is always starting from scratch
    GlobalDBHandler._GlobalDBHandler__instance = None  # type: ignore

    handler = GlobalDBHandler(data_dir=data_directory, sql_vm_instructions_cb=sql_vm_instructions_cb)  # noqa: E501
    return handler


def _initialize_fixture_globaldb(
        globaldb_version,
        tmpdir_factory,
        sql_vm_instructions_cb: int,
        reload_user_assets,
        target_globaldb_version,
        globaldb_upgrades,
) -> GlobalDBHandler:
    # clean the previous resolver memory cache, as it
    # may have cached results from a discarded database
    AssetResolver().clean_memory_cache()
    root_dir = Path(__file__).resolve().parent.parent.parent
    if globaldb_version is None:  # no specific version -- normal test
        source_db_path = root_dir / 'data' / 'global.db'
    else:
        source_db_path = root_dir / 'tests' / 'data' / f'v{globaldb_version}_global.db'
    new_data_dir = Path(tmpdir_factory.mktemp('test_data_dir'))
    new_global_dir = new_data_dir / 'global_data'
    new_global_dir.mkdir(parents=True, exist_ok=True)
    copyfile(source_db_path, new_global_dir / 'global.db')
    if reload_user_assets is False:
        with (
            patch('rotkehlchen.globaldb.upgrades.manager.UPGRADES_LIST', globaldb_upgrades),
            patch('rotkehlchen.globaldb.utils.GLOBAL_DB_VERSION', target_globaldb_version),
        ):
            return create_globaldb(new_data_dir, sql_vm_instructions_cb)
    return create_globaldb(new_data_dir, sql_vm_instructions_cb)


@pytest.fixture(scope='session', name='session_globaldb')
def fixture_session_globaldb(
        tmpdir_factory,
        session_sql_vm_instructions_cb,
):
    return _initialize_fixture_globaldb(
        globaldb_version=None,
        tmpdir_factory=tmpdir_factory,
        sql_vm_instructions_cb=session_sql_vm_instructions_cb,
        reload_user_assets=True,
        target_globaldb_version=GLOBAL_DB_VERSION,
        globaldb_upgrades=[],
    )


@pytest.fixture(name='globaldb')
def fixture_globaldb(
        globaldb_version,
        tmpdir_factory,
        sql_vm_instructions_cb,
        reload_user_assets,
        target_globaldb_version,
        globaldb_upgrades,
):
    return _initialize_fixture_globaldb(
        globaldb_version=globaldb_version,
        tmpdir_factory=tmpdir_factory,
        sql_vm_instructions_cb=sql_vm_instructions_cb,
        reload_user_assets=reload_user_assets,
        target_globaldb_version=target_globaldb_version,
        globaldb_upgrades=globaldb_upgrades,
    )


@pytest.fixture(name='globaldb_version')
def fixture_globaldb_version() -> Optional[int]:
    return None


@pytest.fixture(name='historical_price_test_data')
def fixture_historical_price_test_data(globaldb):
    data = [HistoricalPrice(
        from_asset=A_BTC,
        to_asset=A_EUR,
        source=HistoricalPriceOracle.CRYPTOCOMPARE,
        timestamp=Timestamp(1428994442),
        price=Price(FVal(210.865)),
    ), HistoricalPrice(
        from_asset=A_ETH,
        to_asset=A_EUR,
        source=HistoricalPriceOracle.CRYPTOCOMPARE,
        timestamp=Timestamp(1439048640),
        price=Price(FVal(1.13)),
    ), HistoricalPrice(
        from_asset=A_ETH,
        to_asset=A_EUR,
        source=HistoricalPriceOracle.CRYPTOCOMPARE,
        timestamp=Timestamp(1511626623),
        price=Price(FVal(396.56)),
    ), HistoricalPrice(
        from_asset=A_ETH,
        to_asset=A_EUR,
        source=HistoricalPriceOracle.COINGECKO,
        timestamp=Timestamp(1511626622),
        price=Price(FVal(394.56)),
    ), HistoricalPrice(
        from_asset=A_ETH,
        to_asset=A_EUR,
        source=HistoricalPriceOracle.CRYPTOCOMPARE,
        timestamp=Timestamp(1539713117),
        price=Price(FVal(178.615)),
    ), HistoricalPrice(
        from_asset=A_BTC,
        to_asset=A_EUR,
        source=HistoricalPriceOracle.CRYPTOCOMPARE,
        timestamp=Timestamp(1539713117),
        price=Price(FVal(5626.17)),
    ), HistoricalPrice(
        from_asset=A_ETH,
        to_asset=A_EUR,
        source=HistoricalPriceOracle.COINGECKO,
        timestamp=Timestamp(1618481088),
        price=Price(FVal(2044.76)),
    ), HistoricalPrice(
        from_asset=A_ETH,
        to_asset=A_EUR,
        source=HistoricalPriceOracle.COINGECKO,
        timestamp=Timestamp(1618481095),
        price=Price(FVal(2045.76)),
    ), HistoricalPrice(
        from_asset=A_ETH,
        to_asset=A_EUR,
        source=HistoricalPriceOracle.COINGECKO,
        timestamp=Timestamp(1618481101),
        price=Price(FVal(2049.76)),
    ), HistoricalPrice(
        from_asset=A_BTC,
        to_asset=A_EUR,
        source=HistoricalPriceOracle.COINGECKO,
        timestamp=Timestamp(1618481102),
        price=Price(FVal(52342.5)),
    ), HistoricalPrice(
        from_asset=A_ETH,
        to_asset=A_EUR,
        source=HistoricalPriceOracle.COINGECKO,
        timestamp=Timestamp(1618481103),
        price=Price(FVal(2049.96)),
    ), HistoricalPrice(
        from_asset=A_ETH,
        to_asset=A_EUR,
        source=HistoricalPriceOracle.COINGECKO,
        timestamp=Timestamp(1618481196),
        price=Price(FVal(2085.76)),
    )]
    globaldb.add_historical_prices(data)
