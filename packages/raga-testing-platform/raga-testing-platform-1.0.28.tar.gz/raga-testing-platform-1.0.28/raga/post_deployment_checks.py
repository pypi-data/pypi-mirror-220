from typing import Optional
from raga import StringElement, AggregationLevelElement, TestSession, DriftDetectionRules

def data_drift_detection(test_session:TestSession, train_dataset_name: str, field_dataset_name: str, testName: StringElement, train_embed_col_name: StringElement, field_embed_col_name: StringElement, level: StringElement, rules=DriftDetectionRules, aggregation_level:  Optional[AggregationLevelElement] = AggregationLevelElement(),
filter: Optional[StringElement] = StringElement("")):
    
    train_dataset_id, field_dataset_id = data_drift_detection_validation(test_session=test_session, train_dataset_name=train_dataset_name, field_dataset_name=field_dataset_name, testName=testName, train_embed_col_name=train_embed_col_name, field_embed_col_name=field_embed_col_name, level=level, rules=rules)    
    response = {
            "datasetId": field_dataset_id,
            "experimentId": test_session.experiment_id,
            "name": testName.get(),
            "aggregationLevels": aggregation_level.get(),
            "filter":filter.get(),
            "trainDatasetId":train_dataset_id,
            "trainEmbedColName": train_embed_col_name.get(),
            "fieldEmbedColName": field_embed_col_name.get(),
            "level": level.get(),
            "rules": rules.get(),
            'test_type':'drift_test'
        }
    return response


def data_drift_detection_validation(test_session:TestSession, train_dataset_name: StringElement, field_dataset_name: StringElement, testName: StringElement, train_embed_col_name: StringElement, field_embed_col_name: StringElement, level: StringElement, rules=DriftDetectionRules
               ):
    train_res_data = test_session.http_client.get(f"api/dataset?projectId={test_session.project_id}&name={train_dataset_name.get()}", headers={"Authorization": f'Bearer {test_session.token}'})
    if not isinstance(train_res_data, dict):
            raise ValueError("Invalid response data. Expected a dictionary.")
    train_dataset_id = train_res_data.get("data", {}).get("id")
    if not train_dataset_id:
        raise KeyError("Invalid response data. Token not found.")
    
    field_res_data = test_session.http_client.get(f"api/dataset?projectId={test_session.project_id}&name={field_dataset_name.get()}", headers={"Authorization": f'Bearer {test_session.token}'})
    if not isinstance(field_res_data, dict):
            raise ValueError("Invalid response data. Expected a dictionary.")
    field_dataset_id = field_res_data.get("data", {}).get("id")
    if not field_dataset_id:
        raise KeyError("Invalid response data. Token not found.")
    
    assert isinstance(test_session, TestSession), "test_session must be an instance of the TestSession class."
    assert isinstance(train_dataset_name, StringElement) and train_dataset_name.get(), "train_dataset_name is required and must be an instance of the StringElement class."
    assert isinstance(field_dataset_name, StringElement) and field_dataset_name.get(), "field_dataset_name is required and must be an instance of the StringElement class."
    assert isinstance(testName, StringElement) and testName.get(), "testName is required and must be an instance of the StringElement class."
    assert isinstance(train_embed_col_name, StringElement) and train_embed_col_name.get(), "train_embed_col_name is required and must be an instance of the StringElement class."
    assert isinstance(field_embed_col_name, StringElement) and field_embed_col_name.get(), "field_embed_col_name is required and must be an instance of the StringElement class."
    assert isinstance(level, StringElement) and level.get(), "level is required and must be an instance of the StringElement class."
    assert isinstance(rules, DriftDetectionRules) and rules.get(), "rules is required and must be an instance of the ModelABTestRules class."

    return train_dataset_id, field_dataset_id
