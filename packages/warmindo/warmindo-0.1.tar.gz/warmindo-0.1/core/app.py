from warmindo import Warmindo
from .middleware import Middleware
from .routing import Router
from .database_config import DATABASE_URI
from .models import db

app = Warmindo()
router = Router()
app.router = router

router.add_route('/', home)
router.add_route('/post/<int:post_id>', show_post)

app.add_middleware(Middleware)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db.init_app(app)

if __name__ == '__main__':
    app.run()