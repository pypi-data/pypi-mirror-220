from raga import *
import pandas as pd
import json
import time

ds_json_file = "train_modelA.json"
ds_json_file1 = "field_modelA.json"

model_name = "Train"
model_name1 = "Field"


test_df = []
with open(ds_json_file, 'r') as json_file:
    # Load JSON data
    json_data = json.load(json_file)
    
    # Process the JSON data
    transformed_data = []
    for item in json_data:
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

        data_point = {
            'ImageUri':StringElement(item["image_url"]),
            'ImageId': StringElement(item["inputs"][0]),
            'TimeOfCapture': TimeStampElement(item["capture_time"]),
            'SourceLink': StringElement(item["inputs"][0]),
            f'Annotations {model_name}': AnnotationsV1,
            f'ImageVectors {model_name}': ImageVectorsM1,
            f'ROIVectors {model_name}': ROIVectorsM1,
        }

        merged_dict = {**data_point, **attributes_dict}

        test_df.append(merged_dict)
        

pd_data_frame = pd.DataFrame(test_df)

test_df1 = []
with open(ds_json_file1, 'r') as json_file:
    # Load JSON data
    json_data = json.load(json_file)
    
    # Process the JSON data
    transformed_data = []
    for item in json_data:
        AnnotationsV2 = ImageDetectionObject()
        ROIVectorsM2 = ROIEmbedding()
        ImageVectorsM2 = ImageEmbedding()
        for detection in item["outputs"][0]["detections"]:
            AnnotationsV2.add(ObjectDetection(Id=0, ClassId=0, ClassName=detection['class'], Confidence=detection['confidence'], BBox= detection['bbox'], Format="xywh_normalized"))
            for roi_emb in detection['roi_embedding']:
                ROIVectorsM2.add(Embedding(roi_emb))
        
        attributes_dict = {}
        attributes = item.get("attributes", {})
        for key, value in attributes.items():
            attributes_dict[key] = StringElement(value)

        image_embeddings = item.get("image_embedding", {})
        for value in image_embeddings:
            ImageVectorsM2.add(Embedding(value))

        data_point = {
            'ImageUri':StringElement(item["image_url"]),
            'ImageId': StringElement(item["inputs"][0]),
            'TimeOfCapture': TimeStampElement(item["capture_time"]),
            'SourceLink': StringElement(item["inputs"][0]),
            f'Annotations {model_name1}': AnnotationsV2,
            f'ImageVectors {model_name1}': ImageVectorsM2,
            f'ROIVectors {model_name1}': ROIVectorsM2,
        }

        merged_dict = {**data_point, **attributes_dict}

        test_df1.append(merged_dict)
        

pd_data_frame1 = pd.DataFrame(test_df1)

#create schema object of RagaSchema instance
schema = RagaSchema()
schema.add("ImageUri", ImageUriSchemaElement(), pd_data_frame)
schema.add("ImageId", PredictionSchemaElement(), pd_data_frame)
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement(), pd_data_frame)
schema.add("SourceLink", FeatureSchemaElement(), pd_data_frame)
schema.add("Reflection", AttributeSchemaElement(), pd_data_frame)
schema.add("Overlap", AttributeSchemaElement(), pd_data_frame)
schema.add("CameraAngle", AttributeSchemaElement(), pd_data_frame)
schema.add(f"Annotations {model_name}", InferenceSchemaElement(model=model_name), pd_data_frame)
schema.add(f"ImageVectors {model_name}", ImageEmbeddingSchemaElement(model=model_name, ref_col_name=""), pd_data_frame)
schema.add(f"ROIVectors {model_name}", RoiEmbeddingSchemaElement(model=model_name, ref_col_name=""), pd_data_frame)

schema1 = RagaSchema()
schema1.add("ImageUri", ImageUriSchemaElement(), pd_data_frame1)
schema1.add("ImageId", PredictionSchemaElement(), pd_data_frame1)
schema1.add("TimeOfCapture", TimeOfCaptureSchemaElement(), pd_data_frame1)
schema1.add("SourceLink", FeatureSchemaElement(), pd_data_frame1)
schema1.add("Reflection", AttributeSchemaElement(), pd_data_frame1)
schema1.add("Overlap", AttributeSchemaElement(), pd_data_frame1)
schema1.add("CameraAngle", AttributeSchemaElement(), pd_data_frame1)
schema1.add(f"Annotations {model_name1}", InferenceSchemaElement(model=model_name1), pd_data_frame1)
schema1.add(f"ImageVectors {model_name1}", ImageEmbeddingSchemaElement(model=model_name1, ref_col_name=""), pd_data_frame1)
schema1.add(f"ROIVectors {model_name1}", RoiEmbeddingSchemaElement(model=model_name1 ,ref_col_name=""), pd_data_frame1)

project_name = "testingProject" # Project Name
run_name= "K_Drift_Exp_19Jul_V02" # Experiment Name
dataset_name_t = "k_drift_trainds_19jul_V02" # Dataset Name for train
dataset_name_f = "k_drift_fieldds_19jul_V02" # Dataset Name for feild
train_embed_col_name = f'ImageVectors{model_name}' #Train dataset embedding column name
field_embed_col_name = f'ImageVectors{model_name1}' #Field dataset embedding column name





#create test_session object of TestSession instance
test_session = TestSession(project_name=project_name,run_name=run_name)



#create test_ds object of Train Dataset instance
test_ds1 = Dataset(test_session=test_session, name=dataset_name_t)

#load schema and pandas data frame of train dataset

test_ds1.load(pd_data_frame, schema)

# time.sleep(20)

# time.sleep(5)
# input()
#
#create test_ds object of Feild Dataset instance
test_ds2 = Dataset(test_session=test_session, name=dataset_name_f)

#load schema and pandas data frame of Feild Dataset
test_ds2.load(pd_data_frame1, schema1)


#  #add payload into test_session object
# test_session.add(data_drift_detection)

testName = StringElement("test-labelled-jun-1")
train_dataset_name = StringElement("k_drift_trainds_19jul_V02")
field_dataset_name = StringElement("k_drift_fieldds_19jul_V02")
train_embed_col_name = StringElement("ImageVectors Train")
field_embed_col_name = StringElement("ImageVectors Field")
level = StringElement("image")
aggregation_level = AggregationLevelElement()
aggregation_level.add(StringElement("Reflection"))
aggregation_level.add(StringElement("Overlap"))
aggregation_level.add(StringElement("CameraAngle"))
rules = DriftDetectionRules()
rules.add(type=StringElement("anomaly_detection"), metric=StringElement("Euclidian"), _class = StringElement("ALL"), threshold = FloatElement(0.2))

edge_case_detection = data_drift_detection(test_session, testName=testName, train_dataset_name=train_dataset_name, field_dataset_name=field_dataset_name, train_embed_col_name=train_embed_col_name, field_embed_col_name = field_embed_col_name , level = level, aggregation_level=aggregation_level, rules = rules)

# print(edge_case_detection)

# #add payload into test_session object
test_session.add(edge_case_detection)

# #run added ab test model payload
test_session.run()
