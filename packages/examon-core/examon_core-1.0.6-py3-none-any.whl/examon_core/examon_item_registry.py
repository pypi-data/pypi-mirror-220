import logging


class ExamonItemRegistry:
    __registry = []
    __tags = []

    @classmethod
    def add(cls, quiz_item):
        logging.debug(f'Adding {quiz_item} to registry')
        cls.__registry.append(quiz_item)
        for tag in quiz_item.tags:
            if tag not in cls.__tags:
                cls.__tags.append(tag)

    @classmethod
    def reset(cls):
        cls.__registry = []
        cls.__tags = []

    @classmethod
    def registry(cls, difficulty=None, tag=None,
                 tags_any=None, tags_all=None, max_questions=None):
        def intersection(lst1, lst2):
            return list(set(lst1) & set(lst2))

        results = cls.__registry
        if tags_any is not None:
            results = [
                py_quiz_data
                for py_quiz_data in cls.__registry
                if len(intersection(tags_any, py_quiz_data.tags)) > 0
            ]
        elif tag is not None:
            results = [
                py_quiz_data
                for py_quiz_data in cls.__registry
                if tag in py_quiz_data.tags
            ]
        elif tags_all is not None:
            results = [
                py_quiz_data
                for py_quiz_data in cls.__registry
                if len(intersection(tags_all, py_quiz_data.tags)) == len(py_quiz_data.tags)
            ]
        if max_questions is not None:
            return results[0:max_questions]
        else:
            return results

    @classmethod
    def unique_tags(cls):
        return cls.__tags
