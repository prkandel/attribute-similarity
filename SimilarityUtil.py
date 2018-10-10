import math


class SimilarityUtil:
    def __init__(self):
        pass

    @staticmethod
    def get_euclidean_distance(vect1, vect2):
        return math.sqrt(sum((vect1[i] - vect2[i])**2 for i in range(0, len(vect1))))

    @staticmethod
    def get_cosine_similarity(vect1, vect2):
        mag1 = SimilarityUtil.get_magnitude(vect1)
        mag2 = SimilarityUtil.get_magnitude(vect2)
        dot_product = sum(vect1[i] * vect2[i] for i in range(0, len(vect1)))
        return dot_product / (mag1 * mag2)

    @staticmethod
    def normalize(x, x_min, x_max):
        return (x - x_min) / (x_max - x_min)

    @staticmethod
    def normalize_vector(v):
        magnitude = SimilarityUtil.get_magnitude(v)
        return [v[i] / magnitude for i in range(0, len(v))]

    @staticmethod
    def get_magnitude(v):
        return math.sqrt(sum(v[i] * v[i] for i in range(0, len(v))))

    @staticmethod
    def get_mixed_similarity(vect1, vect2):
        return 1 - ((1-SimilarityUtil.get_cosine_similarity(vect1,vect2)) * SimilarityUtil.get_euclidean_distance(vect1,vect2))
