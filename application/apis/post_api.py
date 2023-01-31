from apis import *

post_get = {
    'title': fields.String,
    'content': fields.String,
    'username': fields.String,
    'last_modified': fields.DateTime,
}
# Url: /api/posts, /api/posts/<post_id>
class PostAPI(Resource):
    @marshal_with(post_get)
    def get(self,post_id):
        post = Post.query.filter_by(id=post_id).first()
        if post:
            return post
        else:
            return '', 404

    def post(self):
        title = request.form['title']
        content = request.form['post_content']
        author = current_user
        post = Post(title=title, content=content, author=author)
        db.session.add(post)
        db.session.flush()
        image = request.files['post_pic']
        if image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = f"static/uploads/{filename}"
            image = Image(url=image_url, post_id=post.id)
            db.session.add(image)
        db.session.commit()
        return '', 200

    def put(self,post_id):
        print(current_user.username)
        return {'post_id': post_id}

    def delete(self,post_id):
        pass


class Feed(Resource):
    @marshal_with(post_get)
    def get(self):
        try:
           
            user = User.query.filter_by(username=current_user.username).first()
            if not user:
                return {'message':f"user with name {current_user} does not exist"}, 404
            
            
            following = user.following
           
            posts = []
            for follow in following:
                for post in follow.posts:
                    posts.append(post)
            print(posts)
            print('-------------------------')
            try:
                sorted_posts = sorted(posts, key=lambda post: post.date_posted, reverse=True)
            except Exception as e:
                    print('Error occured here:',str(e))
                    return {'message':"Successfully unfollowed user"}, 400

            print('-------------------------')
            return sorted_posts, 200
        except Exception as e:
            return jsonify(message=f"Error while trying to fetch feed: {e}"), 500
