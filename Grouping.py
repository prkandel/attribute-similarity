class Grouping:
    def __init__(self, pairwise_similarity, threshold):
        self.pairwise_similarity = pairwise_similarity
        self.threshold = threshold
        self.ungrouped = set([])
        self.groups = []

    def get_groups(self):
        self.initialize_ungrouped()
        for i in self.pairwise_similarity:
            for j in self.pairwise_similarity[i]:
                if self.pairwise_similarity[i][j] >= self.threshold:
                    if i in self.ungrouped and j in self.ungrouped:
                        self.groups.append([i, j])
                        self.ungrouped.remove(i)
                        self.ungrouped.remove(j)
                    elif self.get_group_number(i) is not None and self.get_group_number(j) is not None:
                        group_number_1 = self.get_group_number(i)
                        group_number_2 = self.get_group_number(j)
                        if group_number_1 != group_number_2:
                            if self.check_pairwise_similarity_for_groups(group_number_1, group_number_2,):
                                self.merge_groups(group_number_1, group_number_2)
                    else:
                        if self.get_group_number(i) is not None:
                            existing_group = self.groups[self.get_group_number(i)]
                            existing_group_number = self.get_group_number(i)
                            isolated = j
                        else:
                            existing_group = self.groups[self.get_group_number(j)]
                            existing_group_number = self.get_group_number(j)
                            isolated = i
                        if self.check_similarity_with_group(existing_group, isolated):
                            self.groups[existing_group_number].append(isolated)
                            self.ungrouped.remove(isolated)
        self.add_all_ungrouped()
        return self.groups

    def get_group_number(self, i):
        for idx, group in enumerate(self.groups):
            if i in group:
                return idx
        return None

    def check_pairwise_similarity_for_groups(self, group_number_1, group_number_2):
        for x in self.groups[group_number_1]:
            for y in self.groups[group_number_2]:
                if x in self.pairwise_similarity and y in self.pairwise_similarity[x]:
                    similarity = self.pairwise_similarity[x][y]
                elif y in self.pairwise_similarity and x in self.pairwise_similarity[y]:
                    similarity = self.pairwise_similarity[y][x]

                if similarity < self.threshold:
                    return False
        return True;

    def check_similarity_with_group(self, existing_group, isolated):
        for i in existing_group:
            if i in self.pairwise_similarity and isolated in self.pairwise_similarity[i]:
                similarity = self.pairwise_similarity[i][isolated]
            elif isolated in self.pairwise_similarity and i in self.pairwise_similarity[isolated]:
                similarity = self.pairwise_similarity[isolated][i]
            if similarity < self.threshold:
                return False
        return True;

    def merge_groups(self, group_number_1, group_number_2):
        self.groups[group_number_1] = self.groups[group_number_1] + self.groups[group_number_2]
        self.groups.remove(self.groups[group_number_2])

    def add_all_ungrouped(self):
        for obj in self.ungrouped:
            self.groups.append([obj])

    def initialize_ungrouped(self):
        for i in self.pairwise_similarity:
            self.ungrouped.add(i)
            for j in self.pairwise_similarity[i]:
                self.ungrouped.add(j)
