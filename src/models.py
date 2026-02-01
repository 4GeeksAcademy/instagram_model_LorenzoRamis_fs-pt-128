from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    
    posts: Mapped[list["Post"]] = relationship(back_populates="user_post")
    comment: Mapped[list['Comment']] = relationship(back_populates = 'user_comment')
    follower: Mapped[list['Follower']] = relationship('Follower', foreign_keys='Follower.user_to_id', back_populates='user_to')

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int]= mapped_column(ForeignKey('user.id'))
    user_to_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user_to: Mapped['User'] = relationship('User', foreign_keys=[user_to_id], back_populates='followers')

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
   
    user_post: Mapped["User"] = relationship(back_populates="posts")
    media_post: Mapped[list['Media']] = relationship(back_populates="media_pots")
    comment_post: Mapped[list['Comment']]= relationship(back_populates='comment_post')

class Media(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
   
    media_pots: Mapped['Post']= relationship(back_populates='media_post')

    def serialize(self):
        return{
            'id': self.id,
            'url': self.url,
        }

class Comment(db.Model):
    id: Mapped[int]= mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(450), nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id')) 
    post_id: Mapped[int]= mapped_column(ForeignKey('post.id'))
    
    user_comment: Mapped['User']= relationship(back_populates='comments')
    comment_post: Mapped['Post'] = relationship(back_populates='comment_post')

    def serialize(self):
        return{
            'id': self.id,
            'comment_text': self.comment_text,
            'author_id': self.author_id
        }