from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 定义基础类
Base = declarative_base()

# 定义 video 数据表
class Video(Base):
    __tablename__ = 'video'
    
    id = Column(Integer, primary_key=True)
    views = Column(Integer)
    author = Column(String(255))
    video_title = Column(String(255))

# 创建 SQLite 数据库引擎
engine = create_engine('sqlite:///videoData.db', echo=True)

# 创建数据表（如果不存在的话）
Base.metadata.create_all(engine)

def insert_data(video_title, author, view_count):
    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 示例：向 video 表中插入一条记录
    new_video = Video(views=view_count, author=author, video_title=video_title)
    session.add(new_video)
    session.commit()

    # 关闭会话
    session.close()

def get_data():
    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 示例：查询 video 表中的所有记录
    videos = session.query(Video).order_by(Video.id.desc()).limit(20).all()
    
    # 关闭会话
    session.close()

    return videos

def delete_all():
    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 示例：删除 video 表中的所有记录
    session.query(Video).delete()
    session.commit()

    # 关闭会话
    session.close()

def delete_one(id):
    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 示例：删除 video 表中的所有记录
    session.query(Video).filter(Video.id == id).delete()
    session.commit()

    # 关闭会话
    session.close()