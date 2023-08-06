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

def convert_json_to_data_frame(json_file_path_model_1, json_file_path_model_2, json_file_path_model_3):
    test_data_frame = []
    with open(json_file_path_model_1, 'r') as json_file:
        # Load JSON data
        model_1 = json.load(json_file)
    with open(json_file_path_model_2, 'r') as json_file:
        # Load JSON data
        model_2 = json.load(json_file)
    
    with open(json_file_path_model_3, 'r') as json_file:
        # Load JSON data
        model_gt = json.load(json_file)

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
        for detection in item["outputs"][0]["detections"]:
            AnnotationsV1.add(ObjectDetection(Id=0, ClassId=0, ClassName=detection['class'], Confidence=detection['confidence'], BBox= detection['bbox'], Format="xywh_normalized"))
            for roi_emb in detection['roi_embedding']:
                ROIVectorsM1.add(Embedding(roi_emb))
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
        for detection in merged_item["outputs"][0]["detections"]:
            AnnotationsV2.add(ObjectDetection(Id=0, ClassId=0, ClassName=detection['class'], Confidence=detection['confidence'], BBox= detection['bbox'], Format="xywh_normalized"))
            for roi_emb in detection['roi_embedding']:
                ROIVectorsM2.add(Embedding(roi_emb))
        
        image_embeddings = merged_item.get("image_embedding", {})
        for value in image_embeddings:
            ImageVectorsM2.add(Embedding(value))
        
        merged_item2 = inputs_dict.get(tuple(inputs), {})
        AnnotationsV3 = ImageDetectionObject()
        ROIVectorsM3 = ROIEmbedding()
        ImageVectorsM3 = ImageEmbedding()
        for detection in merged_item2["outputs"][0]["detections"]:
            AnnotationsV3.add(ObjectDetection(Id=0, ClassId=0, ClassName=detection['class'], Confidence=detection['confidence'], BBox= detection['bbox'], Format="xywh_normalized"))
            for roi_emb in detection['roi_embedding']:
                ROIVectorsM3.add(Embedding(roi_emb))
        
        image_embeddingsGT = merged_item2.get("image_embedding", {})
        for value in image_embeddingsGT:
            ImageVectorsM3.add(Embedding(value))


        data_point = {
            'ImageUri':StringElement(item["image_url"]),
            'ImageId': StringElement(item["inputs"][0]),
            'TimeOfCapture': TimeStampElement(get_timestamp_x_hours_ago(hr)),
            'SourceLink': StringElement(item["inputs"][0]),
            'AnnotationsV1': AnnotationsV1,
            'ROIVectorsM1': ROIVectorsM1,
            'ImageVectorsM1': ImageVectorsM1,
            'AnnotationsV2': AnnotationsV2,
            'ROIVectorsM2': ROIVectorsM2,
            'ImageVectorsM2': ImageVectorsM2,
            'AnnotationsV3': AnnotationsV3,
            'ROIVectorsM3': ROIVectorsM3,
            'ImageVectorsM3': ImageVectorsM3,
            
        }

        merged_dict = {**data_point, **attributes_dict}
        test_data_frame.append(merged_dict)
        hr+=1

    return test_data_frame



#Convert JSON dataset to pandas Data Frame
pd_data_frame = pd.DataFrame(convert_json_to_data_frame("ma.json", "mb.json", "gt.json"))

# pd_data_frame.to_pickle("TestingDataFrame.pkl")

schema = RagaSchema()
schema.add("ImageUri", ImageUriSchemaElement(), pd_data_frame)
schema.add("ImageId", PredictionSchemaElement(), pd_data_frame)
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement(), pd_data_frame)
schema.add("SourceLink", FeatureSchemaElement(), pd_data_frame)
schema.add("Reflection", AttributeSchemaElement(), pd_data_frame)
schema.add("Overlap", AttributeSchemaElement(), pd_data_frame)
schema.add("CameraAngle", AttributeSchemaElement(), pd_data_frame)
schema.add("AnnotationsV1", InferenceSchemaElement(model="modelA"), pd_data_frame)
schema.add("ImageVectorsM1", ImageEmbeddingSchemaElement(model="modelA", ref_col_name=""), pd_data_frame)
schema.add("ROIVectorsM1", RoiEmbeddingSchemaElement(model="modelA", ref_col_name=""), pd_data_frame)
schema.add("AnnotationsV2", InferenceSchemaElement(model="modelB"), pd_data_frame)
schema.add("ImageVectorsM2", ImageEmbeddingSchemaElement(model="modelB", ref_col_name=""), pd_data_frame)
schema.add("ROIVectorsM2", RoiEmbeddingSchemaElement(model="modelB", ref_col_name=""), pd_data_frame)
schema.add("AnnotationsV3", InferenceSchemaElement(model="modelGT"), pd_data_frame)
schema.add("ImageVectorsM3", ImageEmbeddingSchemaElement(model="modelGT", ref_col_name=""), pd_data_frame)
schema.add("ROIVectorsM3", RoiEmbeddingSchemaElement(model="modelGT", ref_col_name=""), pd_data_frame)


project_name = "testingProject" # Project Name
run_name= "K_PD_Exp_18Jul_V8" # Experiment Name
dataset_name = "k_pd_ds_18jul_v8" # Dataset Name


#create test_session object of TestSession instance
test_session = TestSession(project_name=project_name,run_name=run_name)

#create test_ds object of Dataset instance
test_ds = Dataset(test_session=test_session, name=dataset_name)

#load schema and pandas data frame
test_ds.load(pd_data_frame, schema)


# # Params for unlabelled AB Model Testing
# testName = StringElement("QA_Unlabelled_04Jul_03")
# modelA = StringElement("modelA")
# modelB = StringElement("modelB")
# type = ModelABTestTypeElement("unlabelled")
# aggregation_level = AggregationLevelElement()
# aggregation_level.add(StringElement("Reflection"))
# aggregation_level.add(StringElement("Overlap"))
# aggregation_level.add(StringElement("CameraAngle"))
# rules = ModelABTestRules()
# rules.add(metric = StringElement("difference_all"), IoU = FloatElement(0.5), _class = StringElement("ALL"), threshold = FloatElement(0.5))
# rules.add(metric = StringElement("difference_candy"), IoU = FloatElement(0.5), _class = StringElement("candy"), threshold = FloatElement(0.5))
# rules.add(metric = StringElement("difference_drink"), IoU = FloatElement(0.5), _class = StringElement("drink"), threshold = FloatElement(0.5))
# rules.add(metric = StringElement("difference_tissue"), IoU = FloatElement(0.5), _class = StringElement("tissue"), threshold = FloatElement(0.5))
# rules.add(metric = StringElement("difference_canned_food"), IoU = FloatElement(0.5), _class = StringElement("canned_food"), threshold = FloatElement(0.5))

# #create payload for model ab testing
# model_comparison_check = model_ab_test(test_session, dataset_name=dataset_name, testName=testName, modelA = modelA , modelB = modelB , type = type, aggregation_level = aggregation_level, rules = rules)


# #add payload into test_session object
# test_session.add(model_comparison_check)

# #run added ab test model payload
# test_session.run()

# Params for labelled AB Model Testing
testName = StringElement("QA_Labelled_04Jul_02")
modelA = StringElement("modelA")
modelB = StringElement("modelB")
gt = StringElement("modelGT")
type = ModelABTestTypeElement("labelled")
aggregation_level = AggregationLevelElement()
aggregation_level.add(StringElement("Reflection"))
aggregation_level.add(StringElement("Overlap"))
aggregation_level.add(StringElement("CameraAngle"))
rules = ModelABTestRules()
rules.add(metric = StringElement("precision_diff_all"), IoU = FloatElement(0.5), _class = StringElement("ALL"), threshold = FloatElement(0.5))
rules.add(metric = StringElement("precision_candy"), IoU = FloatElement(0.5), _class = StringElement("candy"), threshold = FloatElement(0.5))
# rules.add(metric = StringElement("precision_tissue"), IoU = FloatElement(0.5), _class = StringElement("drink"), threshold = FloatElement(0.5))

#create payload for model ab testing
model_comparison_check = model_ab_test(test_session, dataset_name=dataset_name, testName=testName, modelA = modelA , modelB = modelB ,aggregation_level = aggregation_level, type = type,  rules = rules, gt=gt)


#add payload into test_session object
test_session.add(model_comparison_check)

#run added ab test model payload
test_session.run()

# Params for unlabelled AB Model Testing
testName = StringElement("QA_Unlabelled_04Jul_03")
modelA = StringElement("modelA")
modelB = StringElement("modelB")
type = ModelABTestTypeElement("unlabelled")
aggregation_level = AggregationLevelElement()
aggregation_level.add(StringElement("Reflection"))
aggregation_level.add(StringElement("Overlap"))
aggregation_level.add(StringElement("CameraAngle"))
rules = ModelABTestRules()
rules.add(metric = StringElement("difference_all"), IoU = FloatElement(0.5), _class = StringElement("ALL"), threshold = FloatElement(0.5))
rules.add(metric = StringElement("difference_candy"), IoU = FloatElement(0.5), _class = StringElement("candy"), threshold = FloatElement(0.5))
rules.add(metric = StringElement("difference_drink"), IoU = FloatElement(0.5), _class = StringElement("drink"), threshold = FloatElement(0.5))
rules.add(metric = StringElement("difference_tissue"), IoU = FloatElement(0.5), _class = StringElement("tissue"), threshold = FloatElement(0.5))
rules.add(metric = StringElement("difference_canned_food"), IoU = FloatElement(0.5), _class = StringElement("canned_food"), threshold = FloatElement(0.5))

#create payload for model ab testing
model_comparison_check = model_ab_test(test_session, dataset_name=dataset_name, testName=testName, modelA = modelA , modelB = modelB , type = type, aggregation_level = aggregation_level, rules = rules)


#add payload into test_session object
test_session.add(model_comparison_check)

#run added ab test model payload
test_session.run()