from typing import Tuple, Any

from account_books.models import AccountBook, AccountBookCategory, AccountBookLog
from users.models         import User


class GetAccountBook:
    
    """
    description:
        - 가계부 id를 통해 가계부 객체(정보)의 존재여부 확인
        - 가계부 객체의 유저정보와 API를 요청한 유저정보가 일치하는지 확인
    """
    
    def get_book_n_check_error(account_book_id: int, user: User) -> Tuple[Any, str]:
        """
        가계부 데이터 존재 확인
        """
        try:
            book = AccountBook.objects\
                              .get(id=account_book_id)                   
        except AccountBook.DoesNotExist:
            return None, f'가계부 {account_book_id}(id)는 존재하지 않습니다.'
        
        """
        본인의 가계부인지 확인
        """
        if not user.nickname == book.user.nickname:
            return None, '다른 유저의 가계부입니다.'
        
        return book, None
    

class GetAccountBookCategory:
    """
    description:
        - 가계부 카테고리 id를 통해 카테고리 객체(정보)의 존재여부 확인
        - 가계부 카테고리 객체의 유저정보와 API를 요청한 유저정보가 일치하는지 확인
    """
    
    def get_category_n_check_error(account_book_category_id: int, user: User) -> Tuple[Any, str]:
        """
        카테고리 존재여부 확인
        """
        try:
            category = AccountBookCategory.objects\
                                          .get(id=account_book_category_id)
        except AccountBookCategory.DoesNotExist:
            return None, f'가계부 카테고리 {account_book_category_id}(id)는 존재하지 않습니다.'
        
        """
        본인의 카테고리인지 확인
        """
        if not user.nickname == category.user.nickname:
            return None, '다른 유저의 가계부 카테고리입니다.'
        
        return category, None


class GetAccountBookLog:
    """
    description:
        - 가계부 기록 id를 통해 가계부 기록 객체(정보)의 존재여부 확인
        - 가계부 기록 객체의 유저정보와 API를 요청한 유저정보가 일치하는지 확인
        - 가계부 기록이 해당 가계부의 기록인지 확인
    """
    
    def get_log_n_check_error(account_book_log_id: int, book: AccountBook, user: User) -> Tuple[Any, str]:
        """
        가계부 기록 존재여부 확인
        """
        try:
            log = AccountBookLog.objects\
                                .get(id=account_book_log_id)
        except AccountBookLog.DoesNotExist:
            return None, f'가계부 기록 {account_book_log_id}(id)는 존재하지 않습니다.'
        
        """
        본인의 가계부 기록인지 확인
        """
        if not user.nickname == log.book.user.nickname:
            return None, '다른 유저의 가계부 기록입니다.'
        
        """
        해당 가계부에 존재하는 기록인지 확인
        """
        if log not in book.logs.all():
            return None, f'해당 기록은 가계부 {book.id}(id)의 기록이 아닙니다.'
        
        return log, None