from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column, ForeignKey, Table, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


follower_table = Table(
    "follower",
    db.metadata,
    Column("follower_id", ForeignKey("user.id"), primary_key=True),
    Column("followed_id", ForeignKey("user.id"), primary_key=True),
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    
    posts: Mapped[list["Post"]] = relationship(back_populates="user_post")
    comments: Mapped[list['Comment']] = relationship(back_populates = 'user_comment')

    followers: Mapped[list['User']] = relationship(
        'User', 
        secondary=follower_table, 
        primaryjoin = (follower_table.c.follower_id == id), 
        secondaryjoin = (follower_table.c.followed_id == id),  
        back_populates='following')
    
    following: Mapped[list['User']] = relationship(
        'User', 
        secondary=follower_table, 
        primaryjoin = (follower_table.c.followed_id == id), 
        secondaryjoin = (follower_table.c.follower_id == id), 
        back_populates='followers')

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
   
    user_post: Mapped["User"] = relationship(back_populates="posts")
    media_post: Mapped[list['Media']] = relationship(back_populates="media_post")
    comment_post: Mapped[list['Comment']]= relationship(back_populates='comment_post')

class Media(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
   
    media_post: Mapped['Post']= relationship(back_populates='media_post')

class Comment(db.Model):
    id: Mapped[int]= mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(450), nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id')) 
    post_id: Mapped[int]= mapped_column(ForeignKey('post.id'))
    
    user_comment: Mapped['User']= relationship(back_populates='comments')
    comment_post: Mapped['Post'] = relationship(back_populates='comment_post')
