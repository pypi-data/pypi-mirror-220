from typing import Optional
from raga import  StringElement, AggregationLevelElement, ModelABTestRules, ModelABTestTypeElement, TestSession

def model_ab_test(test_session:TestSession, dataset_name: str, testName: StringElement, modelA: StringElement, modelB: StringElement,
                  type: ModelABTestTypeElement, rules: ModelABTestRules, aggregation_level:  Optional[AggregationLevelElement] = AggregationLevelElement(),
                  gt: Optional[StringElement] = StringElement(""), filter: Optional[StringElement] = StringElement("")):
    dataset_id = ab_test_validation(test_session=test_session, dataset_name=dataset_name, testName=testName, modelA=modelA, modelB=modelB, type=type, rules=rules, gt=gt)    
    response = {
            "datasetId": dataset_id,
            "experimentId": test_session.experiment_id,
            "name": testName.get(),
            "modelA": modelA.get(),
            "modelB": modelB.get(),
            "type": type.get(),
            "rules": rules.get(),
            "aggregationLevels": aggregation_level.get(),
            'filter':filter.get(),
            'gt':gt.get(),
            'test_type':'ab_test'
        }
    return response


def ab_test_validation(test_session:TestSession, dataset_name: str, testName: StringElement, modelA: StringElement, modelB: StringElement,
               type: ModelABTestTypeElement, rules: ModelABTestRules,
               gt: Optional[StringElement] = StringElement("")):
    res_data = test_session.http_client.get(f"api/dataset?projectId={test_session.project_id}&name={dataset_name}", headers={"Authorization": f'Bearer {test_session.token}'})
    if not isinstance(res_data, dict):
            raise ValueError("Invalid response data. Expected a dictionary.")
    dataset_id = res_data.get("data", {}).get("id")
    if not dataset_id:
        raise KeyError("Invalid response data. Token not found.")
    
    assert isinstance(test_session, TestSession), "test_session must be an instance of the TestSession class."
    assert isinstance(dataset_name, str) and dataset_name, "dataset_name is required and must be str."
    assert isinstance(testName, StringElement) and testName.get(), "testName is required and must be an instance of the StringElement class."
    assert isinstance(modelA, StringElement) and modelA.get(), "modelA is required and must be an instance of the StringElement class."
    assert isinstance(modelB, StringElement) and modelB.get(), "modelB is required and must be an instance of the StringElement class."
    assert isinstance(type, ModelABTestTypeElement), "type must be an instance of the ModelABTestTypeElement class."
    assert isinstance(rules, ModelABTestRules) and rules.get(), "rules is required and must be an instance of the ModelABTestRules class."

    if type.get() == "labelled":
        assert isinstance(gt, StringElement) and gt.get(), "gt is required on labelled type and must be an instance of the StringElement class."

    if type.get() == "unlabelled":
        if isinstance(gt, StringElement) and gt.get():
            raise ValueError("gt is not required on unlabelled type.")
    return dataset_id
