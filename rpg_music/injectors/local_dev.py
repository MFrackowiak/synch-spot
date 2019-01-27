from injector import Injector

from rpg_music.users.repositories.user.redis import RedisUserRepository
from rpg_music.users.repositories.user_auth.redis import RedisUserAuthRepository

injector = Injector([RedisUserRepository(), RedisUserAuthRepository()])
