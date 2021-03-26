from enum import Enum


class LockShape(Enum):
    EnemyR15H10HC = "CircleLockEnemyR15H10HC"
    Enemy = "CircleLockEnemy"
    EnemyAmborFly = "CircleLockEnemyAmborFly"
    EnemyR10 = "CircleLockEnemyR10"
    EnemyR8H6HC = "CircleLockEnemyR8H6HC"
    EnemyR10H6HC = "CircleLockEnemyR10H6HC"
    EnemyR5H6HC = "CircleLockEnemyR5H6HC"
    EnemyR5H10HC = "CircleLockEnemyR5H10HC"


class DragType(Enum):
    ROTATE_CAMERA = "DRAG_ROTATE_CAMERA"
    ROTATE_CHARACTER = "DRAG_ROTATE_CHARACTER"
