from SentenceReadingAgent import SentenceReadingAgent, Ontology
import time


def test():
    # This will test your SentenceReadingAgent
    # with nine initial test cases.

    test_agent = SentenceReadingAgent()

    sentence_1 = "Ada brought a short note to Irene."
    question_1 = "Who brought the note?"
    question_2 = "What did Ada bring?"
    question_3 = "Who did Ada bring the note to?"
    question_4 = "How long was the note?"

    sentence_2 = "David and Lucy walk one mile to go to school every day at 8:00AM when there is no snow."
    question_5 = "Who does Lucy go to school with?"
    question_6 = "Where do David and Lucy go?"
    question_7 = "How far do David and Lucy walk?"
    question_8 = "How do David and Lucy get to school?"
    question_9 = "At what time do David and Lucy walk to school?"
    start = time.time()
    print(test_agent.solve(sentence_1, question_1))  # Ada
    end = time.time()
    print(end - start)
    start = time.time()
    print(test_agent.solve(sentence_1, question_2))  # "note" or "a note"
    end = time.time()
    print(end - start)
    start = time.time()
    print(test_agent.solve(sentence_1, question_3))  # "Irene"
    end = time.time()
    print(end - start)
    start = time.time()
    print(test_agent.solve(sentence_1, question_4))  # "short"
    end = time.time()
    print(end - start)

    start = time.time()
    print(test_agent.solve(sentence_2, question_5))  # "David"
    end = time.time()
    print(end - start)
    start = time.time()
    print(test_agent.solve(sentence_2, question_6))  # "school"
    end = time.time()
    print(end - start)
    start = time.time()
    print(test_agent.solve(sentence_2, question_7))  # "mile" or "a mile"
    end = time.time()
    print(end - start)
    start = time.time()
    print(test_agent.solve(sentence_2, question_8))  # "walk"
    end = time.time()
    print(end - start)
    start = time.time()
    print(test_agent.solve(sentence_2, question_9))  # "8:00AM"
    end = time.time()
    print(end - start)


if __name__ == "__main__":
    test()
