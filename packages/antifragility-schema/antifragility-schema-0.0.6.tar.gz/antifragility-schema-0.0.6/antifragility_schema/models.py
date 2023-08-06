from datetime import datetime
from enum import IntEnum
from tortoise import fields
from tortoise_api_model import Model


class ClientStatus(IntEnum):
    me = 7
    my = 5
    own = 3
    pause = 2
    wait = 1
    block = 0


class AdvStatus(IntEnum):
    defActive = 0
    active = 1
    two = 2
    old = 3
    four = 4
    notFound = 9


class OrderStatus(IntEnum):
    zero = 0
    one = 1
    two = 2
    three = 3
    done = 4
    fifth = 5
    canceled = 6
    paid_and_canceled = 7
    # COMPLETED, PENDING, TRADING, BUYER_PAYED, DISTRIBUTING, COMPLETED, IN_APPEAL, CANCELLED, CANCELLED_BY_SYSTEM


class ExType(IntEnum):
    p2p = 1
    cex = 2
    main = 3  # p2p+cex
    dex = 4
    futures = 8


class DepType(IntEnum):
    earn = 1
    stake = 2
    beth = 3


class AssetType(IntEnum):
    spot = 1
    earn = 2
    found = 3


class Country(Model):
    id = fields.SmallIntField(pk=True)
    code: int = fields.IntField(null=True)
    short: str = fields.CharField(3, unique=True, null=True)
    name: str = fields.CharField(63, unique=True, null=True)
    cur: fields.ForeignKeyRelation["Cur"] = fields.ForeignKeyField("models.Cur", related_name="countries")
    curs: fields.ReverseRelation["Cur"]


class Cur(Model):
    id = fields.SmallIntField(pk=True)
    ticker: str = fields.CharField(3, unique=True)
    rate: float = fields.FloatField(null=True)
    blocked: bool = fields.BooleanField(default=False)
    country: str = fields.CharField(63, null=True)
    exs: fields.ManyToManyRelation["Ex"] = fields.ManyToManyField("models.Ex", through="curex", backward_key="curs")  # only root pts

    pts: fields.ManyToManyRelation["Pt"]
    ptcs: fields.ReverseRelation["Ptc"]
    pairs: fields.ReverseRelation["Pair"]
    countries: fields.ReverseRelation[Country]

    _name = 'ticker'
    class Meta:
        table_description = "Fiat currencies"


class Coin(Model):
    id: int = fields.SmallIntField(pk=True)
    ticker: str = fields.CharField(15, unique=True)
    rate: float = fields.FloatField(null=True)
    is_fiat: bool = fields.BooleanField(default=False)
    # quotable: bool = fields.BooleanField(default=False)

    assets: fields.ReverseRelation["Asset"]
    deps: fields.ReverseRelation["Dep"]
    deps_reward: fields.ReverseRelation["Dep"]

    def repr(self):
        return f"{self.ticker}{self.is_fiat and ' (fiat)' or ''}"

    class Meta:
        table_description = "Crypro coins"


class Ex(Model):
    id: int = fields.SmallIntField(pk=True)
    name: str = fields.CharField(31)
    type: ExType = fields.IntEnumField(ExType)

    curs: fields.ManyToManyRelation[Cur] # = fields.ManyToManyField("models.Cur", through="curex", backward_key="exs")
    pairs: fields.ReverseRelation["Pair"]
    deps: fields.ReverseRelation["Dep"]

    class Meta:
        table_description = "Exchanges"


class Pair(Model):
    id = fields.SmallIntField(pk=True)
    coin: fields.ForeignKeyRelation[Coin] = fields.ForeignKeyField("models.Coin", related_name="pairs")
    cur: fields.ForeignKeyRelation[Cur] = fields.ForeignKeyField("models.Cur", related_name="pairs")
    sell: bool = fields.BooleanField()
    fee: float = fields.FloatField()
    total: int = fields.IntField()
    ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex", related_name="pairs")
    ads: fields.ReverseRelation["Ad"]
    deps: fields.ReverseRelation["Dep"]
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table_description = "Coin/Currency pairs"
        unique_together = (("coin", "cur", "sell", "ex"),)

    def repr(self):
        return f"{self.coin.ticker}/{self.cur.ticker} {'SELL' if self.sell else 'BUY'}"


class User(Model):
    id: int = fields.IntField(pk=True)
    uid: str = fields.CharField(63, unique=True, null=True)
    name: str = fields.CharField(63, null=True)
    ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex", related_name="users")
    auth: {} = fields.JSONField(null=True)
    client: fields.ForeignKeyNullableRelation["Client"] = fields.ForeignKeyField("models.Client", related_name="users", null=True)
    is_active: bool = fields.BooleanField(default=True, null=True)
    updated_at: datetime = fields.DatetimeField(auto_now=True)
    orders: fields.ReverseRelation["Order"]
    ads: fields.ReverseRelation["Ad"]

    class Meta:
        table_description = "Exchange users"

    # @staticmethod
    # def defs(data: {}):
    #     return {
    #         'nickName': data['nickName'],
    #         'uid': data['userNo'],
    #         'ex_id': 1,
    #     }


class Client(Model):
    id: int = fields.SmallIntField(pk=True)
    gmail: str = fields.CharField(64, unique=True, null=True)
    status: ClientStatus = fields.IntEnumField(ClientStatus, default=ClientStatus.wait)
    users: fields.ReverseRelation[User]

    def repr(self):
        return f"Telegram user {self.id}, gmail: {self.gmail} ({self.status.name})"

    class Meta:
        table_description = "Our clients"


class Adpt(Model):
    ad: fields.ForeignKeyRelation["Ad"] = fields.ForeignKeyField("models.Ad")
    pt: fields.ForeignKeyRelation["Pt"] = fields.ForeignKeyField("models.Pt")

    class Meta:
        table_description = "P2P Advertisements - Payment methods"

class Ad(Model):
    id: int = fields.BigIntField(pk=True)
    pair: fields.ForeignKeyRelation[Pair] = fields.ForeignKeyField("models.Pair")
    price: float = fields.FloatField()
    pts: fields.ManyToManyRelation["Pt"] = fields.ManyToManyField("models.Pt", through="adpt")  # only root pts
    maxFiat: float = fields.FloatField()
    minFiat: float = fields.FloatField()
    detail: str = fields.CharField(4095, null=True)
    autoMsg: str = fields.CharField(255, null=True)
    user: fields.ForeignKeyRelation = fields.ForeignKeyField("models.User", "ads")
    status: AdvStatus = fields.IntEnumField(AdvStatus)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True, index=True)

    orders: fields.ReverseRelation["Order"]

    def repr(self):
        return f"{self.pair.repr()} {self.price}"

    class Meta:
        table_description = "P2P Advertisements"


class Pt(Model):
    name: str = fields.CharField(63)
    identifier: str = fields.CharField(63, unique=True, null=True)
    binance_id = fields.SmallIntField(unique=True, null=True)
    huobi_id = fields.SmallIntField(unique=True, null=True)
    template = fields.SmallIntField(null=True)  # default=0
    rank = fields.SmallIntField(default=0)
    type = fields.CharField(63, default='')
    group: str = fields.CharField(63, null=True)

    curs: fields.ManyToManyRelation[Cur] = fields.ManyToManyField("models.Cur", through="ptc")
    pairs: fields.ReverseRelation[Pair]
    orders: fields.ReverseRelation["Order"]
    children: fields.ReverseRelation["Pt"]
    ptcs: fields.ReverseRelation["Ptc"]

    class Meta:
        table_description = "Payment methods"


class Ptc(Model):
    pt: fields.ForeignKeyRelation[Pt] = fields.ForeignKeyField("models.Pt")
    cur: fields.ForeignKeyRelation[Cur] = fields.ForeignKeyField("models.Cur")
    blocked: fields.BooleanField = fields.BooleanField(default=False)
    fiats: fields.ReverseRelation["Fiat"]

    class Meta:
        table_description = "Payment methods - Currencies"
        unique_together = (("pt", "cur"),)


class Fiat(Model):
    id: int = fields.IntField(pk=True)
    ptc: fields.ForeignKeyRelation[Ptc] = fields.ForeignKeyField("models.Ptc")
    pts: fields.ManyToManyRelation[Pt] = fields.ManyToManyField("models.Pt", through="ptc")
    country: fields.ForeignKeyRelation[Country] = fields.ForeignKeyField("models.Country", related_name="fiats")
    detail: str = fields.CharField(127)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", "fiats")  # only user having client
    amount: float = fields.FloatField(default=None, null=True)
    target: float = fields.FloatField(default=None, null=True)

    orders: fields.ReverseRelation["Order"]

    def repr(self):
        return f"{self.id}: {self.ptc.pt_id} ({self.user.nickName})"

    class Meta:
        table_description = "Currency accounts balance"


class Route(Model):
    ptc_from: fields.ForeignKeyRelation[Ptc] = fields.ForeignKeyField("models.Ptc", related_name="out_routes")
    ptc_to: fields.ForeignKeyRelation[Ptc] = fields.ForeignKeyField("models.Ptc", related_name="in_routes")


class Limit(Model):
    route: fields.ForeignKeyRelation[Route] = fields.ForeignKeyField("models.Route")
    limit: int = fields.IntField(default=-1, null=True)  # '$' if unit >= 0 else 'transactions count'
    unit: int = fields.IntField(default=30)  # positive: $/days, 0: $/transaction, negative: transactions count / days
    fee: float = fields.IntField(default=0, null=True)  # on multiply Limits for one Route - fees is quanting by minimum unit if units equal, else summing


class Asset(Model):
    id: int = fields.IntField(pk=True)
    coin: fields.ForeignKeyRelation[Coin] = fields.ForeignKeyField("models.Coin", related_name="assets")
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", "assets")
    ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex", "assets")
    type: AssetType = fields.IntEnumField(AssetType)
    free: float = fields.FloatField()
    freeze: float = fields.FloatField()
    lock: float = fields.FloatField()
    target: float = fields.FloatField(default=0, null=True)

    def repr(self):
        return f'{self.coin_id} {self.free:.3g}/{self.freeze:.3g} user:{self.user_id}'

    class Meta:
        table_description = "Coin balance"
        unique_together = (("coin", "user", "ex", "type"),)


class Order(Model):
    id: int = fields.BigIntField(pk=True)
    ad: fields.ForeignKeyRelation[Ad] = fields.ForeignKeyField("models.Ad", related_name="ads")
    amount: float = fields.FloatField()
    fiat: fields.ForeignKeyRelation[Fiat] = fields.ForeignKeyField("models.Fiat", related_name="orders", null=True)
    pt: fields.ForeignKeyNullableRelation[Pt] = fields.ForeignKeyField("models.Pt", related_name="orders", null=True)
    taker: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", "orders")
    status: OrderStatus = fields.IntEnumField(OrderStatus)
    created_at = fields.DatetimeField()
    updated_in_db_at = fields.DatetimeField(auto_now=True)
    notify_pay_at = fields.DatetimeField(null=True)
    confirm_pay_at = fields.DatetimeField(null=True)

    def repr(self):
        return f'{self.amount:.3g} pt:{self.pt_id}/{self.fiat_id} {self.status.name}'

    class Meta:
        table_description = "P2P Orders"

class Dep(Model):
    id: int = fields.IntField(pk=True)
    pid: str = fields.CharField(31)  # product_id
    apr: float = fields.FloatField()
    fee: float = fields.FloatField(null=True)
    apr_is_fixed: bool = fields.BooleanField(default=False)
    duration: int = fields.SmallIntField(null=True)
    early_redeem: bool = fields.BooleanField(null=True)
    type: DepType = fields.IntEnumField(DepType)
    # mb: renewable?
    min_limit: float = fields.FloatField()
    max_limit: float = fields.FloatField(null=True)
    is_active: bool = fields.BooleanField(default=True)

    updated_at = fields.DatetimeField(auto_now=True, index=True)

    coin: fields.ForeignKeyRelation[Coin] = fields.ForeignKeyField("models.Coin", related_name="deps")
    reward_coin: fields.ForeignKeyRelation[Coin] = fields.ForeignKeyField("models.Coin", related_name="deps_reward", null=True)
    ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex", related_name="deps")
    # investments: fields.ReverseRelation["Investment"]

    def repr(self):
        return f'{self.pid} {self.apr*100:.3g}% {f"{self.duration}d" if self.duration and self.duration>0 else "flex"}'

    class Meta:
        table_description = "Investment products"
        unique_together = (("pid", "type", "ex"),)
