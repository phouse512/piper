from decimal import *

from poller.models import Votes
from poller.models import Answers
from poller.models import Poll
from poller.models import Users
from poller.models import Scores

getcontext().prec = 3


def score_poll(poll_id, correct_id, save_scores): #poll_id: integer, save_scores: Bool
    existing_poll = Poll.objects.filter(id=poll_id).first()
    if not existing_poll:
        return "poll doesn't exist"

    all_answers = Answers.objects.filter(poll=existing_poll).all()

    # get total number of answers
    all_votes = Votes.objects.filter(poll=existing_poll).all()

    # verify correct id is here
    exists = False
    for answer in all_answers:
        if answer.id == correct_id:
            exists = True
            break

    if not exists:
        return "correct answer doesn't exist"

    right_answer_score = 0
    wrong_answers_score = 0
    for answer in all_answers:
        if answer.id == correct_id:
            # this is the right answer, calculate accordingly

            percentage = Decimal(len(answer.votes.all()))/Decimal(len(all_votes))
            weighted_add = Decimal(existing_poll.weight) * Decimal(.1)
            print weighted_add
            print(percentage)

            right_answer_score = Decimal(.5) + (1 - percentage) + weighted_add

            print("right answer: " + str(right_answer_score))

        else:
            # wrong answer
            wrong_answers_score = Decimal(-.25) - (1 - (Decimal(len(answer.votes.all()))/Decimal(len(all_votes)))) \
                                  - (Decimal(existing_poll.weight) * Decimal(.1))

            print("wrong answer: " + str(wrong_answers_score))

    if not save_scores:
        return "not saving scores"

    # time to iterate over votes and create scores objects
    for vote in all_votes:
        if vote.answer.id == correct_id:
            points_to_add = right_answer_score
        else:
            points_to_add = wrong_answers_score

        new_score = Scores.objects.create(
            points=points_to_add,
            vote=vote,
            user=vote.user
        )

        vote.user.points_total += points_to_add
        vote.user.save()