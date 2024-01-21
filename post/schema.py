import graphene
from graphene_django.types import DjangoObjectType
from .models import Post, Comment


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class Query(graphene.ObjectType):
    posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.Int())

    def resolve_posts(self, info, **kwargs):
        return Post.objects.all()

    def resolve_post(self, info, id):
        return Post.objects.get(pk=id)


class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        description = graphene.String()
        publish_date = graphene.String()
        author = graphene.String()

    post = graphene.Field(lambda: PostType)

    def mutate(self, info, title, description, publish_date, author):
        post = Post.objects.create(title=title, description=description, publish_date=publish_date, author=author)
        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        title = graphene.String()
        description = graphene.String()
        publish_date = graphene.String()
        author = graphene.String()

    post = graphene.Field(lambda: PostType)

    def mutate(self, info, id, title, description, publish_date, author):
        post = Post.objects.get(pk=id)
        post.title = title
        post.description = description
        post.publish_date = publish_date
        post.author = author
        post.save()
        return UpdatePost(post=post)


class CreateComment(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int()
        text = graphene.String()
        author = graphene.String()

    comment = graphene.Field(lambda: CommentType)

    def mutate(self, info, post_id, text, author):
        post = Post.objects.get(pk=post_id)
        comment = Comment.objects.create(post=post, text=text, author=author)
        return CreateComment(comment=comment)


class DeleteComment(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            Comment.objects.get(pk=id).delete()
            success = True
        except Comment.DoesNotExist:
            success = False
        return DeleteComment(success=success)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    create_comment = CreateComment.Field()
    delete_comment = DeleteComment.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
