class Identified(object):
    id = ''

    def __init__(self, id):
        self.id = id

    def asDict(self):
        d = {}
        d['id'] = self.id
        return d


class DocumentHash(Identified):
    content = ''
    attributes = {}

    def __init__(self, id, content, attributes):
        super().__init__(id)
        self.content = content
        self.attributes = attributes

    def category(self):
        if 'category' in self.attributes:
            return self.attributes['category']
        else:
            print('category was not in attributes')
            return ""

    def original(self):
        if 'original' in self.attributes:
            return self.attributes['original']
        else:
            print('original was not in attributes')
            return ''


class DocumentProcessingStats(Identified):
    features_after_processing = []
    features_prior_processing = []
    num_features_after_processing = 0
    num_features_prior_processing = 0
    category = ''

    def __init__(self, id, features_after_processing, features_prior_processing, category):
        super().__init__(id)
        self.features_after_processing = features_after_processing
        self.features_prior_processing = features_prior_processing
        self.num_features_after_processing = len(self.unique_features_after_processing())
        self.num_features_prior_processing = len(self.unique_features_prior_processing())
        self.category = category

    def unique_features_after_processing(self):
        return set(self.features_after_processing)

    def unique_features_prior_processing(self):
        return set(self.features_prior_processing)


class DocumentProcessingAggregateStats(Identified):
    stats = []
    total_features_prior_processing = 0.
    total_features_after_processing = 0.
    reduction_by_categories = {}

    def __init__(self, id, stats, total_features_prior_processing, total_features_after_processing, reduction_percent_by_categories = None):
        super().__init__(id)
        self.stats = stats
        self.total_features_after_processing = total_features_after_processing
        self.total_features_prior_processing = total_features_prior_processing
        self.reduction_by_categories = reduction_percent_by_categories


    def as_json(self):
        base = super().asDict()
        base['features prior processing'] = self.total_features_prior_processing
        base['features after processing'] = self.total_features_after_processing

        total_reduction_percent = round((1 - self.total_features_after_processing / self.total_features_prior_processing) * 100, 3)
        base['reduction (%)'] = total_reduction_percent

        reduction_by_categories_percentages = {}
        for k,v in self.reduction_by_categories.items():
            reduction_by_categories_percentages[k] = round(v * 100, 3)

        base['reduction (%) by category'] = reduction_by_categories_percentages
        return base
