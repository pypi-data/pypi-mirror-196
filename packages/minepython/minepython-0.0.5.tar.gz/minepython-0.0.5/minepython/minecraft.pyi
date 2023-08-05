
from vec3 import Vec3
from minecollection import *
from typing import Union, Optional, Tuple


class CmdPlayer:
    """
    玩家相关的类型
    """
    def getPos(self) -> Vec3:
        """
        获得玩家的位置
        返回Vec3对象
        """

    def setPos(self, x: Union[int, float], y: Union[int, float], z: Union[int, float]) -> None:
        """
        将玩家移动至x,y,z坐标位置
        """

    def setItems(self, itemName: 物品, slot: 槽位, count: int) -> None:
        """
        获得物品
        itemName：物品名
        slot：槽位设置
        count：范围从1-64
        """

    def setNarutoRun(self, activate:bool)->None:
        """
        activate只能设置为True或False
        当activate设置为True就可以像忍者一样奔跑
        """

    def getLookAngle(self, offset:int=0)->Vec3:
        """
        获得玩家的朝向
        返回一个Vec3数据表示x,y,z三个方向的值，并且数值做了归一化，使得根号下(x^2+y^2+z^2)等于1
        """

class CmdEvents:
    """
    事件相关的类型
    """
    def getKeyReturn(self)->Tuple[Optional[str],Optional[str],Optional[float]]:
        """
        该方法有3个返回值key_on, key_name, key_t
        key_on表示按键状态：
            KEY_ON：按键按下
            KEY_OFF：按键松开
            MOUSE_ON：鼠标按下
            MOUSE_OFF：鼠标松开
            MOUSE_SCROLL：鼠标滚轮转动
        key_name表示按键名称
        key_t表示按键从按下到松开的持续时长，单位是秒，KEY_ON,MOUSE_ON,MOUSE_SCROLL状态下key_t为0
        没有检测到按键活动时key_on, key_name, key_t都返回None值
        """

class Minecraft:
    player : CmdPlayer
    events : CmdEvents

    def postToChat(self, msg: str) -> None:
        """
        向聊天窗口发送信息
        """

    def setBlock(self, x: Union[int, float], y: Union[int, float], z: Union[int, float], block: 方块) -> None:
        """
        在x,y,z坐标位置放置方块
        """

    def setBlocks(self, x0: Union[int, float], y0: Union[int, float], z0: Union[int, float], x1: Union[int, float], y1: Union[int, float], z1: Union[int, float], block: 方块)-> None:
        """
        从x0到x1，y0到y1，z0到z1的范围内容放置方块
        """

    def getBlock(self, x: Union[int, float], y: Union[int, float], z: Union[int, float])->Union[方块, str]:
        """
        获取x,y,z坐标位置的方块
        """

    def spawnAreaParticle(self, particle:str, x:float, y:float, z:float, num:int, xoffset:float, yoffset:float, zoffset:float, speed:float)->None:
        """
        产生多个粒子，粒子的速度方向具有随机性
        particle为粒子的名称
        在x,y,z坐标位置产生粒子
        num为粒子数量
        xoffset,yoffset,zoffset为粒子产生出来时的位置偏移
        speed为粒子运动速度
        """

    def spawnSingleParticle(self, particle:str, x:float, y:float, z:float, xv:float, yv:float, zv:float) -> None:
        """
       产生1个粒子
       particle为粒子的名称
       在x,y,z坐标位置产生粒子，xv,yv,zv为粒子在3个方向的速度
       """

class Entity:
    """

    """

