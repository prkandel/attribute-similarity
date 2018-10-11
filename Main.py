from Grouping import Grouping
from SimilarityUtil import SimilarityUtil


def main():
    THRESHOLD = 0.95

    person1 = [15, 1.5, 25]
    person2 = [15, 1.5, 22]
    person3 = [45, 8, 1]
    person4 = [42, 7, 2]
    person5 = [41, 7.5, 1]
    person6 = [15, 8, 2.5]
    person7 = [16, 2, 24]

    persons = [person1, person2, person3, person4, person5, person6, person7]
    pairwise_similarity = get_pairwise_similarity(persons)
    grouping = Grouping(pairwise_similarity, THRESHOLD)
    groups = grouping.get_groups()

    print(groups)


def get_pairwise_similarity(persons):
    pairwise_similarity = {}
    for i in range(len(persons) - 1):
        pairwise_similarity[i + 1] = {}
        for j in range(i + 1, len(persons)):
            similarity = SimilarityUtil.get_cosine_similarity(persons[i], persons[j])
            pairwise_similarity[i + 1][j + 1] = similarity
    return pairwise_similarity


if __name__ == '__main__':
    main()
