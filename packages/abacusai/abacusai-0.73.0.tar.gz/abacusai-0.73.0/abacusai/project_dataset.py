from .return_class import AbstractApiClass


class ProjectDataset(AbstractApiClass):
    """
        The description of how a dataset is used in a project

        Args:
            client (ApiClient): An authenticated API Client instance
            name (str): The name for the dataset.
            featureGroupTableName (str): The feature group table name for this dataset
            datasetType (str): The dataset's type in this project. The possible values will be based on the project's use-case. See the (Use Case Documentation)[https://api.abacus.ai/app/help/useCases] for more details.
            datasetId (str): The unique ID associated with the dataset.
            streaming (bool): true if the dataset is a streaming dataset.
    """

    def __init__(self, client, name=None, featureGroupTableName=None, datasetType=None, datasetId=None, streaming=None):
        super().__init__(client, None)
        self.name = name
        self.feature_group_table_name = featureGroupTableName
        self.dataset_type = datasetType
        self.dataset_id = datasetId
        self.streaming = streaming

    def __repr__(self):
        return f"ProjectDataset(name={repr(self.name)},\n  feature_group_table_name={repr(self.feature_group_table_name)},\n  dataset_type={repr(self.dataset_type)},\n  dataset_id={repr(self.dataset_id)},\n  streaming={repr(self.streaming)})"

    def to_dict(self):
        """
        Get a dict representation of the parameters in this class

        Returns:
            dict: The dict value representation of the class parameters
        """
        return {'name': self.name, 'feature_group_table_name': self.feature_group_table_name, 'dataset_type': self.dataset_type, 'dataset_id': self.dataset_id, 'streaming': self.streaming}
