import inspect
import time
from abc import abstractmethod
from typing import Optional, Literal, NamedTuple, no_type_check, Union, Dict, Any, TypeVar

from pydantic import BaseModel


class BaseModelWithSetter(BaseModel):
    """
    可以使用@property.setter的BaseModel

    目前pydantic 1.10.7 无法使用@property.setter
    issue: https://github.com/pydantic/pydantic/issues/1577#issuecomment-790506164
    """

    @no_type_check
    def __setattr__(self, name, value):
        try:
            super().__setattr__(name, value)
        except ValueError as e:
            setters = inspect.getmembers(
                self.__class__,
                predicate=lambda x: isinstance(x, property) and x.fset is not None
            )
            for setter_name, func in setters:
                if setter_name == name:
                    object.__setattr__(self, name, value)
                    break
            else:
                raise e


class BaseModelWithUpdate(BaseModel):
    """
    可以使用update方法的BaseModel
    """
    _T = TypeVar("_T", bound=BaseModel)

    @abstractmethod
    def update(self, obj: Union[_T, Dict[str, Any]]) -> _T:
        """
        更新数据对象

        :param obj: 新的数据对象或属性字典
        :raise TypeError
        """
        if isinstance(obj, type(self)):
            obj = obj.dict()
        items = filter(lambda x: x[0] in self.__fields__, obj.items())
        for k, v in items:
            setattr(self, k, v)
        return self


class Good(BaseModelWithUpdate):
    """
    商品数据
    """
    type: int
    """为 1 时商品只有在指定时间开放兑换；为 0 时商品任何时间均可兑换"""
    next_time: Optional[int]
    """为 0 表示任何时间均可兑换或兑换已结束"""
    status: Optional[Literal["online", "not_in_sell"]]
    sale_start_time: Optional[str]
    time_by_detail: Optional[int]
    next_num: Optional[int]
    account_exchange_num: int
    """已经兑换次数"""
    account_cycle_limit: int
    """最多可兑换次数"""
    account_cycle_type: str
    """限购类型 Literal["forever", "month", "not_limit"]"""
    game_biz: Optional[str]
    """商品对应的游戏区服（如 hk4e_cn）（单独查询一个商品时）"""
    game: Optional[str]
    """商品对应的游戏"""
    unlimit: Optional[bool]
    """是否为不限量商品"""

    # 以下为实际会用到的属性

    name: Optional[str]
    """商品名称（单独查询一个商品时）"""
    goods_name: Optional[str]
    """商品名称（查询商品列表时）"""

    goods_id: str
    """商品ID(Good_ID)"""

    price: int
    """商品价格"""

    icon: str
    """商品图片链接"""

    def update(self, obj: Union["Good", Dict[str, Any]]) -> "Good":
        """
        更新商品信息

        :param obj: 新的商品数据
        :raise TypeError
        """
        return super().update(obj)

    @property
    def time(self):
        """
        兑换时间

        :return:
        如果返回`None`，说明任何时间均可兑换或兑换已结束。
        如果返回`0`，说明该商品需要调用获取详细信息的API才能获取兑换时间
        """
        # "next_time" 为 0 表示任何时间均可兑换或兑换已结束
        if self.next_time == 0:
            return None
        elif self.status == "not_in_sell" and self.sale_start_time is not None:
            return int(self.sale_start_time)
        elif self.status == "online":
            return self.next_time
        else:
            return 0

    @property
    def time_text(self):
        """
        商品的兑换时间文本

        :return:
        如果返回`None`，说明需要进一步查询商品详细信息才能获取兑换时间
        """
        if self.time_end:
            return "已结束"
        elif self.time == 0:
            return None
        elif self.time_limited:
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.time))
        else:
            return "任何时间"

    @property
    def stoke_text(self):
        """
        商品的库存文本
        """
        if self.time_end:
            return "无"
        elif self.time_limited:
            return str(self.num)
        else:
            return "不限"

    @property
    def time_limited(self):
        """
        是否为限时商品
        """
        # 不限量被认为是不限时商品
        return not self.unlimit

    @property
    def time_end(self):
        """
        兑换是否已经结束
        """
        return self.next_time == 0

    @property
    def num(self):
        """
        库存
        如果返回`None`，说明库存不限
        """
        if self.type != 1 and self.next_num == 0:
            return None
        else:
            return self.next_num

    @property
    def limit(self):
        """
        限购，返回元组 (已经兑换次数, 最多可兑换次数, 限购类型)
        """
        return (self.account_exchange_num,
                self.account_cycle_limit, self.account_cycle_type)

    @property
    def is_virtual(self):
        """
        是否为虚拟商品
        """
        return self.type == 2

    @property
    def general_name(self):
        return self.name or self.goods_name


class GameRecord(BaseModel):
    """
    用户游戏数据
    """
    region_name: str
    """服务器区名"""

    game_id: int
    """游戏ID"""

    level: int
    """用户游戏等级"""

    region: str
    """服务器区号"""

    game_role_id: str
    """用户游戏UID"""

    nickname: str
    """用户游戏昵称"""


class GameInfo(BaseModel):
    """
    游戏信息数据
    """
    # ABBR_TO_ID: Dict[int, Tuple[str, str]] = {}
    # '''
    # 游戏ID(game_id)与缩写和全称的对应关系
    # >>> {游戏ID, (缩写, 全称)}
    # '''
    id: int
    """游戏ID"""

    app_icon: str
    """游戏App图标链接(大)"""

    op_name: str
    """游戏代号(英文数字, 例如hk4e)"""

    en_name: str
    """游戏代号2(英文数字, 例如ys)"""

    icon: str
    """游戏图标链接(圆形, 小)"""

    name: str
    """游戏名称"""


class Address(BaseModel):
    """
    地址数据
    """
    connect_areacode: str
    """电话区号"""
    connect_mobile: str
    """电话号码"""

    # 以下为实际会用到的属性

    province_name: str
    """省"""

    city_name: str
    """市"""

    county_name: str
    """区/县"""

    addr_ext: str
    """详细地址"""

    connect_name: str
    """收货人姓名"""

    id: str
    """地址ID"""

    @property
    def phone(self) -> str:
        """
        联系电话(包含区号)
        """
        return self.connect_areacode + " " + self.connect_mobile


class MmtData(BaseModel):
    """
    短信验证码-人机验证任务申请-返回数据
    """
    challenge: Optional[str]
    gt: str
    mmt_key: str
    new_captcha: bool
    risk_type: Optional[str]
    """任务类型，如滑动拼图 slide"""
    success: Optional[int]
    use_v4: Optional[bool]
    """是否使用极验第四代 GT4"""


class BaseApiStatus(BaseModel):
    """
    API返回结果基类
    """
    success = False
    """成功"""
    network_error = False
    """连接失败"""
    incorrect_return = False
    """服务器返回数据不正确"""
    login_expired = False
    """登录失效"""
    need_verify = False
    """需要进行人机验证"""
    invalid_ds = False
    """Headers DS无效"""

    def __bool__(self):
        if self.success:
            return True
        else:
            return False


class CreateMobileCaptchaStatus(BaseApiStatus):
    """
    发送短信验证码 返回结果
    """
    incorrect_geetest = False
    """人机验证结果数据无效"""


class GetCookieStatus(BaseApiStatus):
    """
    获取Cookie 返回结果
    """
    incorrect_captcha = False
    """验证码错误"""
    missing_login_ticket = False
    """Cookies 缺少 login_ticket"""
    missing_bbs_uid = False
    """Cookies 缺少 bbs_uid (stuid, ltuid, ...)"""
    missing_cookie_token = False
    """Cookies 缺少 cookie_token"""
    missing_stoken = False
    """Cookies 缺少 stoken"""
    missing_stoken_v1 = False
    """Cookies 缺少 stoken_v1"""
    missing_stoken_v2 = False
    """Cookies 缺少 stoken_v2"""
    missing_mid = False
    """Cookies 缺少 mid"""


class GetGoodDetailStatus(BaseApiStatus):
    """
    获取商品详细信息 返回结果
    """
    good_not_existed = False


class ExchangeStatus(BaseApiStatus):
    """
    兑换操作 返回结果
    """
    missing_stoken = False
    """商品为游戏内物品，但 Cookies 缺少 stoken"""
    missing_mid = False
    """商品为游戏内物品，但 stoken 为 'v2' 类型同时 Cookies 缺少 mid"""
    missing_address = False
    """商品为实体物品，但未配置收货地址"""
    missing_game_uid = False
    """商品为游戏内物品，但未配置对应游戏的账号UID"""
    unsupported_game = False
    """暂不支持兑换对应分区/游戏的商品"""
    failed_getting_game_record = False
    """获取用户 GameRecord 失败"""
    init_required = False
    """未进行兑换任务初始化"""
    account_not_found = False
    """账号不存在"""


class GetFpStatus(BaseApiStatus):
    """
    兑换操作 返回结果
    """
    invalid_arguments = False
    """参数错误"""


GeetestResult = NamedTuple("GeetestResult", validate=str, seccode=str)
"""人机验证结果数据"""


class GeetestResultV4(BaseModel):
    """
    GEETEST GT4 人机验证结果数据
    """
    captcha_id: str
    lot_number: str
    pass_token: str
    gen_time: str
    captcha_output: str
