from raga import *
import pandas as pd
import json
import datetime

def get_timestamp_x_hours_ago(hours):
    current_time = datetime.datetime.now()
    delta = datetime.timedelta(days=90, hours=hours)
    past_time = current_time - delta
    timestamp = int(past_time.timestamp())
    return timestamp

def convert_json_to_data_frame(json_file_path_model_1, json_file_path_model_2):
    test_data_frame = []
    with open(json_file_path_model_1, 'r') as json_file:
        # Load JSON data
        model_1 = json.load(json_file)
    with open(json_file_path_model_2, 'r') as json_file:
        # Load JSON data
        model_2 = json.load(json_file)

    # Create a dictionary to store the inputs and corresponding data points
    inputs_dict = {}
    hr = 1
    # Process model_1 data
    for item in model_1:
        inputs = item["inputs"]
        inputs_dict[tuple(inputs)] = item
    
    # Process model_2 data
    for item in model_2:
        inputs = item["inputs"]
        AnnotationsV1 = ImageDetectionObject()
        ROIVectorsM1 = ROIEmbedding()
        ImageVectorsM1 = ImageEmbedding()
        for index, detection in enumerate(item["outputs"][0]["detections"]):
            id = index+1
            AnnotationsV1.add(ObjectDetection(Id=id, ClassId=0, ClassName=detection['class'], Confidence=detection['confidence'], BBox= detection['bbox'], Format="xywh_normalized"))
            ROIVectorsM1.add(id=id, embedding_values=[float(num_str) for num_str in detection['roi_embedding']])
                
            attributes_dict = {}
            attributes = item.get("attributes", {})
            for key, value in attributes.items():
                attributes_dict[key] = StringElement(value)
            image_embeddings = item.get("image_embedding", {})
            for value in image_embeddings:
                ImageVectorsM1.add(Embedding(value))

        merged_item = inputs_dict.get(tuple(inputs), {})
        AnnotationsV2 = ImageDetectionObject()
        ROIVectorsM2 = ROIEmbedding()
        ImageVectorsM2 = ImageEmbedding()
        for index, detection in enumerate(merged_item["outputs"][0]["detections"]):
            id = index+1
            AnnotationsV2.add(ObjectDetection(Id=id, ClassId=0, ClassName=detection['class'], Confidence=detection['confidence'], BBox= detection['bbox'], Format="xywh_normalized"))
            ROIVectorsM2.add(id=id, embedding_values=[float(num_str) for num_str in detection['roi_embedding']])
        
        image_embeddings = merged_item.get("image_embedding", {})
        for value in image_embeddings:
            ImageVectorsM2.add(Embedding(value))

        data_point = {
            'ImageId': StringElement(item["inputs"][0]),
            'ImageUri': StringElement(item["inputs"][0]),
            'TimeOfCapture': TimeStampElement(get_timestamp_x_hours_ago(hr)),
            'SourceLink': StringElement(item["inputs"][0]),
            'AnnotationsV1': AnnotationsV1,
            'ROIVectorsM1': ROIVectorsM1,
            'ImageVectorsM1': ImageVectorsM1,
            'AnnotationsV2': AnnotationsV2,
            'ROIVectorsM2': ROIVectorsM2,
            'ImageVectorsM2': ImageVectorsM2,
        }

        merged_dict = {**data_point, **attributes_dict}
        test_data_frame.append(merged_dict)
        hr+=1

    return test_data_frame



#Convert JSON dataset to pandas Data Frame
pd_data_frame = pd.DataFrame(convert_json_to_data_frame("test-dataset-modelA.json", "test-dataset-modelB.json"))

data_frame_extractor(pd_data_frame).to_csv("roi_embade.csv", index=False)

# create schema object of RagaSchema instance
schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement(), pd_data_frame)
schema.add("ImageUri", ImageUriSchemaElement(), pd_data_frame)
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement(), pd_data_frame)
schema.add("SourceLink", FeatureSchemaElement(), pd_data_frame)
schema.add("Reflection", AttributeSchemaElement(), pd_data_frame)
schema.add("Overlap", AttributeSchemaElement(), pd_data_frame)
schema.add("CameraAngle", AttributeSchemaElement(), pd_data_frame)
schema.add("AnnotationsV1", InferenceSchemaElement(model="modelA"), pd_data_frame)
schema.add("ImageVectorsM1", ImageEmbeddingSchemaElement(model="modelA"), pd_data_frame)
schema.add("ROIVectorsM1", RoiEmbeddingSchemaElement(model="modelA"), pd_data_frame)
schema.add("AnnotationsV2", InferenceSchemaElement(model="modelB"), pd_data_frame)
schema.add("ImageVectorsM2", ImageEmbeddingSchemaElement(model="modelB"), pd_data_frame)
schema.add("ROIVectorsM2", RoiEmbeddingSchemaElement(model="modelB"), pd_data_frame)

# # #create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject",run_name= "exp-jul-18-v1.02")

# # #create test_ds object of Dataset instance
test_ds = Dataset(test_session=test_session, name="test-dataset-v1.02")

# #load schema and pandas data frame
test_ds.load(data=pd_data_frame, schema=schema)


# #Params for unlabelled AB Model Testing
testName = StringElement("test-jun-5")
modelA = StringElement("modelA")
modelB = StringElement("modelB")
type = ModelABTestTypeElement("unlabelled")
aggregation_level = AggregationLevelElement()
aggregation_level.add(StringElement("Reflection"))
aggregation_level.add(StringElement("Overlap"))
aggregation_level.add(StringElement("CameraAngle"))
rules = ModelABTestRules()
rules.add(metric = StringElement("difference_percentage"), IoU = FloatElement(0.5), _class = StringElement("ALL"), threshold = FloatElement(0.2))
rules.add(metric = StringElement("difference_count"), IoU = FloatElement(0.5), _class = StringElement("canned_food"), threshold = FloatElement(0.5))

#create payload for model ab testing
# model_comparison_check = model_ab_test(test_session, dataset_name="test-dataset-1", testName=testName, modelA = modelA , modelB = modelB , type = type, rules = rules, aggregation_level=aggregation_level)

# #add payload into test_session object
# test_session.add(model_comparison_check)

# #run added ab test model payload
# test_session.run()


testName = StringElement("test-labelled-jun-1")
train_dataset_name = StringElement("Train_Ds")
field_dataset_name = StringElement("Field_Ds")
train_embed_col_name = StringElement("Train_embed")
field_embed_col_name = StringElement("Field_embed")
level = StringElement("roi")
aggregation_level = AggregationLevelElement()
aggregation_level.add(StringElement("Reflection"))
aggregation_level.add(StringElement("Overlap"))
aggregation_level.add(StringElement("CameraAngle"))
rules = DriftDetectionRules()
rules.add(type=StringElement("anomaly_detection"), dist_metric=StringElement("Euclidian"), _class = StringElement("ALL"), threshold = FloatElement(0.5))

edge_case_detection = data_drift_detection(test_session, testName=testName, train_dataset_name=train_dataset_name, field_dataset_name=field_dataset_name, train_embed_col_name=train_embed_col_name, field_embed_col_name = field_embed_col_name , level = level, aggregation_level=aggregation_level, rules = rules)

# print(edge_case_detection)

# #add payload into test_session object
test_session.add(edge_case_detection)

# #run added ab test model payload
test_session.run()