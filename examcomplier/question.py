class Question:
    def __init__(self, question, answer, topics):
        self._question = question
        self._answer = answer
        self._topic = topics

    @property
    def question(self):
        return self._question

    @question.setter
    def question(self, question):
        self._question = question

    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, topic):
        self._topic = topic