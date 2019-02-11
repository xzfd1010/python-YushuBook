def is_isbn_or_key(word):
    """
    isbn格式：isbn13 13个0-9的数字；isbn10 10个0-9的数字含有一些'-'
    :param word: 字符串
    :return: 是isbn参数或者关键字参数
    """
    isbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():
        isbn_or_key = 'isbn'
    short_word = word.replace('-', '')
    # 可能为假的条件放在前面；需要查询数据库的条件放在后面
    if '-' in word and len(short_word) == 10 and short_word.isdigit():
        isbn_or_key = 'isbn'
    return isbn_or_key
