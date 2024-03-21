def greeting(language, times):
    if language.lower() == "english":
        return "hello\n" * times
    elif language.lower() == "chinese":
        return "ni hao\n" * times
    elif language.lower() == "russian":
        return "privet\n" * times
    else:
        return "wrong language"


language, times = input(), int(input())
print(greeting(language, times))
