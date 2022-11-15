from ninja import NinjaAPI

from users.api                    import router as users_router
from account_books.api.books      import router as account_books_router
from account_books.api.categories import router as account_book_categories_router


api = NinjaAPI()

api.add_router('/users', users_router)
api.add_router('/account-books', account_books_router)
api.add_router('/account-books/categories', account_book_categories_router)