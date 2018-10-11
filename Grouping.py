class Grouping:
    def __init__(self, pairwise_similarity_list, threshold):
        self.pairwise_similarity_list = pairwise_similarity_list
        self.threshold = threshold
        self.ungrouped = set([])
        self.groups = []

    def get_groups(self):
        self.initialize_ungrouped()
        for pair in self.pairwise_similarity_list:
            if pair.similarity >= self.threshold:
                if pair.id1 in self.ungrouped and pair.id2 in self.ungrouped:
                    self.groups.append([pair.id1, pair.id2])
                    self.ungrouped.remove(pair.id1)
                    self.ungrouped.remove(pair.id2)
                elif self.get_group_number(pair.id1) is not None and self.get_group_number(pair.id2) is not None:
                    group_number_1 = self.get_group_number(pair.id1)
                    group_number_2 = self.get_group_number(pair.id2)
                    if group_number_1 != group_number_2:
                        if self.check_pairwise_similarity_for_groups(group_number_1, group_number_2,):
                            self.merge_groups(group_number_1, group_number_2)
                else:
                    if self.get_group_number(pair.id1) is not None:
                        existing_group = self.groups[self.get_group_number(pair.id1)]
                        existing_group_number = self.get_group_number(pair.id1)
                        isolated = pair.id2
                    else:
                        existing_group = self.groups[self.get_group_number(pair.id2)]
                        existing_group_number = self.get_group_number(pair.id2)
                        isolated = pair.id1
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
                similarity = self.find_similarity_between_two_entities(x,y)
                if similarity < self.threshold:
                    return False
        return True;

    def find_similarity_between_two_entities(self, id1, id2):
        for pair in self.pairwise_similarity_list:
            if (id1 == pair.id1 and id2 == pair.id2) or (id2 == pair.id1 and id1 == pair.id2):
                return pair.similarity

    def check_similarity_with_group(self, existing_group, isolated):
        for i in existing_group:
            similarity = self.find_similarity_between_two_entities(i,isolated)
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
        for pair in self.pairwise_similarity_list:
            self.ungrouped.add(pair.id1)
            self.ungrouped.add(pair.id2)

    def sort_pairwise_similarity_list(self):
        self.pairwise_similarity_list.sort(key=lambda x: x.count, reverse=True)
