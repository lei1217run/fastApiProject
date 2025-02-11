"""
    把两个抽象仓库导入到repository 的包中，方便后续调用

    领域模型的持久化输出模型至此结束

    具体领域模型的怎么读写？从哪里读写？都不是核心逻辑所关心的
    在六边形的内部，只需要知道通过调用这两个repository就可以对领域模型进行持久化操作即可

"""
from app.domain.repositories.post import PostRepository
from app.domain.repositories.user import UserRepository
from app.domain.repositories.codes import CodesRepository