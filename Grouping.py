class Grouping:
    def __init__(self):
        pass

    @staticmethod
    def get_groups(pairwise_similarity, threshold):
        groups = []
        ungrouped = Grouping.initialize_ungrouped(pairwise_similarity)
        for i in pairwise_similarity:
            for j in pairwise_similarity[i]:
                if pairwise_similarity[i][j] >= threshold:
                    if i in ungrouped and j in ungrouped:
                        groups.append([i, j])
                        ungrouped.remove(i)
                        ungrouped.remove(j)
                    elif Grouping.get_group_number(i, groups) is not None and Grouping.get_group_number(j,groups) is not None:
                        group_number_1 = Grouping.get_group_number(i, groups)
                        group_number_2 = Grouping.get_group_number(j, groups)
                        if group_number_1 != group_number_2:
                            if Grouping.check_pairwise_similarity_for_groups(groups, group_number_1, group_number_2, pairwise_similarity, threshold):
                                groups = Grouping.merge_groups(groups, group_number_1, group_number_2)
                    else:
                        if Grouping.get_group_number(i, groups) is not None:
                            existing_group = groups[Grouping.get_group_number(i, groups)]
                            existing_group_number = Grouping.get_group_number(i, groups)
                            isolated = j
                        else:
                            existing_group = groups[Grouping.get_group_number(j, groups)]
                            existing_group_number = Grouping.get_group_number(j, groups)
                            isolated = i
                        if Grouping.check_similarity_with_group(existing_group, isolated, pairwise_similarity, threshold):
                            groups[existing_group_number].append(isolated)
                            ungrouped.remove(isolated)
        groups = Grouping.add_all_ungrouped(groups, ungrouped)
        return groups



    @staticmethod
    def get_group_number(i, groups):
        for idx, group in enumerate(groups):
            if i in group:
                return idx
        return None

    @staticmethod
    def check_pairwise_similarity_for_groups(groups, group_number_1, group_number_2, pairwise_similarity, threshold):
        for x in groups[group_number_1]:
            for y in groups[group_number_2]:
                if x in pairwise_similarity and y in pairwise_similarity[x]:
                    similarity = pairwise_similarity[x][y]
                elif y in pairwise_similarity and x in pairwise_similarity[y]:
                    similarity = pairwise_similarity[y][x]

                if similarity < threshold:
                    return False
        return True;

    @staticmethod
    def check_similarity_with_group(existing_group, isolated, pairwise_similarity, threshold):
        for i in existing_group:
            if i in pairwise_similarity and isolated in pairwise_similarity[i]:
                similarity = pairwise_similarity[i][isolated]
            elif isolated in pairwise_similarity and i in pairwise_similarity[isolated]:
                similarity = pairwise_similarity[isolated][i]
            if similarity < threshold:
                return False
        return True;

    @staticmethod
    def merge_groups(groups, group_number_1, group_number_2):
        groups[group_number_1] = groups[group_number_1]+groups[group_number_2]
        groups.remove(groups[group_number_2])
        return groups

    @staticmethod
    def add_all_ungrouped(groups, ungrouped):
        for obj in ungrouped:
            groups.append([obj])
        return groups


    @staticmethod
    def initialize_ungrouped(pairwise_similarity):
        ungrouped = set([])
        for i in pairwise_similarity:
            ungrouped.add(i)
            for j in pairwise_similarity[i]:
                ungrouped.add(j)
        return ungrouped